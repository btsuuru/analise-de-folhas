from copy import copy
import time
import cv2
import numpy as np
from datetime import datetime

#      Escruro   Claro
# R    60        101
# G    70        109
# B    33        58

# [linha : coluna]
# [-1 : -1] [-1 : 0] [-1 : +1]
# [0 : -1]  [0 : 0]  [0: +1]
# [+1 : -1] [+1 : 0] [+1 : +1]

#########################
#   PRE-PROCESSAMENTO   #
#########################

def swap(vetor, p1, p2):
    aux = vetor[p1]
    vetor[p1] = vetor[p2]
    vetor[p2] = aux
    return vetor

def getAvg(obj):
    return int(sum(obj)/2)

def getSubImagem(img, i, ii):
    amostra = []
    amostra.append(img[i-1][ii-1])
    amostra.append(img[i-1][ii])
    amostra.append(img[i-1][ii+1])
    amostra.append(img[i][ii-1])
    amostra.append(img[i][ii])
    amostra.append(img[i][ii+1])
    amostra.append(img[i+1][ii-1])
    amostra.append(img[i+1][ii])
    amostra.append(img[i+1][ii+1])
    return amostra

def mediana(img):
    for i in range(1, len(img)-1):
        for ii in range(1, len(img[i])-1):
            amostra = getSubImagem(img, i, ii)
            #auxiliar = list(map(getAvg, amostra))
            for a in range(len(amostra)):
                for b in range(a, len(amostra)):
                    #if auxiliar[a] > auxiliar[b]:
                    if amostra[a] > amostra[b]:
                        #swap(auxiliar, a, b)
                        swap(amostra, a, b)
            img[i][ii] = amostra[int(len(amostra)/2)]
    return img

def tiraFundo(img):
    # Escala minima para ser reconhecida e pintada.
    # OBS: escala maxima = [255, 255, 255]
    corMinima = 150
    for i in range(largura):
        # Pinta de cima para baixo
        for ii in range(altura):
            if img[ii][i] >= corMinima:
                img[ii][i] = corFundo
            else:
                break
        # Pinta de baixo para cima
        for ii in reversed(range(altura)):
            if img[ii][i] >= corMinima:
                img[ii][i] = corFundo
            else:
                break
    return img

def limiarizar(img):
    corMinima = 1
    corMaxima = 170 # 145
    preto = 0
    for i in range(altura):
        for ii in range(largura):
            if corMinima <= img[i][ii] <= corMaxima:
                img[i][ii] = corMeio
            elif img[i][ii] != preto and not (corMinima <= img[i][ii] <= corMaxima):
                img[i][ii] = corBuraco
    return img


def pintaMeio(img):
    for i in range(altura):
        direita = copy(largura-1)
        esquerda = 0
        while esquerda < largura and img[i][esquerda] == 0:
            esquerda += 1
        while direita > 0 and img[i][direita] == 0:
            direita -= 1
        if esquerda < direita:
            meio = int((esquerda + direita)/2)
            img[i][meio] = corLinha
    return img

'''
    ultimoX = copy(x)
    ultimoY = copy(y)
    for i in range(x+1, altura): 
        for ii in range(largura):
            if img[i][ii] == corLinha:
                img[i][ii] = 100
                dist = ultimoY - ii
                print("Ponto Anterior", ultimoY)
                print("Atual", ii)
                print("Distancia", dist)
                #ultimoY = ii
                img[i][dist+ultimoY] = 20'''

def distanciaDaBorda(img, x, y):
    contador = 0
    while True:
        if img[x][y]!=0:
            contador += 1
            y -= 1
        else:
            return contador

def refazLinha(img, x, y, bicoX, bicoY):
    for i in range(bicoX, x, -1):
        for ii in range(largura):
            if corLinha-10 <= img[i][ii] <= corLinha+10:
                img[i][ii]=255
                db = distanciaDaBorda(img,i,ii)
                distancia = bicoY - ii
                img[i][bicoY+distancia]=100
                db = distanciaDaBorda(img,i,ii)
                print(db)
                try:
                    for iii in range((bicoY+distancia), (bicoY+db)):
                        if img[i][iii]!=255:
                            img[i][iii] = corBuraco
                except:
                    return img
    return img

