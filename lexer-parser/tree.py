def makeTree(productions: list, tree: dict, pPos: int = 0):
    if pPos >= len(productions):
        return pPos
    oldPos = pPos
    if pPos == 0:
        tree["name"] = productions[pPos]["left"]
        tree["sons"] = []
    elif tree["name"] != productions[pPos]["left"]:
        return pPos
    pPos = pPos + 1
    for i in productions[oldPos]["right"]:
        tree["sons"].append({"name": i, "sons": []})
    for i in range(len(productions[oldPos]["right"]) - 1, -1, -1):
        pPos = makeTree(productions, tree["sons"][i], pPos)
    return pPos


def printTree(
    node: dict,
    tokenList: list,
    pos: int = 0,
    indent: list = [],
    level: int = 0,
    final_node: bool = True,
):
    """打印树结构的算法
    node: 节点
    node 表示根节点
        node["name"] 为本节点名称
        node["sons"] 为列表，里面是子节点
    tokenList token 列表
    pos       第几个token
    indent: 记录了节点之前需要打印的信息
    level: 记录了节点的层级
    final_node: node 是否是最后一个节点（i.e. 没有下一个 sibling 了）
    """
    if node["name"] == "":
        return pos
    # print(node['name'])
    # 每行之前的树枝部分
    for i in range(level):
        print(indent[i], end="")
    if final_node:
        print("\-- ", end="")
    else:
        print("|-- ", end="")
    # 提升鲁棒性：解析错误有时会留一个空的节点
    # if(len(node) == 0):
    # return

    # 是token
    if len(node["sons"]) == 0:
        print("<%s> :  %s" % (tokenList[pos].type, tokenList[pos].val))
        return pos + 1

    # 节点名
    # print("<>")
    print("<%s>" % node["name"])

    # 递归向下
    cnt = len(node["sons"])
    for i, n in enumerate(node["sons"]):
        c = "    " if final_node else "|   "
        indent.append(c)
        last_node = i == cnt - 1
        pos = printTree(n, tokenList, pos, indent, level + 1, last_node)
        del indent[-1]
    return pos
