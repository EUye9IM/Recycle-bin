# ------------------------------------------------
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: Anakin &
# Function: 实现语法分析器
# ------------------------------------------------
# !!! Attention: 本 py 使用了 python prettytable
# 				 实现表格打印，可以通过 pip 安装
# pip install prettytable
# ------------------------------------------------

import utility
from prettytable import PrettyTable
from grammar_reader import GrammerReader


# Parser class 定义
class Parser:
    """
    production type: list[dict{},...]
    eg: A->B
    form: [{left: A, right: B}, ...]
    ---------------------------------
    grammar type: dict{"vt": [], "vn": []}
    eg: {"vt": ['a', 'b'],
         "vn": ['A', 'B']}
    """

    def __init__(self, _production, _grammar):
        _grammar["vt"].append("$")
        _grammar["start"] = _production[0]["left"]
        self.production = _production
        self.grammar = _grammar
        # 首先计算 first 表，然后增广文法
        self.first_table = utility.single_first(self.production, self.grammar)
        self.to_argument_grammar()
        self.table = self.analysis_table(self.items())
        # 判断是否为 LR1 文法
        # if not self.is_lr1():
        #     error = "该文法存在移进归约冲突，不是 LR1 文法！\n" \
        #           "请检查是否存在'某一产生式的右部是另一产生式的前缀'情形！"
        #     raise Exception(error)

    # 扩展为增广文法
    def to_argument_grammar(self):
        start_obj = {"left": "S'", "right": [self.grammar.get("start")]}
        self.production.insert(0, start_obj)

    # 计算 CLOSURE(I)
    """
    i 为项目集，为 list, 每一个元素为 list,
    单元素的list 形式为 dict, dic 中包含 left, right, look
    即产生式的左右部分，展望符，right 为 list，look 为 str
    eg: I = {X->a.b}
    i = [{left: X, right: [a,.,b], look: '$'}, ...]
    """

    def closure(self, i: list):
        vn = self.grammar["vn"]
        vt = self.grammar["vt"]

        for item in i:
            right = item.get("right")  # 产生式右部
            index = right.index(".")
            if index < (len(right) - 1):  # "." 不在最后
                b = right[index + 1]
                if b in vn:  # b 为非终结符
                    for k in self.production:
                        if b == k.get("left"):  # b 为产生式左部
                            bta = None
                            if index < (len(right) - 2):
                                # bta = right[index + 2]
                                bta = right[index + 2 :] + [item.get("look")]
                            else:
                                bta = [item.get("look")]

                            first_b = utility.multi_first(self.first_table, bta)
                            for li in first_b:
                                obj = {
                                    "left": b,
                                    "right": ["."] + k.get("right"),
                                    "look": li,
                                }
                                if obj not in i and li in vt:
                                    i.append(obj)

        return i

    # 构造 LR(1) 自动机的状态集
    def items(self):
        # 文法已经扩充为增广文法，S' 开始
        start = {
            "left": self.production[0].get("left"),
            "right": ["."] + self.production[0].get("right"),
            "look": "$",
        }
        c = [
            self.closure(
                [
                    start,
                ]
            ),
        ]
        vt = self.grammar["vt"]
        vn = self.grammar["vn"]
        all_character = []  # 文法符号集合
        for i in vn:
            all_character.append(i)
        for i in vt:
            all_character.append(i)
        for i in c:
            for x in all_character:
                temp = self.go_to(i, x)
                if len(temp) != 0 and temp not in c:
                    c.append(temp)

        return c

    # GOTO 函数，返回项目集 I 对应于文法符号 X 的后继项目集闭包
    """
    GOTO(I, X) = CLOSURE({[A→αX·β,a] | [A→α·Xβ, a]∈I})
    """

    def go_to(self, i, x):
        j = []
        for item in i:
            a = item.get("look")  # 展望符
            left = item.get("left")  # LR0 项目左部
            right = item.get("right")  # LR0 项目右部
            index = right.index(".")
            if index == -1:
                raise Exception("非法 LR1 项目\n")
            elif index < (len(right) - 1) and right[index + 1] == x:
                # A→α·Xβ，存在 X
                if index < (len(right) - 2):  # 存在 beta
                    obj = {
                        "left": left,
                        "right": right[:index]
                        + [right[index + 1]]
                        + ["."]
                        + right[index + 2 :],
                        "look": a,
                    }
                    j.append(obj)
                else:  # 不存在 beta
                    obj = {
                        "left": left,
                        "right": right[:index] + [right[index + 1]] + ["."],
                        "look": a,
                    }
                    j.append(obj)
        return self.closure(j)

    # LR1 分析表构造
    """
    构造 G' 的规范 LR(1) 项集族C = { I0, I1, … , In}
    根据 Ii 构造得到状态 i, 状态 i 的语法分析动作按照下面的方法决定:
        if [A→α·aβ, b] ∈ Ii and GOTO( Ii , a)=Ij then ACTION[i, a]=sj
        if [A→α·Bβ, b] ∈ Ii and GOTO( Ii , B)=Ij then GOTO[i, B]=j
        if [A→α·, a] ∈ Ii 且 A ≠ S' then ACTION[i, a]=rj（j是产生式 A→α 的编号）
        if [S'→S·, $] ∈ Ii
    then ACTION [i, $] = acc;
    没有定义的所有条目都设置为“error”
    """

    def analysis_table(self, c):
        status = 0
        vt = self.grammar["vt"]
        vn = self.grammar["vn"]
        len3 = len(c)  # 状态集个数
        len1 = len(self.grammar["vt"])  # 终结符个数
        action_set = []  # ACTION 集合
        for i in range(len3):
            temp = []
            for _ in range(len1):
                temp.append([])
            action_set.append(temp)

        len2 = len(self.grammar["vn"])  # 非终结符个数
        goto_set = []  # GOTO 集合
        for i in range(len3):
            temp = []
            for _ in range(len2):
                temp.append([])
            goto_set.append(temp)

        for i in c:  # i 表示一个项目集
            for item in i:  # item 表示项目集中的每个项目[A→α·aβ, b]
                # lr0 = j[0]	# 第一个元素为 lr0 项目
                right = item.get("right")
                left = item.get("left")
                look = item.get("look")
                index = right.index(".")
                if index == -1:
                    raise Exception("LR1 项目有误")
                # -------------------------------------------------
                elif index < (len(right) - 1):
                    # 非归约项目，存在下一个状态
                    n = right[index + 1]  # '.'后面的文法符号
                    ij = self.go_to(i, n)
                    if n in vt:  # 下一个符号是终结符
                        # 设置为移入 j (j 为项集下标)
                        action_set[status][vt.index(n)].append("s" + str(c.index(ij)))
                    else:
                        goto_set[status][vn.index(n)].append(str(c.index(ij)))
                # --------------------------------------------------
                else:
                    # 归约项目或者接收项目
                    if (
                        left == "S'"
                        and right == ([self.grammar["start"]] + ["."])
                        and look == "$"
                    ):
                        # 接收项目
                        action_set[status][vt.index("$")].append("acc")
                    elif left != "S'":
                        # 归约项目
                        count = 0  # 归约对应的产生式的编号
                        s = right[:]  # 先复制再移除 "."
                        s.remove(".")
                        for li in self.production:
                            if left == li.get("left") and s == li.get("right"):
                                action_set[status][vt.index(look)].append(
                                    "r" + str(count)
                                )
                                break
                            count += 1
            # ------------------------------------------------------
            # end a item for
            status += 1
        return [action_set, goto_set]

    # 判断是否为LR1文法, lr_table 为生成的 LR 分析表
    """
    判断对应项目含有的操作个数(长度)是否 >= 2 即可,
    如果长度是2以上的话就说明有冲突,即该文法不是 LR1 文法
    """

    def is_lr1(self):
        lr_table = self.table
        for i in lr_table:
            for j in i:
                for k in j:
                    s = set(k)
                    if len(s) >= 2:
                        print(k)
                        return False

        return True

    # LR 分析，w 表示输入的字符串
    def analyze(self, w):
        lr_table = self.table
        w = w + ["$"]
        output = ["$"]  # 输出字符
        count = 0  # 记录输入字符串的索引
        a = w[count]  # 指针指向的输入字符
        vt = self.grammar["vt"]
        vn = self.grammar["vn"]
        action_table = lr_table[0]  # ACTION 表
        goto_table = lr_table[1]  # GOTO 表
        status_stack = [0]  # 初始状态下栈状态中只有状态 0

        # 设置表格样式
        t_num = 0
        x = PrettyTable()
        x.field_names = ["Num", "Stack", "Output stream", "Input stream", "Next action"]
        x.align["Num"] = "r"
        x.align["Stack"] = "l"
        x.align["Input stream"] = "r"
        x.align["Output stream"] = "l"
        x.align["Next action"] = "l"
        productions = []  # 记录产生式
        while True:
            # 行号
            t_num += 1
            # 栈状态打印
            t_stack = utility.prettytable_list(list(map(str, status_stack)))

            # 字符输入打印, 为防止输入过长，只取 6 个符号
            t_input = utility.prettytable_list(w[count:], 6)
            # 字符输出打印，原理同上
            t_output = utility.prettytable_list(output, 6)

            # ----------------begin---analyse------------------------
            s_top = status_stack[len(status_stack) - 1]  # 栈顶状态

            is_epsilon = False  # 记录是否为补充 epsilon
            if action_table[s_top][vt.index(a)]:
                operation = action_table[s_top][vt.index(a)][0]  # 获取当前操作
            else:
                # 补充 epsilon，分析文法
                try:
                    operation = action_table[s_top][vt.index("")][0]
                    is_epsilon = True
                except IndexError:
                    print("状态无法处理，语法错误")
                    break

                count -= 1  # 回退 count 指向
                # raise Exception("语法错误！")

            if "s" in operation:  # 移入操作
                t_action = "Shift " + str(operation[1:])
                status_stack.append(int(operation[1:]))  # 压入栈顶
                if is_epsilon:
                    output.append("ε")
                else:
                    output.append(w[count])
                count += 1
                a = w[count]  # 指向下一字符
            elif "r" in operation:
                # 归约操作
                t_action = "Reduce " + str(operation[1:])
                b = int(str(operation[1:]))
                p = self.production[b]  # 获取产生式
                productions.append(p)
                right = p.get("right")
                left = p.get("left")
                num = len(right)  # 产生式右部符号数
                for _ in range(num):
                    status_stack.pop()  # 弹出状态
                    output.pop()
                output.append(left)
                c = vn.index(left)
                s_top = status_stack[len(status_stack) - 1]
                status_stack.append(int(goto_table[s_top][c][0]))
                # print("{} --> {}".format(left, ' '.join(right)))
            elif operation == "acc":
                t_action = "Accept"
                # 语法分析完成
            else:
                t_action = "Error"
                raise Exception("语法分析错误")

            x.add_row([t_num, t_stack, t_output, t_input, t_action])
            if operation == "acc":
                break
        # ------------------------------------
        print("The analysis is as follows: ")
        # print(x)
        return list(reversed(productions))

    # ------------------------------------------------------

    def print_lr_table(self):
        lr_table = self.table
        action_table = lr_table[0]
        goto_table = lr_table[1]
        x = PrettyTable()
        vn = self.grammar.get("vn")
        vt = self.grammar.get("vt")
        len1 = len(vt)
        len2 = len(vn)
        len3 = len(action_table)
        x.field_names = ["state"] + vt + vn
        x.align["state"] = "r"

        for i in range(len3):
            ss = [i]
            for j in range(len1):
                if len(action_table[i][j]) > 0:
                    # ss.append(" ".join(action_table[i][j]))
                    ss.append(action_table[i][j][0])
                else:
                    ss.append("")

            for j in range(len2):
                if len(goto_table[i][j]) > 0:
                    ss.append(goto_table[i][j][0])
                else:
                    ss.append("")

            x.add_row(ss)
        print("ACTION and GOTO table are as follows: ")
        print(x)


if __name__ == "__main__":
    # parser.analysis_table(c)
    file_name = "rules3.l"
    text = utility.read_text(file_name)
    print(text)
    gr = GrammerReader(text)

    production = None
    grammar = None
    try:
        gr.parse()
    except Exception as result:
        print("Failed : %s" % result)
    else:
        production = gr.getProduction()
        grammar = gr.getGrammer()

    try:
        parser = Parser(production, grammar)
    except Exception as err:
        print(err)

    action = parser.table[0]
    goto = parser.table[1]
    print("action = ")
    print(action)
    print("goto = ")
    print(goto)
    parser.print_lr_table()
    text = ["1", "+", "1", "*", "1"]
    productions = parser.analyze(text)
    print(productions)
