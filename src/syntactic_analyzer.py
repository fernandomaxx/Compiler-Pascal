import sys
import traceback

from src.symbol_table import SymbolTable
from src.pct import Pct


class SyntacticAnalyzer(object):

    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.index = -1
        self.flag_do = 0
        self.symbol_table = SymbolTable()  # Semantic
        self.pct = Pct()
        self.scope = 0  # Semantic

    def program(self):
        if self.next_token().token == 'program':
            self.symbol_table.begin_scope()  # Semantic
            if self.next_token().tokenType == 'Identificador':
                self.symbol_table.add_symbol(self.get_token().token, 'program')  # Semantic
                if self.next_token().token == ';':
                    self.variable_declaration()
                    self.subprograms_declarations()
                    self.composed_commands()
                    if self.next_token().token == '.':
                        self.symbol_table.end_scope()  # Semantic
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

    ''' Help Functions '''
    def previous_token(self):
        if (self.index - 1) > 0:
            return self.list_tokens[self.index - 1]
        else:
            sys.exit("out range")

    def next_token(self):
        if (self.index + 1) < len(self.list_tokens):
            self.index += 1
            return self.list_tokens[self.index]
        else:
            sys.exit("out range")

    def syntax_error(self, expected):
        ct = self.get_token()
        sys.exit('Syntax error, "{}" expected but "{}" found in line {}'.format(expected, ct.token, ct.line))

    def get_token(self):
        return self.list_tokens[self.index]

    ''' SyntacticAnalyzer Functions '''
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
            self.verify_scope(self.get_token().token)  # Semantic
            self.list_identifiers_()
            return True
        else:
            self.index -= 1
            return False

    def list_identifiers_(self):
        if self.next_token().token == ',':
            if self.next_token().tokenType == 'Identificador':
                self.verify_scope(self.get_token().token)  # Semantic
                self.list_identifiers_()
            else:
                self.syntax_error('Identificador')
        else:
            self.index -= 1

    def type(self):
        if self.next_token().token in ['integer', 'boolean', 'real']:
            self.symbol_table.set_type(self.get_token().token)  # Semantic
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
                self.symbol_table.add_symbol(self.get_token().token, 'procedure')  # Semantic
                self.symbol_table.begin_scope()  # Semantic
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
        if self.next_token().token == ';':  # ainda existe mais parâmetros para ser verificado
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
            self.scope += 1  # Semantic
            self.options_commands()
            if self.next_token().token == 'end':
                self.scope -= 1  # Semantic
                if not self.scope:  # Semantic
                    self.symbol_table.end_scope()  # Semantic
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

    ''' Semantic '''
    def verify_typesId(self, type_id, pct_top):
        line = self.get_token().line
        if type_id == 'integer' and pct_top == 'real':
            sys.exit('Erro linha {}! Incompatibilade de tipos: Atribuindo um valor real a uma variável inteira'.format(line))
        if type_id in ['integer', 'real'] == pct_top == 'boolean':
            sys.exit('Erro linha {}! Incompatibilade de tipos: Atribuindo um valor booleano a uma variável {}'.format(line, type_id))
        if type_id == 'boolean' and pct_top in ['integer', 'real']:
            sys.exit('Erro linha {}! Incompatibilade de tipos: Atribuindo um valor {} em uma variavel boolean'.format(line, pct_top))

        self.pct.pop()

    def verify_scope(self, symbol):
        if self.scope:
            if not self.symbol_table.search_symbol(symbol.token):
                sys.exit('Erro linha {}! Simbolo {} nao declarado'.format(symbol.line, symbol.token))
        else:
            if not  self.symbol_table.add_symbol(symbol.token, '?'):
                sys.exit("Erro linha {}! Simbolo {} ja foi declarado no mesmo escopo".format(symbol.line, symbol.token))

