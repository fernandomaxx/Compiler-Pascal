from src import tokens
import re


class LexicalAnalyzer():
    isComment = False
    file = None
    reserved = None
    table = []

    def __init__(self, file, reserved):
        self.file = file
        self.reserved = reserved

    def tete(self):
        self.delComments()
        self.splitTokens()

    def isInvalid(self, char):
        if char == ' ':
            return False
        pattern = "[a-z]|[A-Z]|\d|/|:|;|<|=|-|>|\(|\)|\.|,|{|}|\*|\+"
        valid = re.compile(pattern)
        if valid.match(char) is not None:
            return False
        return True

    def delComments(self):
        for i in range(len(self.reserved)):
            self.reserved[i] = self.reserved[i].replace('\n', '')

        for x in range(0, len(self.file)):
            string = self.file[x]
            string = string.replace("\t", "")
            string = string.replace("\n", "")

            size = len(string)
            listchar = list(string)
            flag = 0

            for i in range(0, size):
                if listchar[i] == '{' and self.isComment == False:
                    self.isComment = True

                if i + 1 < size:
                    if listchar[i] == '/' and listchar[i + 1] == '/' and self.isComment == False:
                        self.isComment = True
                        flag = 1

                if self.isInvalid(listchar[i]) and not self.isComment:
                    print("caractere invalido")

                if listchar[i] == '}' and self.isComment and flag is not 1:
                    self.isComment = False
                    listchar[i] = "";
                elif listchar[i] == '}' and not self.isComment:
                    print('comentario invalido')

                if self.isComment:
                    listchar[i] = "";

            if flag is 1 and self.isComment:
                self.isComment = False
                flag = 0

            string = ''.join(listchar)
            self.file[x] = string

        if self.isComment:
            print('comentario aberto e não fechado')

    def splitTokens(self):
        for x in range(0, len(self.file)):

            listchar = list(self.file[x])
            length = len(listchar)
            i = 0
            # print(length)
            while (i < length):

                # print(length)
                # print(i)
                mov = self.isSymbol(listchar[i], listchar[i + 1 if i + 1 < length else i])
                # print(listchar[i] + ' ' + listchar[i + 1 if i + 1 < length else i])
                size = 0

                if mov is 0:

                    if listchar[i + 1 if i + 1 < length else i] is not ' ':
                        listchar.insert(i + 1, ' ')
                        size += 1
                    if listchar[i - 1 if i - 1 > 0 else 0] is not ' ':
                        listchar.insert(i, ' ')
                        size += 1
                    length = len(listchar)

                if mov is 1:

                    if listchar[i - 1 if i - 1 > 0 else 0] is not ' ':
                        listchar.insert(i, ' ')
                        size += 1
                    if listchar[i + 3] is not ' ':
                        listchar.insert(i + 3, ' ')
                        size += 1

                    length = len(listchar)

                i += size
                i += 1

            self.file[x] = ''.join(listchar)

    def isReservedWord(self, word):
        if word in self.reserved:
            return True
        return False

    def isSymbol(self, char_one, char_two):
        string = char_one + char_two + ''
        # print(string)

        if re.match(r'(:=|<=|>=|<>)+', string) is not None:
            return 1;
        elif re.match(r',|;|:|\(|\)|/|\*|\+|-', char_one) is not None:
            return 0;

        return -1

    def isSymbolwithif(self, a, b):
        string = a + b

        if string is ':=' or string is '<=' or string is '>=' or string is '<>':
            return 1

        elif a is ',' or a is ';' or a is ':' or a is "(" or a is ')' or a is '/' or a is '*' or a is '+' or a is '-':
            return 0

        return -1

    def show(self):
        for i in self.file:
            listchar = list(i.split(" "))
            i = " ".join(listchar)
            print(i)

    def identifierChecker(self):
        for x in range(0, len(self.file)):

            pattern = '\d+\w+'
            listchar = list(self.file[x].split(" "))

            for i in range(0, len(listchar)):
                string = listchar[i]

                if re.match(pattern, string) is not None:
                    for j in range(0, len(string)):
                        if re.match('\d', string[j]) is None:
                            stringlist = list(string)
                            stringlist.insert(j, ' ')
                            string = ''.join(stringlist)
                            listchar[i] = ''.join(string)
                            self.file[x] = ' '.join(listchar)
                            break

    def classifierTokens(self, token, line):

        if token is '':
            return

        if re.match(r'\d+[.]\d*x\d+[.]\d*y\d+[.]\d*z', token):
            tokenType = 'Real 3D'

        elif re.match(r'\d+', token) and '.' not in token:
            tokenType = 'Numero inteiro'

        elif re.match(r'\d+.\d*', token):
            tokenType = 'Numero real'

        elif re.match(r'\*|/|and', token):
            tokenType = 'Operador multiplicativo'

        elif re.match(r'\+|-|or', token):
            tokenType = 'Operador aditivo'

        elif re.match(r'<|>|=|<=|>=|<>', token):
            tokenType = 'Operador relacional'

        elif token == ':=':
            tokenType = 'Atribuicao'

        elif re.match(r':|;|\.|,|\(|\)', token):
            tokenType = 'Delimitador'

        elif re.match(r'\w+', token):
            if self.isReservedWord(token):
                tokenType = 'Palavra reservada'

            elif token.lower() == 'true' or token.lower() == 'false':
                tokenType = 'Boolean'

            else:
                tokenType = 'Identificador'
        else:
            return

        self.table.append(tokens.Token(token, tokenType, line))

    def classifier(self):
        for x in range(0, len(self.file)):

            tokens = list(self.file[x].split(' '))

            for i in range(0, len(tokens)):
                self.classifierTokens(tokens[i], x + 1)

        return self.table
