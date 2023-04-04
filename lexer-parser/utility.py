# ------------------------------------------------
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: Anakin
# Function: 公用函数
# ------------------------------------------------

# 读取文本函数
def read_text(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()
        return text


# 列表打印优化
def prettytable_list(l: list, max_len=10):
    content = None
    if len(l) > max_len:
        content = (
            " ".join(l[: int(max_len / 2)])
            + "......"
            + " ".join(l[-int(max_len / 2) :])
        )
    else:
        content = " ".join(l)
    return content


# -------------------------------------------------------
# 计算字符 FIRST 集
"""
1) 如果 X 是一个终结符号，那么 FIRST(X) = X;
2) 如果 X 是一个非终结符号，且有产生式X→a..., a∈VT,
   则把 a 加入到FIRST(X)中，若有 X→ε，则把ε加入FIRST(X);
3) 如果 X 是一个非终结符号，且X→Y..., Y ∈ VN, 
   则把 FIRST (Y) - {ε} 加到 FIRST(X) 中;                    
   若X→Y1Y2...Yk, Y1, Y2, ..., Yi-1 ∈ VN, ε∈FIRST (Yj)，
   则把 (1<= j <= i -1) FIRST (Yi) - {ε}加到 FIRST(X) 中;
   特别地，若 ε∈FIRST(Yj)(1<=j<=k)，则 ε∈FIRST(X).
*  为后续方便，将'$'归为终结符号的一种
"""


def single_first(production, grammar):
    epsilon = ""  # 标记 epsilon 为 ''
    vn = grammar["vn"]
    vt = grammar["vt"]
    first = {}
    # 处理终结符号
    for i in vt:
        first[i] = [i]
    # 初始化非终结符号
    for i in vn:
        first[i] = []
    # --------------------------------------------------
    flag = True
    while flag:
        flag = False
        for p in production:
            left = p["left"]
            right = p["right"]
            if len(right) == 0:
                continue
            if left in vn:  # 左边为非终结字符
                if right[0] in vt:  # X→a..., a∈VT
                    if right[0] not in first[left]:
                        first[left].append(right[0])
                        flag = True  # 改变
                # -------------------------------
                elif right[0] == epsilon:
                    if epsilon not in first[left]:
                        first[left].append(epsilon)
                        flag = True  # 改变
                # -------------------------------
                elif right[0] in vn:  # X→Y..., Y ∈ VN
                    len1 = len(first[left])
                    # 复制列表，防止左递归重复
                    first_right = first[right[0]][:]
                    first[left].extend(x for x in first_right if x != epsilon)
                    first[left] = list(set(first[left]))  # 去重复元素
                    len2 = len(first[left])
                    if len1 != len2:  # 列表已经修改
                        flag = True  # 改变
                    # --------------------------------
                    # X→Y1Y2...Yk
                    i = 1
                    while i < len(right):
                        if epsilon not in first[right[i - 1]]:
                            break
                        len1 = len(first[left])
                        first_right = first[right[i]][:]
                        first[left].extend(x for x in first_right if x != epsilon)
                        first[left] = list(set(first[left]))  # 去重复元素
                        len2 = len(first[left])
                        if len1 != len2:  # 列表已经修改
                            flag = True  # 改变
                        # -------------------------------
                        i += 1
                    if i == len(right):
                        if (
                            epsilon not in first[left]
                            and epsilon in first[right[i - 1]]
                        ):
                            first[left].append(epsilon)
                            flag = True  # 改变
                # -----------------------------------
            # ---------------------------------------
            # -------------------------------------------
            # 终结字符已经处理完成，且正常情况下左边不会有终结符
            else:
                raise Exception("终结符出现在产生式左边！")
    # -----------------------------------------------
    # 退出 while 循环
    return first


# ----------------------------------------------------
# 计算字符串的 FIRST 集
"""
对于符号串α= X1X2...Xn，构造 FIRST (α) 
1） 置 FIRST(α) = FIRST (X1) - {ε};
2） 若对所有的 Xj ,1<=j<=i-1, ε∈FIRST (Xj), 则把FIRST(Xi) -{ε}加到FIRST(α)中；
3） 若对所有的 Xj ,1<=j<=n, ε∈FIRST (Xj), 则把ε加到FIRST(α)中。
"""


# first_table 为单字符 FIRST 表，w 为字符串集


def multi_first(first_table: dict, w: list):
    if len(w) == 0:
        raise Exception("字符串为空")
    elif len(w) == 1:
        return first_table[w[0]]

    epsilon = ""
    first = []
    first_w = first_table[w[0]][:]
    first.extend(x for x in first_w if x != epsilon)
    i = 1
    while i < len(w):
        if epsilon not in first_table[w[i - 1]]:
            break

        first_w = first_table[w[i]][:]
        first.extend(x for x in first_w if x != epsilon)
        first = list(set(first))
        i += 1
    # ----------------------------------------------
    if i == len(w):
        if epsilon not in first and epsilon in first_table[w[i - 1]]:
            first.append(epsilon)
    # ----------------------------------------------
    return first
