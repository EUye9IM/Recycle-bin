from scan import *
from symbol_table import *
from prettytable import PrettyTable


class TreeParser:
    def __init__(self):
        """
        对7个做特殊处理
        <VariableDeclaration>
        <Declarations>
        <IfSentence>
        <WhileSentence>
        <ReturnSentence>
        <AssignSentence>
        <CallFunction>
        """
        self.paserMap = {
            "VariableDeclaration": self.T_variableDeclaration,
            "Declarations": self.T_FunctionDeclarations,
            "IfSentence": self.T_IfSentence,
            "WhileSentence": self.T_WhileSentence,
            "ReturnSentence": self.T_ReturnSentence,
            "AssignSentence": self.T_AssignSentence,
            # "CallFunction": self.T_CallFunction,
            "ArgumentDeclaration": self.T_ArgumentDeclaration,
            "Expression": self.T_Expression,
            "T_IDENTIFIER": self.T_IDENTIFIER,
            "T_INTEGER": self.T_INTEGER,
            "Block": self.T_Block,
        }
        self.depth = 0
        self.symTB = SymbolTable()
        self.tac = []  # 四元式
        self.dbgMsg = {}

        self.flags = {
            "in_Expression": False,
            "in_ArgumentDeclaration": False,
            "val": "_",
            "temp_num": 0,
        }

    def T_variableDeclaration(self, node: dict, tokenList: list, pos: int):
        id = tokenList[pos + 1].val
        info = {"id": id, "dep": self.depth, "type": "int"}
        name = str(self.depth) + "." + tokenList[pos + 1].val

        if self.symTB.ifExist(name):
            print(self.symTB)
            raise Exception(
                id
                + " mutidefine "
                + str(tokenList[pos].pos.ln)
                + ":"
                + str(tokenList[pos].pos.col)
            )
        self.symTB.add(Symbol(name, info))

        i = pos + 2
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)

        if tokenList[i].val == "=":
            # 赋值
            tac.append(["=", self.flags["val"], "_", id])

        return pos

    def T_FunctionDeclarations(self, node: dict, tokenList: list, pos: int):
        self.dbgMsg[str(len(self.tac))] = tokenList[pos + 1].val + "()"

        id = tokenList[pos + 1].val
        info = {
            "id": id,
            "dep": self.depth,
            "val": 0,
            "type": "func",
            "ent": len(self.tac),
        }
        name = str(self.depth) + "." + id
        # Todo 传参
        if self.symTB.ifExist(name):
            raise Exception(
                id
                + " mutidefine "
                + tokenList[pos].pos.ln
                + ":"
                + tokenList[pos].pos.col
            )
        self.symTB.add(Symbol(name, info))

        # i=pos+2
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)

        # if tokenList[i].type == "T_=":
        #     # 赋值
        #     tac.append(["=","t"+str(self.flags['temp_num'],"_",id)])
        return pos

    def T_IfSentence(self, node: dict, tokenList: list, pos: int):
        self.dbgMsg[str(len(self.tac))] = "if"
        # <T_IF><T_(><Expression><T_)><Block><T_ELSE><Block>
        # <T_IF><T_(><Expression><T_)><Block>;
        #  0     1     2           3    4       5       6      7
        if_type_1 = len(node["sons"]) == 7
        if_type_2 = not if_type_1

        true_jump = -1
        false_jump = -1
        final_jump = -1

        for i, n in enumerate(node["sons"]):
            if i == 4:
                self.tac[true_jump][3] = len(self.tac)  # true jump
            elif i == 6:
                self.dbgMsg[str(len(self.tac))] = "else"
                self.tac[false_jump][3] = len(self.tac)  # false jump -- if_type_1
            pos = self.visitNodes(n, tokenList, pos)
            if i == 2:
                false_jump = len(self.tac)
                self.tac.append(["jz", self.flags["val"], "_", "?"])
                true_jump = len(self.tac)
                self.tac.append(["j", "_", "_", "?"])
            elif i == 4 and if_type_1:
                final_jump = len(self.tac)
                self.tac.append(["j", "_", "_", "?"])  # final jump
            elif i == 4 and if_type_2:
                self.tac[false_jump][3] = len(self.tac)  # false jump -- if_type_2
            elif i == 6:
                self.tac[final_jump][3] = len(self.tac)  # final jump
        return pos

    def T_WhileSentence(self, node: dict, tokenList: list, pos: int):
        self.dbgMsg[str(len(self.tac))] = "while"
        # <T_WHILE><T_(><Expression><T_)><Block>;
        #   0      1       2         3     4
        ExpPos = -1
        false_jump = -1
        for i, n in enumerate(node["sons"]):
            if i == 2:
                ExpPos = len(self.tac)
            pos = self.visitNodes(n, tokenList, pos)
            if i == 2:
                false_jump = len(self.tac)
                self.tac.append(["jz", self.flags["val"], "_", "?"])
            elif i == 4:
                self.tac.append(["j", "_", "_", ExpPos])
                self.tac[false_jump][3] = len(self.tac)
        return pos

    def T_ReturnSentence(self, node: dict, tokenList: list, pos: int):
        self.tac.append(["ret", "_", "_", "_"])
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)

        return pos

    def T_AssignSentence(self, node: dict, tokenList: list, pos: int):
        name = ""
        for i, n in enumerate(node["sons"]):
            pos = self.visitNodes(n, tokenList, pos)
            if i == 1:
                name = self.flags["val"]
        self.tac.append(["=", self.flags["val"], "_", name])
        return pos

    # def T_CallFunction(self, node: dict, tokenList: list, pos: int):
    #     tokenList[pos].sen = "CallFunction"
    #     for n in node["sons"]:
    #         pos = self.visitNodes(n, tokenList, pos)

    #     return pos

    def T_ArgumentDeclaration(self, node: dict, tokenList: list, pos: int):
        self.flags["in_Expression"] = True
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)
        self.flags["in_Expression"] = False
        return pos

    def T_Expression(self, node: dict, tokenList: list, pos: int):
        inner_Expression = self.flags["in_Expression"]
        if not inner_Expression:
            self.flags["in_Expression"] = True
            self.flags["temp_num"] = 0

        if node["sons"][0]["name"] != "Item":
            # <Expression><Relop><Item>
            # exp
            pos = self.visitNodes(node["sons"][0], tokenList, pos)
            temp1 = self.flags["val"]
            relop = tokenList[pos].val
            pos = self.visitNodes(node["sons"][1], tokenList, pos)
            pos = self.visitNodes(node["sons"][2], tokenList, pos)
            temp2 = self.flags["val"]

            self.flags["val"] = "t" + str(self.flags["temp_num"])
            self.flags["temp_num"] = self.flags["temp_num"] + 1
            # 赋值
            self.tac.append([relop, temp1, temp2, self.flags["val"]])
        else:
            for n in node["sons"]:
                pos = self.visitNodes(n, tokenList, pos)

        if not inner_Expression:
            self.flags["in_Expression"] = False
        return pos

    def T_IDENTIFIER(self, node: dict, tokenList: list, pos: int):
        if self.flags["in_Expression"]:
            self.flags["val"] = str(self.depth) + "." + tokenList[pos].val
            self.symTB.update(
                Symbol(
                    str(self.depth + 1) + "." + tokenList[pos].val,
                    {"id": tokenList[pos].val, "dep": self.depth + 1, "type": "int"},
                )
            )
            return pos + 1

        for i in range(self.depth, -1, -1):
            if self.symTB.ifExist(str(i) + "." + tokenList[pos].val):
                self.flags["val"] = str(i) + "." + tokenList[pos].val
                return pos + 1
        raise Exception(
            tokenList[pos].val
            + " never defineded "
            + str(tokenList[pos].pos.ln)
            + ":"
            + str(tokenList[pos].pos.col)
        )
        return pos + 1

    def T_INTEGER(self, node: dict, tokenList: list, pos: int):
        self.flags["val"] = tokenList[pos].val
        # print("<%s> :  %s" % (node['name'], tokenList[pos].val))
        return pos + 1

    def T_Block(self, node: dict, tokenList: list, pos: int):
        self.depth = self.depth + 1
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)
        """同时要删除所有在里面的变量"""
        self.symTB.removeWhere(lambda x: x.info["dep"] >= self.depth)
        self.depth = self.depth - 1
        return pos

    def visitNodes(self, node: dict, tokenList: list, pos: int = 0):
        """遍历树结构的算法
        node: 节点
        node 表示根节点
                node["name"] 为本节点名称
                node["sons"] 为列表，里面是子节点
        tokenList token 列表
        pos       第几个token
        """
        if node["name"] == "":
            return pos

        if node["name"] in self.paserMap:
            return self.paserMap[node["name"]](node, tokenList, pos)

        # 是token
        if len(node["sons"]) == 0:
            # print("<%s> :  %s" % (node['name'], tokenList[pos].val))
            return pos + 1

        # 节点名
        # print("<%s>" % node["name"])

        # 递归向下
        for n in node["sons"]:
            pos = self.visitNodes(n, tokenList, pos)
        return pos

    def showResult(self):
        for i, v in enumerate((self.tac)):
            if str(i) in self.dbgMsg:
                print(i, v, "\t<--", self.dbgMsg[str(i)])
            else:
                print(i, v)

    # 格式化打印四元式
    def printQuad(self):
        x = PrettyTable()
        x.field_names = ['address', 'op', 'arg1', 'arg2', 'result']
        for i, qdr in enumerate(self.tac):
            x.add_row([i] + qdr)
        print(x)


def test(rootNode: dict, tokens):
    x

# if __name__ == "__main__":
#     import utility
#     from grammar_reader import GrammerReader
#     from top_down_analysis import parse
#     rule_file_name = "rules3.l"
#     code_file_name = "input.cpp"

#     code_scan = Scanner(code_file_name)
#     tokens = code_scan.get_token_list()

#     code_text = ""
#     for t in tokens:
#         code_text=code_text+t.type

#     print( code_text)

#     text = utility.read_text(rule_file_name)
#     gr = GrammerReader(text)
#     # production = None
#     # grammar = None
#     try:
#         gr.parse()
#     except Exception as result:
#         print("Failed : %s" % result)


# parser = Parser(production, grammar)


# tp = TreeParser()
# tp.visitNodes(rootNode, tokens)
# tp.showResult()
