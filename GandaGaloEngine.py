# -*- coding:utf-8 -*-
'''
Created on 1/12/2018

@author: valves
'''
from Stack import Stack
from linkedlist import node
from random import randint
class GandaGaloEngine:
    
    def __init__(self):
        self.linhas = 0
        self.colunas = 0
        self.tabuleiro = [] #matriz que representa o puzzle
        self.jogadas = Stack() #stack com todas as jogadas do utilizador
        self.ancora = (-1,-1)
        self.validado = (-2,-2)
        self.livres = 0
        self.proximajogada = None
    
    def ler_tabuleiro_ficheiro(self, filename):
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        :return tabuleiro: matriz do tabuleiro de jogo
        '''
        try:
            ficheiro = open(filename, "r")
            lines = ficheiro.readlines() #ler as linhas do ficheiro para a lista lines
            dim = lines[0].strip('\n').split(' ')  # obter os dois numeros da dimensao do puzzle, retirando o '\n'
            self.linhas = int(dim[0])  # retirar o numero de linhas
            self.colunas = int(dim[1])  # retirar o numero de colunas
            self.tabuleiro=[]
            for i in range(1,len(lines)):
                self.tabuleiro.append(lines[i].split())
            return self.tabuleiro
        except:
            print("Erro: na leitura do tabuleiro")
        else:
            self.ficheiro.close()
        return self.tabuleiro

    def prepararjogo(self):
        '''
        Função que calcula informações necessarias para o funcionamento do jogo
        a quando a iniciação de um novo tabuleiro
        :return:
        '''
        ocupadas = 0
        for i in range(self.linhas):
            for j in range(self.linhas):
                simbolo = self.tabuleiro[i][j]
                if simbolo in ["#", "X", "O"]:
                    ocupadas +=1
                    if self.proximajogada == None:
                        self.proximajogada = node((i,j),True)
                    else:
                        proximo = node((i,j),False,self.proximajogada)
                        self.proximajogada.setnext(proximo)
                        self.proximajogada = proximo
        self.livres = (self.linhas * self.colunas) - ocupadas

    def printpuzzle(self):
        '''
        Mostra o tabuleiro na consola
        '''
        for linha in self.tabuleiro:
            for simbolo in linha:
                print(simbolo,end=" ")
            print()

    def gravar_tabuleiro_ficheiro(self, filename):
        '''
        Grava instancia do jogo num ficheiro
        :param filename: nome do ficheiro a gravar
        '''
        try:
            ficheiro = open(filename, "w")
            line = (str(self.linhas) + " " + str(self.colunas))
            ficheiro.write(line)
            for linha in self.tabuleiro:
                line = "\n"
                for simbolo in linha:
                    line += (" " + simbolo)
                ficheiro.write(line)
            ficheiro.close()
        except:
            print("Erro: ao gravar o tabuleiro")
        else:
            ficheiro.close()

    def getlinhas(self):
        '''
        Get do numero de linhas do matriz do tabuleiro de jogo
        :return: numero de linhas
        '''
        return int(self.linhas)
    
    def getcolunas(self):
        '''
        Get do numero de colunas da matriz do tabuleiro de jogo
        :return: numero de colunas
        '''
        return int(self.colunas)
    
    def gettabuleiro(self):
        '''
        Get da instancia atual do tabuleiro de jogo
        :return: matriz da instancia atual do tabuleiro de jogo
        '''
        return self.tabuleiro

    def getjogadas(self):
        '''
        Get o numero de jogadas realizadas
        :return: int do numero de jogadas realizadas
        '''
        return len(self.jogadas)

    def getultimajogada(self):
        '''
        Get a informação da ultima jogada
        :return: tuplo com informação das coordenadas da ultima jogada
        '''
        return self.jogadas.top()

    def getproximajogada(self):
        '''
        Get do valor da jogada realizada durante a resolução automatica
        do tabuleiro que se encontra sobre a esturutra de linked list
        :return:
        '''
        self.proximajogada.getvalue()

    def getancora(self):
        '''
        Get da posição da ultima ancora definida
        :return: tuplo com as coordenadas da ultima ancora definida
        '''
        return self.ancora

    def getvalidado(self):
        '''
        Get do estado de validade do tabuleiro
        :return: tuplo com as coordenadas do estado / ultima jogada validada
        '''
        return self.validado

    def setproximajogada(self, linha, coluna):
        '''
        Set da proximo ligação na lista ligada com informações das coordenadas atuais
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        '''
        proximo = node((linha, coluna), False, self.proximajogada)
        self.proximajogada.setnext(proximo)
        self.proximajogada = proximo

    def settabuleiro(self, t): #nao é preciso o set de linhas e colunas acho
        '''
        Set da instancia atual do tabuleiro do jogo a partir de uma matriz t
        :param t: matriz de um tabuleiro de jogo
        :return: nova matriz do tabuleiro de jogo
        '''
        self.tabuleiro = t

    def dentrotabuleiro(self, linha, coluna):
        '''
        Verifica se as coordenadas existem dentro do tabuleiro de jogo (coordenadas de input)
        :param linha: coordenada correspondente a linha do tabuleiro
        :param coluna: coordenada correspondente a coluna do tabuleiro
        :return: True se as coordenadas existirem dentro do tabuleiro de jogo
        '''
        if linha <= self.getlinhas() and linha > 0 and coluna <= self.getcolunas() and coluna > 0:
            return True
        else:
            return False

    def setsimbolo(self, simbolo, linha, coluna):
        '''
        Set do simbolo de jogo numa posicao especifica do tabuleiro
        :param simbolo: simbolo a defininr na matriz ("X" ou "O")
        :param linha: coordenada correspondente a linha do tabuleiro
        :param coluna: coordenada correspondente a coluna do tabuleiro
        '''
        if self.dentrotabuleiro(linha, coluna):
            if self.tabuleiro[linha - 1][coluna - 1] == ".":
                self.tabuleiro[linha - 1][coluna - 1] = simbolo
                self.jogadas.push((linha - 1, coluna - 1))
                self.livres -= 1
                self.printpuzzle()
                self.setproximajogada(linha - 1, coluna - 1)
            else:
                print("Erro: Posição ocupada, escolha outra posição")
        else:
            print("Erro: Posição fora do tabuleiro")

    def setancora(self, jogada):
        '''
        Set de uma ancora de jogo, do qual é possivel reverter o estado de jogo
        :param jogada: tuplo com as coordenadas da ultima jogada efectuada
        '''
        self.ancora = jogada
        self.proximajogada.setblock(True)

    def setvalidado(self, jogada):
        '''
        Set do estado de validade do tabuleiro
        :param jogada: tuplo com informação das coordenadas da ultima jogada
        '''
        self.validado = jogada

    def undo(self):
        '''
        Volta atras uma jogada apartir da stack de jogadas efetuadas
        '''
        linha, coluna = self.jogadas.pop() # retorna par linha, coluna da ultima jogada e remove da stack de jogadas a ultima efetuada
        self.tabuleiro[linha][coluna] = "."

    def undoancora(self):
        '''
        Volta atras uma ou mais jogadas até ao estado da ultima ancora
        '''
        if self.ancora == (-1,-1):
            print("Erro: Ancora não definida")
        else:
            while self.getjogadas() > 1 or self.getultimajogada() != self.ancora:
                self.undo()
            print("Estado restaurado")

    def validadiagonal1(self, simbolo, linha, coluna, max = 2):
        '''
        Valida a posição na diagonal da esquerda para a direita
        :param simbolo: string do simbolo presente no tabuleiro para comparação
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        :param max: int do maximo(nao inclusive) de casas iguais por comparação
        :return: Boleano com o resultado da validade da posição referente à primeira diagonal
        '''
        #coordenadas matriz
        contar = 0
        movimentos = [-3, -2, 0, 1]
        # Primeira diagonal
        i1 = 0  # apontador da primeira casa
        i2 = 1  # apontador da segunda casa
        while i2 <= 3: # conta cada uma das 3 combinações possiveis de ambiguidade na direçção especifica
            # verifica se o par de coordenadas a comparar existem na matriz do tabuleiro
            if self.dentrotabuleiro(linha + movimentos[i1] + 2, coluna + movimentos[i1] + 2) and self.dentrotabuleiro(linha + movimentos[i2] + 2, coluna + movimentos[i2] + 2):
                if self.tabuleiro[linha + movimentos[i1] + 1][coluna + movimentos[i1] + 1] == simbolo:
                    contar += 1
                    if self.tabuleiro[linha + movimentos[i2] + 1][coluna + movimentos[i2] + 1] == simbolo:
                        contar += 1
            if contar >= max:
                return False
            contar = 0
            i1 += 1
            i2 += 1
        return True
        # fim da primeira diagonal

    def validavertical(self, simbolo, linha, coluna, max = 2):
        '''
        Valida a posição na vertical
        :param simbolo: string do simbolo presente no tabuleiro para comparação
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        :param max: int do maximo(nao inclusive) de casas iguais por comparação
        :return:Boleano com o resultado da validade da posição referente à vertical
        '''
        contar = 0
        movimentos = [-3, -2, 0, 1]
        # Inicio Vertical
        i1 = 0  # apontador da primeira casa
        i2 = 1  # apontador da segunda casa
        while i2 <= 3:# conta cada uma das 3 combinações possiveis de ambiguidade na direçção especifica
            # verifica se o par de coordenadas a comparar existem na matriz do tabuleiro
            if self.dentrotabuleiro(linha + movimentos[i1] + 2, coluna + 1) and self.dentrotabuleiro(linha + movimentos[i2] + 2, coluna + 1):
                if self.tabuleiro[linha + movimentos[i1] + 1][coluna] == simbolo:
                    contar += 1
                    if self.tabuleiro[linha + movimentos[i2] + 1][coluna] == simbolo:
                        contar += 1
            if contar >= max:
                return False
            contar = 0
            i1 += 1
            i2 += 1
        return True

        # fim da vertical

    def validahorizontal(self, simbolo, linha, coluna, max = 2):
        '''
        Valida a posição na horizontal
        :param simbolo: string do simbolo presente no tabuleiro para comparação
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        :param max: int do maximo(nao inclusive) de casas iguais por comparação
        :return: Boleano com o resultado da validade da posição referente à horizontal
        '''
        contar = 0
        movimentos = [-3, -2, 0, 1]
        # Inicio Horizontal
        i1 = 0  # apontador da primeira casa
        i2 = 1  # apontador da segunda casa
        while i2 <= 3 and contar < max:# conta cada uma das 3 combinações possiveis de ambiguidade na direçção especifica
            # verifica se o par de coordenadas a comparar existem na matriz do tabuleiro
            if self.dentrotabuleiro(linha + 1, coluna + movimentos[i1] + 2) and self.dentrotabuleiro(linha + 1,coluna + movimentos[i2] + 2):
                if self.tabuleiro[linha][coluna + movimentos[i1] + 1] == simbolo:
                    contar += 1
                    if self.tabuleiro[linha ][coluna + movimentos[i2] + 1] == simbolo:
                        contar += 1
            if contar >= max:
                return False
            contar = 0
            i1 += 1
            i2 += 1
        return True

    def validadiagonal2(self, simbolo, linha, coluna, max = 2):
        '''
        Valida a posição na diagonal da direita para a esquerda
        :param simbolo: string do simbolo presente no tabuleiro para comparação
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        :param max: int do maximo(nao inclusive) de casas iguais por comparação
        :return: Boleano com o resultado da validade da posição referente à segunda diagonal
        '''
        contar = 0
        movimentos = [-3, -2, 0, 1]
        movimentosrev = movimentos[::-1]  # reversao da lista movimentos
        i1l = 0  # apontador da linha da primeira casa
        i1c = 0  # apontador da coluna da primeira casa
        i2l = 1  # apontador da linha da segunda casa
        i2c = 1  # apontador da coluna da segunda casa
        while i2l <= 3 and contar < max: # conta cada uma das 3 combinações possiveis de ambiguidade na direçção especifica
            # verifica se o par de coordenadas a comparar existem na matriz do tabuleiro
            if self.dentrotabuleiro(linha + movimentos[i1l] + 2,coluna + movimentosrev[i1c] + 2) and self.dentrotabuleiro(linha + movimentos[i2l] + 2, coluna + movimentosrev[i2c] + 2):
                if self.tabuleiro[linha + movimentos[i1l]+ 1][coluna + movimentosrev[i1c] + 1] == simbolo:
                    contar += 1
                    if self.tabuleiro[linha + movimentos[i2l] + 1][coluna + movimentosrev[i2c] + 1] == simbolo:
                        contar += 1
            if contar >= max:
                return False
            contar = 0
            i1l += 1
            i1c += 1
            i2l += 1
            i2c += 1
        return True
        # fim da segunda diagonal

    def valida(self, simbolo, linha, coluna, max = 2):
        '''
        Valida uma determinada coordenada, tendo em conta o simbolo e o maximo de simbolos semelhantes
        :param simbolo: string do simbolo presente no tabuleiro para comparação
        :param linha: int com a coordenada correspondente a linha
        :param coluna: int com a coordenada correspondente a coluna
        :param max: int do maximo(nao inclusive) de casas iguais por comparação
        :return: Boleano com o resultado da validade da posição referente a todas as combinações
        '''
        if simbolo in [".", "#"]:
            return True
        else:
            if self.validadiagonal1(simbolo, linha, coluna, max) == False:
                return False
            if self.validadiagonal2(simbolo, linha, coluna, max) == False:
                return False
            if self.validavertical(simbolo, linha, coluna, max) == False:
                return False
            if self.validahorizontal(simbolo, linha, coluna, max) == False:
                return False
            return True

    def percorrer(self):
        '''
        Percorre todas as posições no tabuleiro e verifica se estão todas validas
        :return: boleano que representa a validade de todo o tabuleiro
        '''
        for lin in range(self.linhas):
            for col in range(self.colunas):
                if self.valida(self.tabuleiro[lin][col], lin, col) == False:
                    return False
        return True

    def validajogadas(self, jogada):
        '''
        Verifica a validade de todas as jogadas ate à ultima jogada avaliada
        :param jogada: tuplo com as coordenadas da ultima jogada avaliada
        :return: boleano que representa a validade de todas as jogadas ate a ultima avaliada
        '''
        jogadas = self.jogadas
        while len(jogadas) > 1 and jogadas.top() != jogada:
            lin, col = jogadas.pop()
            if self.valida(self.tabuleiro[lin][col],lin,col) == False:
                return False
        return True

    def conjuntocoordenadasproximas(self):
        '''
        Funcao que gera uma lista de coordenadas proximas da ultima jogada
        :return: lista com tuplos de coordenadas
        '''
        conjuntocoordenadas = []
        linha, coluna = self.proximajogada.getvalue()
        for i in range(linha - 3, linha + 3):
            for j in range (coluna - 3, linha + 3):
                if self.dentrotabuleiro(i + 1,j + 1):
                    conjuntocoordenadas.append((i,j))
        return conjuntocoordenadas

    def conjunntocoordenadastodas(self, conjunto=[]):
        '''
        Função que gera uma lista de todas as coordenadas do tabuleiro
        :param conjunto: lista de tuplos de coordenadas a excluir do tabuleiro
        :return: lista de tuplos com coordenadas de tabuleiro
        '''
        conjuntocoordenadas = []
        for i in range(0, self.linhas):
            for j in range (0, self.colunas):
                if self.dentrotabuleiro(i + 1, j + 1) and self.tabuleiro[i][j] == "." and (i,j) not in conjunto:
                    conjuntocoordenadas.append((i, j))
        return conjuntocoordenadas

    def coordenadasvazias(self):
        '''
        Função que gera uma lista de coordenadas possiveis de jogar (com ".")
        :return: lista de tuplos de coordenadas da matriz
        '''
        conjunto = []
        for i in range(0, self.linhas):
            for j in range(0, self.colunas):
                if self.tabuleiro[i][j] == ".":
                    conjunto.append((i,j))
        return conjunto

    def coordenadaslogicas(self):
        '''
        Função que gera uma lista de coordenadas possiveis de jogar,
        que podem criar ambiguidades
        :return: lista de tuplos de coordenadas da matriz
        '''
        conjunto = []
        for i in range(0, self.linhas):
            for j in range(0, self.colunas):
                if self.dentrotabuleiro(i + 1, j + 1) and self.tabuleiro[i][j] == ".":
                    if self.valida("X", i, j, 2) == False or self.valida("O", i, j, 2) == False:
                        conjunto.append((i,j))
        return conjunto

    def resolverproxima(self, conjunto):
        '''
        Verifica se e possivel resolver uma determinada coordenada, se sim, resolve a coordenada ao atribuir uma figura
        :param conjunto: lista de tuplos com coordenadas possiveis a testar
        :return: tuplo com str, e 2 ints, correspondentes ao simbolo introduzido e as coordenadas
                 boleano False, caso nao tenha sido possivel resolver
        '''
        for i in range(0, len(conjunto)):
            j = randint(0,1)
            linha,coluna = conjunto[i]
            simbolos = ["X", "O"]
            if self.tabuleiro[linha][coluna] == ".":
                if self.valida(simbolos[j], linha ,coluna):
                    return (simbolos[j], linha, coluna)
                else:
                    simbolos.pop(j)
                    if self.valida(simbolos[0], linha, coluna):
                        return (simbolos[0], linha, coluna)
        return False


    def resolver2(self):
        '''
        função que que resolve puzzles ao comparar posições
        de possivel ambiguidade e depois as resntantes sem ambiguidade
        '''
        repetir = True
        while repetir:
            livres = self.livres # nr de casas livres (com ".")
            conjunto = self.coordenadaslogicas() # conjunto de coordenadas livres
            for linha,coluna in conjunto:
                simbolos = ["X", "O"]
                # colocar aleatoriamente um simbolo na coordenada
                ri = randint(0,1)
                if self.valida(simbolos[ri], linha, coluna, 2):
                    self.tabuleiro[linha][coluna] = simbolos[ri]
                    self.livres -= 1
                else:
                    simbolos.pop(ri)
                    # caso a anterior tenha falhado tenta com o outro simbolo
                    if self.valida(simbolos[0], linha, coluna, 2):
                        self.tabuleiro[linha][coluna] = simbolos[0]
                        self.livres -= 1
            if livres == self.livres:
                repetir = False

        repetir = True
        while repetir:
            livres = self.livres
            conjunto = self.coordenadasvazias() # conjunto de todas as coordenadas vazias (com ".")
            for linha, coluna in conjunto:
                simbolos = ["X", "O"]
                ri = randint(0, 1)
                # Tenta preencher a casa com um "X" ou "Y" aleatoriamente
                if self.valida(simbolos[ri], linha, coluna, 2):
                    self.tabuleiro[linha][coluna] = simbolos[ri]
                    self.livres -= 1
                else:
                    #Caso o anterior nao seja valido, tenta com o outro simbolo
                    simbolos.pop(ri)
                    if self.valida(simbolos[0], linha, coluna, 2):
                        self.tabuleiro[linha][coluna] = simbolos[0]
                        self.livres -= 1
            if livres == self.livres:
                repetir = False


    def criartabuleiro(self, linhas, colunas):
        '''
        Função que cria tabuleiros vazios com dimensoes linhas, colunas e coloca em memoria de jogo
        :param linhas: int com o numero de linhas do tabuleiro
        :param colunas: int com o numero de colunas do tabuleiro
        :return: matriz do tabuleiro
        '''
        tabuleiro = []
        for i in range(0, linhas):
            linha = []
            for j in range(0, colunas):
                linha.append(".")
            tabuleiro.append(linha)
        self.linhas = linhas
        self.colunas = colunas
        self.jogadas = Stack()
        self.ancora = (-1,-1)
        self.validado = (-1,-1)
        self.livres = 0
        self.proximajogada = None
        return tabuleiro

    def gerarcoordenadasrandom(self, min, max):
        '''
        Funcao que gera coordenadas aleatorias tendo em conta um numero minimo e um numero maximo
        :param min: int com o numero minimo de coordenadas a criar
        :param max: int com o numero maximo de coordenadas a criar
        :return: lista de tuplos com coordenadas aleatorias
        '''
        coordenadas = []
        for i in range(0, randint(min,max)):
            coordenada = (randint(0, int(self.linhas -1)), randint(0, int(self.colunas - 1)))
            if coordenada not in coordenadas :
                coordenadas.append(coordenada)
        return coordenadas

    def colocarsimbolos(self, simbolo, conjunto):
        '''
        Função que coloca simbolos especificos num conjunto de coordenadas do tabuleiro, caso valida
        :param simbolo: string com o simbolo a colocar no tabuleiro
        :param conjunto: lista de tuplos de coordenadas correspondentes a matriz do tabueliro
        '''
        for coordenada in conjunto:
            linha, coluna = coordenada
            if self.valida(simbolo, linha, coluna):
                self.tabuleiro[linha][coluna] = simbolo

