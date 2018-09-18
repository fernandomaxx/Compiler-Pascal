import tkinter as tk
# import ttk
from tkinter import ttk
from src import lexical_analyzer
from src import syntactic_analyzer


class Application(tk.Frame):

    def __init__(self, table, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.set_widgets(table)

    def set_widgets(self, table):
        # Inicia o Treeview com as seguintes colunas:
        self.dataCols = ('token', 'classificação', 'linha')
        self.tree = ttk.Treeview(columns=self.dataCols, show='headings')
        self.tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        # Barras de rolagem
        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        xsb.grid(row=1, column=0, sticky=tk.E + tk.W)

        # Define o textos do cabeçalho (nome em maiúsculas)
        for c in self.dataCols:
            self.tree.heading(c, text=c.title())

        # Insere cada item dos dados
        for tab in table:
            lol = (tab.token, tab.tokenType, tab.line)
            self.tree.insert('', 'end', values=lol)


if __name__ == '__main__':
    root = tk.Tk()
    ref_cod = open("../program.txt", 'r')
    File = ref_cod.readlines()
    ref_reserved = open("../reservedwords.txt", 'r')
    reserved = ref_reserved.readlines()
    lexical = lexical_analyzer.LexicalAnalyzer(File, reserved)
    lexical.delComments()
    lexical.splitTokens()
    lexical.identifierChecker()
    result = lexical.classifier()
    syntactic_analyzer.SyntacticAnalyzer(result).program()
    app = Application(result, master=root)
    app.mainloop()
