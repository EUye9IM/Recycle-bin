from scan import Token

ErrorPos = 0
ErrorMsg = ""
ErrorTempFlag = True


class ProductionRule:
    "生成式"

    def __init__(
        self,
        name: str,
        rulesList: list,
        individualCharacter: bool = False,
        illegalStrList: list = [],
    ):
        """
        name : 字符串。（非）终结符名称
        rules : 二位字符串数组。生成规则
        individualCharacter : 单字。在之后的递归解析中不忽略空白字符
        illegalStrList : 非法字符串集：专门处理关键字。
        """
        self.name = name
        self.rulesList = rulesList
        self.individualCharacter = individualCharacter
        self.illegalStrList = illegalStrList


def parse(
    name: str,
    productionRule: dict,
    text: str,
    pos: int,
    end: int,
    record: dict,
    ignoreBlank: bool = True,
):
    """
    分析文本
    self   : 当前节点名字
    rules  : 生成式字典
    text   : 待分析文本
    pos    : 开始位置
    end    : 结束位置
    record : 递归过程记录

    返回值 : 失败返回 -1 成功返回该节点末尾位置（一般而言end+1）
    """
    global ErrorPos
    global ErrorMsg
    global ErrorTempFlag

    # 记录自己节点信息
    record["name"] = name
    record["begin"] = pos
    record["end"] = end
    record["sons"] = []
    if pos > end:
        return -1

    # 去除空白字符
    if ignoreBlank == True:
        while pos < end and text[pos] in [" ", "\t", "\n"]:
            pos = pos + 1

    # 记录错误信息
    if pos >= ErrorPos:
        ErrorPos = pos
        if (
            pos == ErrorPos
            and name in productionRule
            and productionRule[name].individualCharacter
            and ignoreBlank
        ):
            ErrorMsg = name
        if (
            pos == ErrorPos
            and name not in productionRule
            and ignoreBlank
            and not ErrorTempFlag
        ):
            ErrorMsg = name

    # 自己是终结符
    if not name in productionRule:
        if text.startswith(name, pos):
            record["end"] = pos + len(name)
            pos += len(name)
            return pos
        return -1
    if productionRule[name].individualCharacter == True:
        ignoreBlank = False

    # 遍历规则
    for rule in productionRule[name].rulesList:
        # 清空上一次循环的遍历记录
        record["sons"] = []
        newPos = pos

        notFound = False
        # 逐一匹配
        for index, j in enumerate(rule):
            ErrorTempFlag = productionRule[name].individualCharacter
            record["sons"].append({})
            newPos = parse(
                j, productionRule, text, newPos, end, record["sons"][index], ignoreBlank
            )
            # 匹配失败
            if newPos < 0:
                notFound = True
                break
        # 匹配成功
        if notFound == False:
            record["end"] = newPos
            for i in productionRule[name].illegalStrList:
                if text[pos:newPos].strip() == i:
                    notFound = True
                    break
        if notFound == False:
            return newPos
    return -1


# 向 productionRules 中添加规则


def addRule(
    productionRules: dict,
    name: str,
    rulesList: list,
    individualCharacter: bool = False,
    illegalStrList: list = [],
):
    productionRules[name] = ProductionRule(
        name, rulesList, individualCharacter, illegalStrList
    )


# resetErrorPos


def resetErrorPos():
    global ErrorPos
    ErrorPos = 0


# getErrorPos


def getErrorPos():
    global ErrorPos
    return ErrorPos


def getErrorMsg():
    global ErrorMsg
    return ErrorMsg
