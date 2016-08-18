import random
import math
import heapq
import time

#BLOCO DE CLASSES DO ESTADO E VARIÁVEIS
listaVertice = []
entradaDeDados = []
sequenciaDePassos = []
populacao = []
listaCruamento = []
tamanhoPopulacao = 10
numeroTentativas = 0
melhorouSolucao = True

class Vertice:
    def __init__(self, numero, cordenadaX, cordenadaY):
      self.numero = numero
      self.cordenadaX = cordenadaX
      self.cordenadaY = cordenadaY

class Solucao:
    caminho = []
    aptidao = -1

    def __lt__(self, other):
        return self.custo() < other.custo()

    def custo(self):
        global listaVertice
        if (self.aptidao == -1):
            soma = 0
            for i in range(tamanhoConjunto - 1):
                v1 = listaVertice[self.caminho[i] - 1]
                v2 = listaVertice[self.caminho[i + 1] - 1]
                soma += math.sqrt(((v1.cordenadaX - v2.cordenadaX) ** 2) +
                                  ((v1.cordenadaY - v2.cordenadaY) ** 2))
            v1 = listaVertice[self.caminho[0] - 1]
            v2 = listaVertice[self.caminho[tamanhoConjunto - 1] -1]
            soma += math.sqrt(((v1.cordenadaX - v2.cordenadaX) ** 2) +
                              ((v1.cordenadaY - v2.cordenadaY) ** 2))
            self.aptidao = soma
        return self.aptidao

tamanhoConjunto = int(input())
for i in range(tamanhoConjunto):
    entrada = input()
    entradaDeDados.append(entrada)

for i in range(tamanhoConjunto):
    vList = entradaDeDados[i].split()
    vertice = Vertice(int(vList[0]), float(vList[1]), float(vList[2]))
    listaVertice.append(vertice)

for i in range(1, tamanhoConjunto + 1):
    sequenciaDePassos.append(i)

#BLOCO DEFINIÇÃO DAS FUNÇOES
def geraPopulacao():
    global populacao
    
    for i in range(tamanhoPopulacao):
        solucao = Solucao()
        solucao.caminho = sequenciaDePassos[:]
        random.shuffle(solucao.caminho)
        heapq.heappush(populacao, solucao)
        
    return populacao
    
def selecionaRota(pPopulacao):
    vRandom1 = random.randrange(tamanhoPopulacao//2)
    vRandom2 = random.randrange(tamanhoPopulacao//2)

    if pPopulacao[vRandom1].custo() < pPopulacao[vRandom2].custo():
        return pPopulacao[vRandom1].caminho
    else:
        return pPopulacao[vRandom2].caminho

def geraCruzamento(pSolucaoA, pSolucaoB):
    global tamanhoPopulacao
    global tamanhoConjunto
    
    listaCruzamento = []
    contador = 0
    qtGeracoes = int(tamanhoPopulacao * 0.8)
    tamanhoCorte = int(tamanhoConjunto * 0.95)
    while contador < qtGeracoes:

        novoCaminho = pSolucaoA[:tamanhoCorte]
        qtAdicionados = 0
        for i in pSolucaoB:
            if qtAdicionados == (tamanhoConjunto - tamanhoCorte):
                break
            if i not in novoCaminho:
                novoCaminho.append(i)
                qtAdicionados += 1

        novoCaminho = mutacaoCaminho(novoCaminho) #Mutação
        cruzamento = Solucao()
        cruzamento.caminho = novoCaminho
        cruzamento = buscaLocal(cruzamento) #Busca Local - First Improvement
        listaCruzamento.append(cruzamento)
        contador += 1

    return listaCruzamento
    
def mutacaoCaminho(pCaminho):
    p1 = random.randrange(tamanhoConjunto - 1)
    p2 = random.randrange(p1, tamanhoConjunto - 1)
    pCaminho[p1], pCaminho[p2] = pCaminho[p2], pCaminho[p1]
    return pCaminho
    
def geraVizinho(pCaminho, pContador):
    caminho = pCaminho[:]
    (caminho[pContador], caminho[pContador +1]) = (caminho[pContador +1], caminho[pContador])
    return caminho

def buscaLocal(pCruzamento):
    i = 0
    vizinho = Solucao()
    for i in range(tamanhoConjunto//2):
        vizinho.caminho = geraVizinho(pCruzamento.caminho, i)
        if vizinho.custo() < pCruzamento.custo():
            pCruzamento = vizinho
            break

    return pCruzamento

def atualizaPopulacao(pPopulacao, pListaCruzamento):
    global melhorouSolucao
    global numeroTentativas

    for cruzamento in pListaCruzamento:
        maior = heapq.nlargest(1, pPopulacao)[0]
        menor = pPopulacao[0]

        custoCruzamento = cruzamento.custo()
        if (custoCruzamento < maior.custo()):
            pPopulacao.remove(maior)
            heapq.heappush(pPopulacao, cruzamento)
            heapq.heapify(pPopulacao)
            
            if (custoCruzamento < menor.custo()):
                numeroTentativas = 0
            else:
                numeroTentativas += 1
        else:
            numeroTentativas += 1

        if (numeroTentativas == 700):
            melhorouSolucao = False

    return pPopulacao
        
def obtemMenor(pPopulacao):
    return pPopulacao[0].custo()

#BLOCO PROGRAMA PRINCIPAL
populacao = geraPopulacao()
while (melhorouSolucao):
    #Avaliação e Seleção
    solucaoA = selecionaRota(populacao)
    solucaoB = selecionaRota(populacao)

    #Cruzamento
    listaCruamento = geraCruzamento(solucaoA, solucaoB)

    #Atualização - Elitismo
    populacao = atualizaPopulacao(populacao, listaCruamento)

print(obtemMenor(populacao))
