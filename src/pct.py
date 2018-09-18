

class Pct(object):

    def __init__(self):
        self.list = []

    def push(self, var_type):
        self.list.append(var_type)

    def isempty(self):
        return not self.list

    def pop(self):
        if not self.isempty():
            temp = self.list.pop(-1)
            return temp

    def top(self):
        return self.list[-1]

    def actualize_pct(self, result_type):
        self.list.pop(-1)
        self.list.pop(-1)
        self.list.append(result_type)

    def type_checking_arithmetic(self):
        top = self.list[-1]
        sub_top = self.list[-2]

        if top == 'integer' and sub_top == 'integer':
            self.actualize_pct('integer')
        elif top == 'real' and sub_top == 'real':
            self.actualize_pct('real')
        elif top == 'integer' and sub_top == 'real':
            self.actualize_pct('real')
        elif top == 'real' and sub_top == 'integer':
            self.actualize_pct('real')
        else:
            #print('arithmetic ' + top + ' - ' + sub_top)
            return False
        #print('arithmetic ' + top + ' - ' + sub_top)
        return True

    def type_checking_relational(self):
        top = self.list[-1]
        sub_top = self.list[-2]
        types = ['integer', 'real']

        if top in types and sub_top in types:
            self.actualize_pct('boolean')
        else:
            #print('relational ' + top + ' - ' + sub_top)
            return False
        #print('relational ' + top + ' - ' + sub_top)
        return True

    def type_checking_logical(self):
        top = self.list[-1]
        sub_top = self.list[-2]

        if top == 'boolean' and sub_top == 'boolean':
            self.actualize_pct('boolean')
        else:
            #print('logical ' + top + ' - ' + sub_top)
            return False
        #print('logical ' + top + ' - ' + sub_top)
        return True
