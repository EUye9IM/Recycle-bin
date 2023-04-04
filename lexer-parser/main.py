from scan import Scanner
from parser_ import Parser
from grammar_reader import GrammerReader
from tree import *
from tree_parser import TreeParser
import utility


if __name__ == "__main__":
    rule_file_name = "rule.l"
    code_file_name = "input.cpp"

    print("扫描程序开始，从 {} 文件读取类 C 语言代码...".format(code_file_name))
    code_scan = Scanner(code_file_name)
    tokens = code_scan.get_token_list()
    # code_scan.print_token_to_file()

    print("从 {} 文件读取文法......".format(rule_file_name))
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

    print("所有产生式如下所示：")
    count = 0
    for i in production:
        count += 1
        print("{}. {} --> {}".format(count, i["left"], " ".join(i["right"])))
    print()
    print("正在生成语法分析器......")
    parser = Parser(production, grammar)
    print("语法分析器完成.")
    print("正在传入 token 流......")
    code_text = []
    for t in tokens:
        code_text.append(t.type)
    parser.print_lr_table()
    if parser.is_lr1():
        print("是LR1文法")
    else:
        print("不是LR1")
    productions = parser.analyze(code_text)
    print("分析完成，打印语法树......")
    node = {}
    makeTree(productions, node)
    printTree(node, tokens)
    print("打印完成，生成四元式......")

    tp = TreeParser()
    tp.visitNodes(node, tokens)

    tp.showResult()
    tp.printQuad();
    print("\nOver!")
