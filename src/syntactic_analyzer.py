import sys


class SyntacticAnalyzer(object):

    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.index = -1
        self.flag_do = 0

    def program(self):
        if self.next_token().token == 'program':
            if self.next_token().tokenType == 'Identificador':
                if self.next_token().token == ';':
                    self.variable_declaration()
                    self.subprograms_declarations()
                    self.composed_commands()
                    if self.next_token().token == '.':
                        print('sucesso')
                    else:
                        self.syntax_error('.')
                else:
                    print(self.get_token().token)
                    self.syntax_error(';')
            else:
                self.syntax_error('Identificador')
        else:
            self.syntax_error('program')

    # aponta para o próximo token da lista
    def previous_token(self):
        if (self.index - 1) > 0:
            return self.list_tokens[self.index - 1]
        else:
            sys.exit("out range")

    # utilities
    def next_token(self):
        if (self.index + 1) < len(self.list_tokens):
            self.index += 1
            return self.list_tokens[self.index]
        else:
            sys.exit("out range")

    # trata os erros de sintax
    def syntax_error(self, expected):
        ct = self.get_token()
        sys.exit('Syntax error, "{}" expected but "{}" found in line {}'.format(expected, ct.token, ct.line))

    # retorna o token atual
    def get_token(self):
        return self.list_tokens[self.index]


    # Início da analise de variáveis #
    def variable_declaration(self):
        if self.next_token().token == 'var':
            self.list_var_declarations(True)
        else:
            self.index -= 1

    ''' 
        flag indica a primeira chamada da função, pois
        a partir da segunda chamada não existe erro de 
        identificador.
    '''

    def list_var_declarations(self, flag=False):
        if self.list_identifiers():
            if self.next_token().token == ':':
                self.type()
                if self.next_token().token == ';':
                    self.list_var_declarations()
                else:
                    self.syntax_error(';')
            else:
                self.syntax_error(':')
        elif flag:
            self.syntax_error('Identificador')

    def list_identifiers(self):
        if self.next_token().tokenType == 'Identificador':
            self.list_identifiers_()
            return True
        else:
            self.index -= 1
            return False

    def list_identifiers_(self):
        if self.next_token().token == ',':
            if self.next_token().tokenType == 'Identificador':
                self.list_identifiers_()
            else:
                self.syntax_error('Identificador')
        else:
            self.index -= 1

    def type(self):
        if self.next_token().token in ['integer', 'boolean', 'real']:
            return
        else:
            self.syntax_error('Tipo')

    # Fim da análise de variáveis #

    def subprograms_declarations(self):
        self.subprograms_declarations_()

    def subprograms_declarations_(self):
        if self.subprogram_declaration():
            if self.next_token().token == ';':
                self.subprograms_declarations_()
            else:
                self.syntax_error(';')

    def subprogram_declaration(self):
        if self.next_token().token == 'procedure':
            if self.next_token().tokenType == 'Identificador':
                self.arguments()
                if self.next_token().token == ';':
                    self.variable_declaration()
                    self.subprograms_declarations()
                    self.composed_commands()
                    return True
                else:
                    self.syntax_error(';')
            else:
                self.syntax_error('Identificador')
        else:
            self.index -= 1

    def arguments(self):
        if self.next_token().token == '(':
            self.list_parameters()
            if self.next_token().token == ')':
                pass
            else:
                self.syntax_error(')')
        else:
            self.index -= 1

    def list_parameters(self):
        self.list_identifiers()
        if self.next_token().token == ':':
            self.type()
            self.list_parameters__()
        else:
            self.syntax_error(':')

    def list_parameters__(self):
        if self.next_token().token == ';': #ainda existe mais parâmetros para ser verificado
            self.list_identifiers()
            if self.next_token().token == ':':
                self.type()
                self.list_parameters__()
            else:
                self.syntax_error(':')
        else:
            self.index -= 1
        '''
            se não for ';' significa que terminou a verificação de parâmetros e o próximo
            caractere da lista tem que ser ')' 
        '''

    def composed_commands(self):
        if self.next_token().token == 'begin':
            self.options_commands()
            if self.next_token().token == 'end':
                return True
            else:
                self.syntax_error('end')
        else:
            self.index -= 1
            return False

    def options_commands(self):
        self.list_commands()

    def list_commands(self):
        self.command()
        self.list_commands_()

    def list_commands_(self):
        if self.next_token().token == ';':
            self.command()
            self.list_commands_()
        else:
            self.index -= 1

    def command(self):
        if self.variable():
            if self.next_token().token == ':=':
                self.expression()
                return
            else:
                self.syntax_error(':=')
        elif self.activation_procedure():
            pass
        elif self.composed_commands():
            pass
        else:
            temp = self.next_token()
            if temp.token == 'if':
                self.expression()
                if self.next_token().token == 'then':
                    self.command()
                    self.part_else()
                    return
                else:
                    self.syntax_error('then')
            elif temp.token == 'while':
                self.expression()
                if self.next_token().token == 'do':
                    self.command()
                    return
                elif self.get_token().token == 'end':
                    self.index -= 1
                    return
                else:
                    self.syntax_error('do')
            elif temp.token == 'do':
                self.list_commands()
            else:
                self.index -= 1
                return False

    def part_else(self):
        self.index += 1
        if self.next_token().token == 'else':
            self.command()
        else:
            self.index -= 1

    def variable(self):
        if self.next_token().tokenType == 'Identificador':
            return True
        else:
            self.index -= 1
            return False

    def activation_procedure(self):
        if self.next_token().tokenType == 'Identificador':
            if self.next_token().token == '(':
                self.list_expressions()
                if self.next_token().token == ')':
                    return True
                else:
                    self.syntax_error(')')
            else:
                self.index -= 1
                return True
        else:
            self.index -= 1
            return False

    def list_expressions(self):
        self.expression()
        self.list_expressions_()

    def list_expressions_(self):
        if self.next_token().token == ';':
            self.expression()
            self.list_expressions_()
        else:
            self.index -= 1

    def expression(self):
        if self.simple_expression():
            if self.op_relational():
                self.simple_expression()
        else:
            self.syntax_error('Expressao')

    def simple_expression(self):
        if self.term():
            self.simple_expression_()
            return True
        elif self.signal():
            self.term()
            self.simple_expression_()
            return True
        else:
            return False

    def simple_expression_(self):
        if self.op_additive():
            self.term()
            self.simple_expression_()

    def term(self):
        if self.factor():
            self.term_()
            return True
        else:
            return False

    def term_(self):
        if self.op_multi():
            self.factor()
            self.term_()

    def factor(self):
        temp = self.next_token()
        if temp.tokenType == 'Identificador':
            if self.next_token() == '(':
                self.list_expressions()
                if self.next_token().token == ')':
                    return True
                else:
                    self.syntax_error(')')
            else:
                self.index -= 1
                return True
        elif temp.tokenType == 'Numero inteiro':
            return True
        elif temp.tokenType == 'Numero real':
            return True
        elif temp.token in ['true', 'false']:
            return True
        elif temp.token == '(':
            self.expression()
            if self.next_token().token == ')':
                return True
            else:
                self.syntax_error(')')
        elif temp.token == 'not':
            self.factor()
            return True
        else:
            self.index -= 1
            return False

    def signal(self):
        if self.next_token().token in "+-":
            return True
        else:
            self.index -= 1
            return False

    def op_relational(self):
        if self.next_token().tokenType == 'Operador relacional':
            return True
        else:
            self.index -= 1
            return False

    def op_additive(self):
        if self.next_token().tokenType == 'Operador aditivo':
            return True
        else:
            self.index -= 1
            return False

    def op_multi(self):
        if self.next_token().tokenType == 'Operador multiplicativo':
            return True
        else:
            self.index -= 1
            return False

