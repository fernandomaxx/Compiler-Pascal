from src import symbol


class SymbolTable(object):

    def __init__(self):
        self.list = []
        self.mark = '$'

    def push(self, symbol):
        self.list.append(symbol)

    def isempty(self):
        return not self.list

    def pop(self):
        if not self.isempty():
            self.list.pop(-1)

    def add_symbol(self, identifier, type):
        if self.isempty():
            self.push(identifier)
            return

        i = -1

        while self.list[i].identifier != self.mark and self.list[i].identifier != identifier:
            i -= 1

        if self.list[i].identifier == self.mark:
            self.push(symbol.Symbol(identifier, type))
            return True
        else:
            return False

    def search_symbol(self, identifier):
        for x in self.list[::-1]:
            if x.identifier == identifier:
                return x
        return False

    def begin_scope(self):
        self.list.append(symbol.Symbol(self.mark, 'mark'))

    def end_scope(self):
        if self.isempty():
            return

        while self.list[-1].identifier != self.mark:
            self.pop()
        self.pop()

    def printStack(self):
        for x in self.list:
            print ('[{}, {}]'.format(x.identifier, x.type), end='')
        print()

    def set_type(self, type):
        i = -1
        while True:
            if self.list[i].type == '?':
                self.list[i].type = type
                i -= 1
            else:
                break
