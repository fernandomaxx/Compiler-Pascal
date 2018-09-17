
class Token(object):

    def __init__(self, token, tokenType, line):
        self.token = token
        self.tokenType = tokenType
        self.line = line

    def show(self):
        return self.token + '\t\t\t' + self.tokenType + '\t + self.line'
