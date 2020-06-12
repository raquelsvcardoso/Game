# -*- coding:utf-8 -*-
'''
Created on 1/12/2018

@author: valves
'''
from cmd import *
from GandaGaloWindow import GandaGaloWindow
from GandaGaloEngine import GandaGaloEngine



class GandaGaloShell(Cmd):
    intro = 'Interpretador de comandos para o GandaGalo. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'GandaGalo> '
                               
    def do_mostrar(self, arg):
        " -  comando mostrar que leva como parâmetro o nome de um ficheiro..: mostrar <nome_ficheiro> \n"
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                tempeng = GandaGaloEngine() # cria nova instancia temporaria de tabuleiro
                tempeng.ler_tabuleiro_ficheiro(lista_arg[0])
                tempeng.printpuzzle() # mostrar tabuleiro na consola
                global janela  # pois pretendo atribuir um valor a um identificador global
                if janela is not None:
                    del janela  # invoca o metodo destruidor de instancia __del__()
                janela = GandaGaloWindow(40, tempeng.getlinhas(), tempeng.getcolunas())
                janela.mostraJanela(tempeng.gettabuleiro())
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle")
    
    def do_abrir(self, arg):
        " - comando abrir que leva como parâmetro o nome de um ficheiro..: abrir <nome_ficheiro>  \n"
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.ler_tabuleiro_ficheiro(lista_arg[0]) # invoca o metodo de leitura do tabuleiro para eng
                eng.prepararjogo() # calcular o numero de casas livres
                eng.printpuzzle() # mostrar o tabuleiro de jogo na consola
        except:
            print("Erro: ao abrir o puzzle")

    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro..: gravar <nome_ficheiro>  \n"
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.gravar_tabuleiro_ficheiro(lista_arg[0]) # invoca o metodo de gravação to tabuleiro num ficheiro de texto
        except:
            print("Erro: ao gravar o puzzle")
    
    def do_jogar(self, arg):    
        " - comando jogar que leva como parâmetro o caractere referente à peça a ser jogada (‘X’ ou ‘O’) e dois inteiros que indicam o número da linha e o número da coluna, respetivamente, onde jogar \n"
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 3 :
                if lista_arg[0].upper() in ["X", "O"]:
                    eng.setsimbolo(lista_arg[0].upper(), int(lista_arg[1]), int(lista_arg[2])) #set do simbolo na coordenada
                else:
                    print("Simbolo errado, introduza X ou O")
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao jogar")

    def do_validar(self, arg):
        " - comando validar que testa a consistência do puzzle e verifica se o tabuleiro está válido: validar \n"
        try:
            if eng.getvalidado() == (-2,-2): # se nunca foi validado (-2,-2) <- sentinela
                if eng.percorrer(): # percorre todas as posições do tabuleiro a procura de validar o tabuleiro
                    if eng.getjogadas() > 0: # se ja houver jogadas efetuadas
                        eng.setvalidado(eng.getultimajogada()) # defenir o estado de validado a ultima jogada
                    else:
                        eng.setvalidado((-1, -1)) #Se for valido e não houver jogadas efetuadas atribui a sentinela (-1,-1)
                        print("Tabuleiro é valido")
                else:
                    print("Tabuleiro não é valido")
            else:
                if eng.getjogadas() > 0: # Se ja foi validado e existem jogadas realizadas
                    if eng.validajogadas(eng.getvalidado()): # valida todas as posições jogadas até á ultima validação
                        eng.setvalidado(eng.getultimajogada())
                        print("Tabuleiro é valido")
                    else:
                        print("Tabuleiro não é valido")
        except:
            print("Erro ao validar")

    def do_ajuda(self, arg):    
        " - comando ajuda que indica a próxima casa lógica a ser jogada (sem indicar a peça a ser colocada): ajuda  \n"
        try:
            conjunto = eng.coordenadaslogicas() # conjunto de coordenadas com possiveis ambiguidades para ser verificada pelo utilizador
            if len(conjunto) > 0:
                if eng.getvalidado() == eng.getultimajogada() or eng.getvalidado() == (-1, -1):
                    linha, coluna = conjunto[0]
                    print("Experimente a casa na linha", linha + 1, "coluna", coluna + 1, "!")
                    global janela  # pois pretendo atribuir um valor a um identificador global
                    if janela is not None:
                        del janela  # invoca o metodo destruidor de instancia __del__()
                    janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
                    janela.mostraJanela(eng.gettabuleiro()) # mostrar tabuleiro de jogo atual na janela
                    janela.desenhaCasaIluminada(coluna + 1, linha + 1)
                    return
                else:
                    conjunto = eng.conjuntocoordenadasproximas() # conjunto de coordenadas proximas caso não haja com possiveis ambiguidades
                    resolucao = eng.resolverproxima(conjunto)
                    if resolucao == False:
                        conjunto = eng.conjunntocoordenadastodas(conjunto)
                        resolucao = eng.resolverproxima(conjunto)
                        if resolucao == False:
                            print("Nao é possivel resolver")
                    if resolucao != False:
                        simbolo, linha, coluna = resolucao
                        print("Experimente a casa na linha", resolucao[1] + 1, "coluna", resolucao[2] + 1, "!")
                        #global janela  # pois pretendo atribuir um valor a um identificador global
                        if janela is not None:
                            del janela  # invoca o metodo destruidor de instancia __del__()
                        janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
                        janela.mostraJanela(eng.gettabuleiro())  # mostrar tabuleiro de jogo atual na janela
                        janela.desenhaCasaIluminada(resolucao[2]+1, resolucao[1]+1)
                    else:
                        print("Tabuleiro não Validado")

        except:
            print("Erro a encontrar ajuda")

    def do_undo(self, arg):    
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        if eng.getjogadas() > 0: # se houverem jogadas realizadas
            eng.undo()
        else:
            print("Erro: ao executar o UNDO: ")

    def do_resolver(self, arg):    
        " - comando para resolver o puzzle: resolver \n"
        #try:
        if eng.resolver2():
            global janela  # pois pretendo atribuir um valor a um identificador global
            if janela is not None:
                del janela  # invoca o metodo destruidor de instancia __del__()
            janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
            janela.mostraJanela(
            eng.gettabuleiro())  # mostrar tabuleiro de jogo atual na janela
            print("Tabuleiro Resolvido!")
        else:
            print("Não é possivel resolver o tabuleiro")
        #except:
            #print("Erro ao resolver o puzzle")

    def do_ancora(self, arg):    
        " - comando âncora que deve guardar o ponto em que está o jogo para permitir mais tarde voltar a este ponto: ancora \n"
        if eng.getlinhas() >= 0 or eng.getcolunas() >= 0:
            if eng.getjogadas() > 0:
                eng.setancora(eng.getultimajogada())
            else:
                eng.setancora((0,0))
            print("Ancora definida")
        else:
            print("Erro: Não existe puzzle aberto")

    def do_undoancora(self, arg):    
        " - comando undo para voltar à última ancora registada: undoancora \n"
        eng.undoancora()
    
    def do_gerar(self, arg):    
        " - comando gerar que gera puzzles com solução única e leva três números inteiros como parâmetros: o nível de dificuldade (1 para ‘fácil’ e 2 para ‘difícil’), o número de linhas e o número de colunas do puzzle \n"
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 3:
                area = int(lista_arg[1])*int(lista_arg[2])
                if int(lista_arg[0]) == 2:
                    resolver = True
                    while resolver:
                        eng.settabuleiro(eng.criartabuleiro(int(lista_arg[1]), int(lista_arg[2]))) # gera novo tabuleiro com as especificações
                        branco = eng.gerarcoordenadasrandom(int(area*0.05), int(area*0.1)) # gera nr de coordenadas que correspondem entre 5 a 10 % do tabuleiro para casa bloqueadas
                        x = eng.gerarcoordenadasrandom(int(area*0.1), int(area*0.20)) # gera nr de coordenadas que correspondem entre 10 e 20% do tabuleiro para X
                        o = eng.gerarcoordenadasrandom(int(area*0.1), int(area*0.20)) # gera nr de coordenadas que coorespondem entre 10 a 20% do tabuleiro para O
                        eng.colocarsimbolos("#", branco)
                        eng.colocarsimbolos("X", x)
                        eng.colocarsimbolos("O", o)
                        eng.printpuzzle() # imprime puzzle na consoola
                        if eng.resolver2(): # tenta resolucao
                            # caso tenha achado resolução retira todas as coordenadas não definidas a priori e entrega o tabuleiro para jogar
                            eng.settabuleiro(eng.criartabuleiro(int(lista_arg[1]), int(lista_arg[2])))
                            eng.colocarsimbolos("#", branco)
                            eng.colocarsimbolos("X", x)
                            eng.colocarsimbolos("O", o)
                            eng.prepararjogo()
                            #eng.printpuzzle()
                elif int(lista_arg[0]) == 1:
                    pass

            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro ao gerar tabuleiro")


    def do_ver(self, arg):
        " - Comando para visualizar graficamente o estado atual do GandaGalo caso seja válido: VER  \n"
        try:
            i = 0
            while i <= 1:
                if eng.getvalidado() == eng.getultimajogada() or eng.getvalidado() == (-1,-1):
                    global janela  # pois pretendo atribuir um valor a um identificador global
                    if janela is not None:
                        del janela  # invoca o metodo destruidor de instancia __del__()
                    janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
                    janela.mostraJanela(eng.gettabuleiro()) # mostrar tabuleiro de jogo atual na janela
                else:
                    self.do_validar(arg)
                i+=1
        except:
            print("Erro: ao mostrar o puzzle")



    def do_sair(self, arg):
        "Sair do programa GandaGalo: sair"
        print('Obrigado por ter utilizado o Gandagalo, espero que tenha sido divertido!')
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        return True




if __name__ == '__main__':
    eng = GandaGaloEngine()
    janela = None
    sh = GandaGaloShell()
    sh.cmdloop()


