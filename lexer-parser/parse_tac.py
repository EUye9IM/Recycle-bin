# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Function: three address code parser
from grammar_reader import GrammerReader
from tac import *
from scan import Token
from scan import Scanner
from tree import makeTree
from symbol_table import Symbol, SymbolTable
from tree_parser import TreeParser
from parser_ import Parser
import utility


class Sentence:
    WHILE = "WhileSentence"
    IF = "IfSentence"
    ASSIGN = "AssignSentence"
    VAR_DECLARE = "VariableDeclare"
    RETURN = "ReturnSentence"
    FUN_DECLARE = "FunctionDeclare"
    CALL = "CallFunction"


depth = 0


def track_depth(func):
    """
    追踪深度数值
    trackDepth increments a depth counter as soon as a parsing function is
    called, and decrements that counter when the function has ended.
    This is vital to our depth-based error recovery.
    """

    def wrapper(classInstance, input=None):
        global depth
        if classInstance.printTree:
            print(depth, "\t", "    " * depth, "Opening:", func.__name__)
        depth += 1
        value = func(classInstance, input)
        depth -= 1
        if classInstance.printTree:
            print(depth, "\t", "    " * depth, "Closing:", func.__name__)
        return value

    return wrapper


# 三地址码分析生成
class TacParse:
    def __init__(self, token_list):
        """
        self.tac 为 InterCode 的实例对象
        self.err_list 记录错误信息
        self.token_list 为token列表
        self.index 为索引值，对应于 token_list
        """
        self.code = InterCode()
        self.err_list = []
        self.token_list = token_list
        self.index = -1
        self.found_error = False
        self.current_token: Token = None  # 当前分析的 token,可能和 index 重复，暂时保留
        self.temp_list = []  # 临时表
        self.depth = 0  # 记录深度
        self.symbol_table = SymbolTable()  # 符号表，先做保留
        self.arithmetic_stack: list = []  # 算术表达式栈

    # 分析程序入口，获取 token,分析
    def parse(self):
        self.next_token()
        self.program()

    # 进行程序分析，根据不同的句子类型进行不同的处理
    def program(self):
        sen_type = self.current_token.sen
        if sen_type == Sentence.VAR_DECLARE:  # 声明语句
            self.var_declare_exp()
        elif sen_type == Sentence.ASSIGN:  # 赋值语句
            self.assign_exp()
        elif sen_type == Sentence.WHILE:  # while 语句
            self.while_exp()
        elif sen_type == Sentence.IF:  # if 语句
            self.if_exp()
        elif sen_type == Sentence.RETURN:  # return 语句
            # self.return_exp()
            pass

        # 在存在 token 的情况下继续递归调用分析
        if self.next_token():
            self.program()

    # 获取 token 类型
    def get_token_type(self):
        return self.current_token.type

    def get_quad_address(self):
        return len(self.code.quad_list) - 1

    # 回退操作，token 后退一个
    def back_token(self):
        self.index = self.index - 1
        self.current_token = self.token_list[self.index]

    # 获取下一个 token 值
    def next_token(self):
        # 目前通过 index 的方式获取 token，后续进行完善
        self.index = self.index + 1
        if self.index >= len(self.token_list):
            print("token is end")
            return False
        self.current_token = self.token_list[self.index]
        return True

        # self.current_token = self.token_list[self.index]
        # if self.get_token_type() == 'T_IDENTIFIER':
        #     # token 为标识符
        #     entry = self.symbol_table.lookup(self.current_token.val)
        #     if entry == -1:  # -1 意味着没有找到
        #         num = self.symbol_table.insert(self.current_token.val, self.current_token.type)
        #         self.current_token.set_sym_tab_entry(num)
        #     else:  # 发现 token，设置入口
        #         self.current_token.set_sym_tab_entry(entry)
        #
        # elif self.get_token_type() == 'T_INTEGER':
        #     # token 为整形数字（目前不处理其他类型数字）
        #     entry = self.symbol_table.lookup(self.current_token.val)
        #     if entry == -1:  # -1 意味着没有找到
        #         num = self.symbol_table.insert(self.current_token.val, self.current_token.type)
        #         self.current_token.set_sym_tab_entry(num)
        #     else:  # 发现 token，设置入口
        #         self.current_token.set_sym_tab_entry(entry)
        #
        # return True

    def match(self):

        pass

    # 语句
    def sentence(self):

        pass

    """
    # 变量声明,入口时 token 应指向变量类型
    def var_declare(self):
        if self.get_token_type() == 'T_INT':
            # 目前的文法不允许 int a,b; 声明，只可以单个声明

            self.next_token()
            self.var_define()
            if self.get_token_type() != 'T_;':
                raise Exception("Error: missing keyword ';'")
            self.next_token()

        pass

    # 分析变量的定义，加入符号表
    def var_define(self):
        if self.get_token_type() == 'T_IDENTIFIER':  # 标识符
            if not self.symbol_table.lookup(self.current_token):
                # 不在符号表中，添加
                self.symbol_table.push_back(self.current_token)
            self.next_token()
            if self.get_token_type() == 'T_=':  # 声明与赋值语句在一起
                self.back_token()  # 回退 token
                self.assign_exp()  # 分析赋值语句
    """

    # 变量声明
    def var_declare_exp(self):
        # 语句形式：
        # T_INT T_IDENTIFIER T_= Expression T_;
        # T_INT T_IDENTIFIER T_;
        #
        # 主要是添加入符号表
        # 符号目前一共三个信息：名字，作用域（深度），值
        # 目前符号表结构为：
        #  name              info
        #  <id,depth>  {'id':id,'dep':depth,'val':value}
        # 目前主要起一个防止变量重定义的作用
        # 不用生成四元式

        # 获得一个表示 id 的 token
        state = State()  # 不知道干什么用
        self.next_token()  # 指向id
        if self.get_token_type() != "T_IDENTIFIER":
            # 缺少 “id” 错误
            raise Exception("Error: missing T_IDENTIFIER")

        var_info = {
            "id": self.current_token.val,
            "dep": self.current_token.depth,
            "val": 0,
        }
        name = "<" + var_info["id"] + "," + var_info["dep"] + ">"

        # 重定义检查
        if self.symbol_table.ifExist(name):
            err_list.append("重定义!" + self.index + var_info["id"])
        else:
            self.symbol_table.add(Symbol(name, info))

        if self.self.token_list[self.index + 1].type == "T_=":
            self.assign_exp()  # 赋值不知道怎么操作
        elif self.self.token_list[self.index + 1].type != "T_;":
            raise Exception("Error: missing keyword ';'")

        self.next_token()  # 指向 T_;

        return state

    # 类型定义
    def type_define(self):
        pass

    # 赋值语句
    def assign_exp(self):
        state = State()
        state.code_begin = self.get_quad_address()
        # 首先需要一些错误处理判断
        # ...
        # token 入栈
        self.arithmetic_stack.append(self.current_token.val)
        self.next_token()
        if self.get_token_type() != "T_=":
            # 缺少 “=” 错误
            raise Exception("Error: missing '='")

        op = "="  # 赋值符号记录
        state = self.arithmetic_exp()  # 进入算术表达式分析
        # 赋值四元式
        if len(self.arithmetic_stack) >= 2:
            arg1 = self.arithmetic_stack.pop()
            arg2 = self.arithmetic_stack.pop()
            self.code.generate(op, arg1, None, arg2)

        return state

    # 算术表达式，入口时 token 位于算术表达式第一项，比如“=”
    def arithmetic_exp(self):
        # 分析每一项
        state = self.term_exp()
        type = self.get_token_type()
        while type == "T_+" or type == "T_-":
            op = type[2]  # 记录操作符
            state = self.term_exp()  # 分析每一项
            if len(self.arithmetic_stack) >= 2:  # 生成四元式
                arg1 = self.arithmetic_stack.pop()
                arg2 = self.arithmetic_stack.pop()
                temp_var = self.code.new_temp()
                self.code.generate(op, arg2, arg1, temp_var)
                self.arithmetic_stack.append(temp_var)
            # 切记不要忘记刷新 type 的值
            type = self.get_token_type()

        return state

    # 对一个单项式的分析，入口时当前 token 是项的前一个
    def term_exp(self):
        state = self.factor()  # 对项进行分析
        self.next_token()  # 下一个 token 应该为运算符 */
        type = self.get_token_type()
        if type == "T_*" or type == "T_/":  # 分析乘除所产生的项
            op = type[2]  # 获取运算符
            state = self.term_exp()  # 递归调用，分析单项式
            # 栈中获取操作数字
            arg1 = self.arithmetic_stack.pop()
            arg2 = self.arithmetic_stack.pop()
            temp_var = self.code.new_temp()
            # 生成四元式
            self.code.generate(op, arg2, arg1, temp_var)
            # 写入乘除的结果的中间变量
            self.arithmetic_stack.append(temp_var)

        return state

    # 对因子的分析，应该为原子化了，入口 token 为前一个，需要 next 处理
    def factor(self):
        state = State()
        state.code_begin = self.get_quad_address()

        self.next_token()
        type = self.get_token_type()
        # 下面对各种 token 类型进行分析
        if type == "T_INTEGER":  # 数字类型
            self.arithmetic_stack.append(self.current_token.val)
        elif type == "T_IDENTIFIER":  # 标识符类型
            # 首先进行标识符的检查
            # ...
            self.arithmetic_stack.append(self.current_token.val)

        elif type == "T_(":  # 遇见‘（’
            state = self.arithmetic_exp()  # 分析括号中的算术表达式
            if self.get_token_type() != "T_)":  # 缺少右括号
                raise Exception("Error: without ')'")
        else:  # 非法 token
            raise Exception("Error: unexpected token")

        return state

    # bool 表达式处理
    def bool_exp(self):
        state = self.bool_term()
        # 目前处理的程序不包括与或非等布尔运算，暂不考虑
        # 只处理关系运算符
        return state

    # bool 式中单项式的处理
    def bool_term(self):
        state = self.bool_factor()
        # 没有 and 运算，直接返回状态即可
        return state

    # bool 式中因子的处理
    def bool_factor(self):
        state = State()
        state.code_begin = self.get_quad_address()
        type = self.get_token_type()
        if type == "T_INTEGER":
            self.index = self.index - 1  # 回退一个 token 进行算术表达式计算
            state = self.arithmetic_exp()
            arg1 = self.arithmetic_stack.pop()
            op = self.get_token_type()[2:]  # 切片获取操作符
            if op in [">", ">=", "==", "<", "<=", "!="]:
                state = self.arithmetic_exp()  # 计算比较符右边的表达式
                arg2 = self.arithmetic_stack.pop()
                # 推入四元式
                op = "j" + op
                self.code.generate(op, arg1, arg2, "-")
                self.code.generate("jump", "-", "-", "-")
            else:
                raise Exception("Error: incomplete expression")

        elif type == "T_IDENTIFIER":
            # 首先需要进行一些分析，标识符是否存在等判断
            # ...
            # 如果正确，进行分析

            pass

        elif type == "T_(":  # 左括号情形
            self.next_token()
            self.bool_exp()
            if self.get_token_type() != "T_)":
                raise Exception("Error: without ')'")
            self.next_token()  # 进入下一个 token 分析

        pass

    # while 语句
    def while_exp(self):
        pass

    # if 语句
    def if_exp(self):
        pass

    # 复合语句
    def sentence_list(self):
        pass


if __name__ == "__main__":
    rule_file_name = "rules2.l"
    code_file_name = "input2.cpp"

    code_scan = Scanner(code_file_name)
    token_list = code_scan.get_token_list()
    text = utility.read_text(rule_file_name)
    print("读取文本完成，生成产生式中......")
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

    parser = Parser(production, grammar)
    print("语法分析器完成.")
    print("正在传入 token 流......")
    code_text = []
    for t in token_list:
        code_text.append(t.type)
    # parser.print_lr_table()
    productions = parser.analyze(code_text)

    node = {}
    makeTree(productions, node)

    tp = TreeParser()
    tp.visitNodes(node, token_list)

    iparse = TacParse(token_list)
    iparse.parse()
    iparse.code.print_quads()
