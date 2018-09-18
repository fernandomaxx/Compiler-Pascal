
from src.lexical_analyzer import LexicalAnalyzer
from src.syntactic_analyzer import SyntacticAnalyzer


if __name__ == '__main__':
    ref_cod = open("../program.txt", 'r')
    File = ref_cod.readlines()
    ref_reserved = open("../PalavrasReservadas.txt", 'r')
    reserved = ref_reserved.readlines()
    lexical = LexicalAnalyzer(File, reserved)
    lexical.delComments()
    lexical.splitTokens()
    lexical.identifierChecker()
    result = lexical.classifier()
    SyntacticAnalyzer(result).program()