def achaBico(img, x, y):
    for i in range(altura-1, x, -1):
        for ii in range(largura):
            if corLinha-10 <= img[i][ii] <= corLinha+10:
                img[i][ii] = 230
                return refazLinha(img, x, y, i, ii)
    return img

def segueLinha(img, x, y):
    if corLinha+10 >= img[x+1][y-2] >= corLinha-10:
        img =  segueLinha(img, x+1, y-2)
    elif corLinha+10 >= img[x+1][y-1] >= corLinha-10:
        img = segueLinha(img, x+1, y-1)
    elif corLinha+10 >= img[x+1][y] >= corLinha-10:
        img = segueLinha(img, x+1, y)
    elif corLinha+10 >= img[x+1][y+1] >= corLinha-10:
        img = segueLinha(img, x+1, y+1)
    elif corLinha+10 >= img[x+1][y+2] >= corLinha-10:
        img = segueLinha(img, x+1, y+2)
    else:
        #img[x][y] = 120
        img = achaBico(img, x, y)
    return img

def achaLinha(img):
    for i in range(altura):
        for ii in range(largura):
            if img[i][ii] == corLinha:
                img[i][ii]=100
                img = segueLinha(img, i, ii)
                return img

if __name__ == '__main__':
    img = cv2.imread('C:\\Users\\User\\Desktop\\Camera SlowMotion\\Materiais de Estudo\\Folhas\\soja.png',0)
    #img = cv2.imread('C:\\Users\\User\\Desktop\\Camera SlowMotion\\Materiais de Estudo\\Folhas\\amostra2.jpg',0)
    # define variaveis globais
    global largura, altura, corFundo, corMeio, corBuraco, corLinha
    largura = len(img[0])
    altura = len(img)
    corFundo = 0
    corMeio = 255
    corBuraco = 170
    corLinha = 50
    tempoTotal = 0
    #kernel = np.ones((5,5),np.float32)/25
    ###############################
    # PRE-PROCESSAMENTO DE IMAGEM #
    ###############################
    #
    # APLICA FILTRO DE MEDIANA
    #
    inicio = int(round(time.time() * 1000))
    img = mediana(img)
    #img = cv2.medianBlur(img, 5)
    fim = int(round(time.time() * 1000))
    tempoTotal += fim-inicio
    print("Mediana: ", (fim-inicio),"ms.")
    #
    # TIRA BACKGROUND
    #
    inicio = int(round(time.time() * 1000))
    img = tiraFundo(img)
    fim = int(round(time.time() * 1000))
    tempoTotal += fim-inicio
    print("Tira Fundo: ", (fim-inicio), "ms.")
    #
    # LIMIARIZA IMAGEM
    #
    inicio = int(round(time.time() * 1000))
    img = limiarizar(img)
    #a, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    fim = int(round(time.time() * 1000))
    tempoTotal += fim-inicio
    print("Limiarizar: ", (fim-inicio),"ms.")
    #
    # DESENHA A LINHA NO MEIO DA FOLHA
    #
    inicio = int(round(time.time() * 1000))
    img = pintaMeio(img)
    fim = int(round(time.time() * 1000))
    tempoTotal += fim-inicio
    print("Pinta Meio: ", (fim-inicio),"ms.")
    #
    # PERCORRE A LINHA
    #
    inicio = int(round(time.time() * 1000))
    img = achaLinha(img)
    fim = int(round(time.time() * 1000))
    tempoTotal += fim-inicio
    print("Acha Linha: ", (fim-inicio),"ms.")
    #
    # FIM
    #
    print("Tempo total: ", round(tempoTotal/1000, 2), "s.")
    arquivo = "C:\\Users\\User\\Desktop\\Camera SlowMotion\\Materiais de Estudo\\Folhas\\{0}.jpg".format(datetime.now().strftime("%d%b%Hh%Mm"))
    cv2.imwrite(arquivo, img)
    cv2.imshow("Folha", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()