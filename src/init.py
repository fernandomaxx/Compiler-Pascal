
from src import lexical_analyzer, Application

ref_cod = open("Codigo.txt", 'r')
File = ref_cod.readlines()
ref_reser = open("PalavrasReservadas.txt", 'r')
reser = ref_reser.readlines()


lexico = lexical_analyzer.LexicalAnalyzer(File, reser)
lexico.delComments()
lexico.splitTokens()
lexico.identifierChecker()
lexico.classifier()
