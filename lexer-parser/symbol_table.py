import copy

"""
符号表
实现课本p222，8.1.1的基本功能
"""


class Symbol:
    def __init__(self, name: str, info: dict = {}):
        self.name = name
        self.info = dict(info)

    def __str__(self):
        return "name:{}\tinfo:{}\n".format(self.name, self.info)


class SymbolTable:
    def __init__(self):
        # nameSet为 Symbol 的 name
        self.nameSet = []
        # content列表元素类型为 Symbol
        self.content = []

    def ifExist(self, name: str):
        return name in self.nameSet

    def add(self, symbol: Symbol):
        if symbol.name not in self.nameSet:
            self.nameSet.append(symbol.name)
        self.content.append(copy.deepcopy(symbol))
        return

    def get(self, name: str):
        if not name in self.nameSet:
            return None
        for i in self.content:
            if i.name == name:
                return copy.deepcopy(i)
        return None

    def update(self, symbol: Symbol):
        if not symbol.name in self.nameSet:
            self.nameSet.append(symbol.name)
            self.content.append(copy.deepcopy(symbol))
            return
        for i, v in enumerate(self.content):
            if self.content[i].name == symbol.name:
                self.content[i].name = symbol.name
                self.content[i].info = copy.deepcopy(symbol.info)
        return

    def remove(self, name: str):
        self.nameSet.remove(name)
        for i, v in enumerate(self.content):
            if self.content[i].name == name:
                self.content.pop(i)

    def removeWhere(self, condition):
        for i, v in enumerate(self.content):
            if condition(self.content[i]):
                self.content.pop(i)
                self.nameSet.remove(v.name)
                self.removeWhere(condition)
                break

    def selectWhere(self, condition):
        ret = SymbolTable()
        for i in self.content:
            if condition(i):
                ret.add(i)
        return ret

    def __str__(self):
        ret = "===== Symbol Table =====\n"
        ret += "{}\t{}\n".format("name", "info")
        for i in self.content:
            ret += "{}\t{}\n".format(i.name, i.info)
        ret += "=== End Symbol Table ==="
        return ret


if __name__ == "__main__":
    print("\nnew symbol table")
    symTb = SymbolTable()
    print(symTb)

    print("\ninit symbol table")
    symTb.add(Symbol("a", {"name": "a1", "val": 1}))
    symTb.add(Symbol("a", {"name": "a2", "val": 1}))
    symTb.add(Symbol("a", {"name": "a3", "val": 1}))
    symTb.add(Symbol("b", {"name": "b", "val": 2}))
    symTb.add(Symbol("c", {"name": "c", "val": 3}))
    symTb.add(Symbol("d", {"name": "d", "val": 4}))
    symTb.add(Symbol("constaint", {"name": "version", "type": "int"}))
    print(symTb)

    print("\nif c in table:", symTb.ifExist("c"))
    print("\nif e in table:", symTb.ifExist("e"))
    print("\nif a1 in table:", symTb.ifExist("a1"))

    print("\nb's info:", symTb.get("b"))
    print("\ne's info:", symTb.get("e"))
    print("\na's info:", symTb.get("a"))

    print("\nupdate b.val=10")
    symTb.update(Symbol("b", {"name": "b", "val": 10}))
    print(symTb)

    print("\nupdate e.val=5")
    symTb.update(Symbol("e", {"name": "b", "val": 3}))
    print(symTb)

    print("\nremove b")
    symTb.remove("b")
    print(symTb)

    print("\nremove where val=3")
    symTb.removeWhere(lambda x: x.info["val"] == 3)
    print(symTb)

    print("\nselect where val>3")
    print(symTb.selectWhere(lambda x: x.info["val"] > 3))
