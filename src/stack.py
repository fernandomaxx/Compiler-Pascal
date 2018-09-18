class Stack(object):

    def __init__(self):
        self.list = []

    def push(self, value):
        self.list.append(value)

    def isempty(self):
        return not self.list

    def pop(self):
        if not self.isempty():
            self.list.pop(-1)
