from top_down_analysis import *


class GrammerReader:
    def __init__(self):
        self.__text = ""
        self.__production = []
        self.__grammer = {"vt": [], "vn": []}
        self.__entrance = ""

    def __init__(self, text: str):
        self.__text = text
        self.__production = []
        self.__grammer = {"vt": [], "vn": []}
        self.__entrance = ""
        self.record = {}

    def __checkError(self, ret: list):
        retStr = ""
        if ret[0] < 0:
            retStr += "Location = %d.\n" % ret[2]
            b = ret[2]
            e = ret[2]
            while b > 0 and self.__text[b - 1] != "\n":
                b = b - 1
            while e < len(self.__text) - 1 and self.__text[e + 1] != "\n":
                e = e + 1
            retStr += "Expect : `%s` but read '%s'\n" % (ret[1], self.__text[ret[2]])
            retStr += 'Near : "%s".\n' % self.__text[b : e + 1]
            retStr += ("%" + str(ret[2] - b + 10) + "s") % "^\n"
            raise Exception(retStr)

    def __parseGrammer(self, productionRules: dict):
        """分析文本
        text   待分析文本
        productionRules 输出 文法规则
            name : 字符串。（非）终结符名称
            rules : 二位字符串数组。生成规则
            individualCharacter : 单字。在之后的递归解析中不忽略空白字符
            illegalStrList : 非法字符串集：专门处理关键字。
        """

        def str2list(string: str):
            s = []
            for i in string:
                s.append([str(i)])
            return s

        self.record = {}
        productionRules.clear()
        # -------------------------------语法-----------------------------------
        addRule(
            productionRules,
            "RulesFile",
            [
                ["Annotation", "SingleRule", "RulesFile"],
                ["Annotation", "SingleRule", "Annotation"],
            ],
        )

        addRule(
            productionRules,
            "SingleRule",
            [["Item1", "::=", "RightPart", ";"], ["Item1", "::=", "RightPart", ";"]],
        )
        addRule(productionRules, "RightPart", [["Items", "|", "RightPart"], ["Items"]])
        addRule(productionRules, "Items", [["Item", "Items"], ["Item"]])
        addRule(productionRules, "Item", [["Item0"], ["Item1"], ["EPS"]])
        addRule(productionRules, "Item0", [["<", "ID", ">", "*"]])
        addRule(productionRules, "Item1", [["<", "ID", ">"]])
        addRule(productionRules, "EPS", [["<", "EPSILON", ">"]])
        # 标识符
        addRule(
            productionRules,
            "ID",
            [["_", "ASCII", "ID"], ["_", "ASCII"], ["ASCII~>", "ID"], ["ASCII~>"]],
            True,
            ["EPSILON"],
        )
        # 注释
        addRule(
            productionRules,
            "Annotation",
            [
                ["Annotation_0", "Annotation"],
                ["Annotation_1", "Annotation"],
                ["Annotation_0"],
                ["Annotation_1"],
                [""],
            ],
        )
        addRule(
            productionRules,
            "Annotation_0",
            [["//", "Annotation_2", "\n"], ["//", "Annotation_2"]],
            True,
        )
        addRule(productionRules, "Annotation_2", [["ASCII~n", "Annotation_2"], [""]])
        addRule(productionRules, "Annotation_1", [["/*", "Annotation_3"]], True)
        addRule(
            productionRules,
            "Annotation_3",
            [["ASCII~*", "Annotation_3"], ["*", "ASCII~/", "Annotation_3"], ["*/"]],
        )

        addRule(
            productionRules,
            "ASCII",
            str2list(
                "\t \n!|\"#$%&'()*+,-./0123456789:;<=>?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )
        addRule(
            productionRules,
            "ASCII_no_blank",
            str2list(
                "!|\"#$%&'()*+,-./0123456789:;<=>?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )
        addRule(
            productionRules,
            "ASCII~>",
            str2list(
                "!|\"#$%&'()*+,-./0123456789:;<=?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )
        # ASCII不带换行
        addRule(
            productionRules,
            "ASCII~n",
            str2list(
                "\t !|\"#$%&'()*+,-./0123456789:;<=>?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )

        # ASCII不带*
        addRule(
            productionRules,
            "ASCII~*",
            str2list(
                "\t\n !|\"#$%&'()+,-./0123456789:;<=>?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )

        # ASCII不带/
        addRule(
            productionRules,
            "ASCII~/",
            str2list(
                "\t\n !|\"#$%&'()*+,-.0123456789:;<=>?@AaBbCcDdEeFfGgHhIi"
                + "JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz[\\]^_`}{~"
            ),
            True,
        )
        # 开始分析
        resetErrorPos()
        ret = parse(
            "RulesFile", productionRules, self.__text, 0, len(self.__text), self.record
        )
        errpos = getErrorPos()
        errmsg = getErrorMsg()
        if errpos != len(self.__text):
            ret = -1
            return ret, errmsg, errpos

        productionRules.clear()
        extraRules = []
        sentencePointer = self.record
        while sentencePointer["sons"][1]["name"] == "SingleRule":
            sentence = sentencePointer["sons"][1]
            #                     item1/pro   <   ID   >
            #                                 0    1
            leftItem = sentence["sons"][0]["sons"][1]
            leftName = self.__text[leftItem["begin"] : leftItem["end"]].strip()

            if self.__entrance == "":
                self.__entrance = leftName
            #                 left ::=  right
            #                  0    1    2
            rightPart = sentence["sons"][2]
            rules = []

            itemsPointer = rightPart
            #                       items
            while itemsPointer["sons"][0]["name"] == "Items":
                items = itemsPointer["sons"][0]
                oneRule = []

                itemPointer = items
                while itemPointer["sons"][0]["name"] == "Item":
                    #                   item           itemx
                    item = itemPointer["sons"][0]["sons"][0]
                    itemName = self.__text[
                        item["sons"][1]["begin"] : item["sons"][1]["end"]
                    ].strip()

                    if itemName == "EPSILON":
                        itemName = ""
                    elif item["name"] == "Item0":
                        extraName = itemName + "'"
                        if not itemName in extraRules:
                            extraRules.append(itemName)
                            addRule(
                                productionRules,
                                extraName,
                                [[extraName, itemName], [itemName], [""]],
                            )
                        itemName = extraName

                    oneRule.append(itemName)

                    if len(itemPointer["sons"]) < 2:
                        break
                    #                    ["Item", "Items"]
                    #                      0          1
                    itemPointer = itemPointer["sons"][1]
                rules.append(oneRule)
                if len(itemsPointer["sons"]) < 3:
                    break
                #                   ["Items", "|", "RightPart"]
                #                      0       1       2
                itemsPointer = itemsPointer["sons"][2]

            addRule(productionRules, leftName, rules)
            if (
                len(sentencePointer["sons"]) < 3
                or sentencePointer["sons"][2]["name"] != "RulesFile"
            ):
                break
            sentencePointer = sentencePointer["sons"][2]

        # if(not "PROGRAMME" in productionRules.keys()):
        #     return -1, "Rule of PROGRAMME", 0
        return 0, "", 0

    # 函数名字没想好
    def __convert(self, productionRules: dict):
        """
        输入 productionRules
        输出 production， grammar
        """
        production = []
        grammar = {"vn": [], "vt": []}
        for i in productionRules:
            leftName = productionRules[i].name
            rights = productionRules[i].rulesList
            for rightList in rights:
                production.append({"left": leftName, "right": rightList})
                if not leftName in grammar["vn"]:
                    grammar["vn"].append(leftName)

        for i in production:
            for j in i["right"]:
                if not (j in grammar["vn"] or j in grammar["vt"]):
                    grammar["vt"].append(j)
        return production, grammar

    def setGrammer(self, text: str):
        self.__text = text

    def parse(self):
        out = {}
        self.__checkError(self.__parseGrammer(out))
        self.__production, self.__grammer = self.__convert(out)

    def getProduction(self):
        """
        获取产生式列表
        production type: list[dict{},...]
        eg: A->BC|D
        form: [{'left': 'A', 'right': ['B','C']}, {'left': 'A', 'right': ['D']}]
        """
        return self.__production

    def getGrammer(self):
        """
        获取符号列表
        grammar type: dict{"vt": [], "vn": []}
        eg: {"vt": ['a', 'b', ...], "vn": ['A', 'B', ...]}
        """
        return self.__grammer

    def getEntrance(self):
        return self.__entrance


# test
if __name__ == "__main__":
    text = """
// zhu chang xu      han shu sheng ming          bian liang sheng ming
<PROGRAMME>    ::= <Declarations><PROGRAMME> | <VariableDeclaration><PROGRAMME> | <EPSILON>;

// han shu sheng ming
<Declarations> ::=
    <Type> <T_IDENTIFIER> <T_(> <ArgumentDeclaration> <T_)> <Block> |
    <Type> <T_IDENTIFIER> <T_(> <ArgumentDeclaration> <T_)> <T_;>;

// lei xing
<Type> ::= <T_INT> | <T_VOID>;

// can shu
<ArgumentDeclaration> ::= <Argument_,>* <T_INT><T_IDENTIFIER> | <T_INT><T_IDENTIFIER>|<T_VOID>  | <EPSILON>;
<Argument_,> ::= <T_INT><T_IDENTIFIER> <T_,>;

// { } huo zhe dan ju 
<Block> ::= <T_{> <Sentences> <T_}>|<Sentence>;

// xx;
<Sentences> ::= <Sentence><Sentence>*;
<Sentence> ::= <IfSentence> | <WhileSentence> | <ReturnSentence> | <VariableDeclaration> | <AssignSentence>;

// int i=0;/int i;
<VariableDeclaration> ::=
    <T_INT><T_IDENTIFIER><T_=><Expression><T_;> |
    <T_INT><T_IDENTIFIER><T_;>;

// i = 0
<AssignSentence> ::= <T_IDENTIFIER><T_=><Expression><T_;>;
 
 // return;
<ReturnSentence> ::= <T_RETURN><Expression><T_;> | <T_RETURN><T_;>;
<WhileSentence> ::= <T_WHILE><T_(><Expression><T_)><Block>;

<IfSentence> ::= <T_IF><T_(><Expression><T_)><Block><T_ELSE><Block> | <T_IF><T_(><Expression><T_)><Block>;
<Expression> ::= <Item><Relop><Expression> | <Item>;
<Item> ::= <T_(><Expression><T_)> | <T_INTEGER> | <CallFunction> | <T_IDENTIFIER>;
<CallFunction> ::= <T_IDENTIFIER><T_(><ArgumentList><T_)>;
<ArgumentList> ::= <Expression><T_,><ArgumentList> | <Expression><EPSILON>;
<Relop> ::= <T_==> | <T_>=> | <T_<=> | <T_!=> | <T_>> | <T_<> | <T_+> | <T_-> | <T_*> | <T_/>;
    """

    gr = GrammerReader(text)
    # 也可以
    # gr = GrammerReader
    # gr.setGrammer(text)

    try:
        gr.parse()
    except Exception as result:
        print("Faild : %s" % result)
    else:
        print("Success.")
        print(gr.getProduction())
        print(gr.getGrammer())
        print(gr.getEntrance())
