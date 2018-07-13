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
            auxiliar = list(map(getAvg, amostra))
            for a in range(len(amostra)):
                for b in range(a, len(amostra)):
                    if auxiliar[a] > auxiliar[b]:
                        swap(auxiliar, a, b)
                        swap(amostra, a, b)
            img[i][ii] = amostra[int(len(amostra)/2)]
    return img

def tiraFundo(img):
    # Escala minima para ser reconhecida e pintada.
    # OBS: escala maxima = [255, 255, 255]
    corMinima = np.array([150, 150, 150])
    for i in range(largura):
        # Pinta de cima para baixo
        for ii in range(altura):
            if img[ii][i][0] >= corMinima[0] and img[ii][i][1] >= corMinima[1] and img[ii][i][2] >= corMinima[2]:
                img[ii][i] = np.array([0, 0, 0])
            else:
                break
        # Pinta de baixo para cima
        for ii in reversed(range(altura)):
            if img[ii][i][0] >= corMinima[0] and img[ii][i][1] >= corMinima[1] and img[ii][i][2] >= corMinima[2]:
                img[ii][i] = np.array([0, 0, 0])
            else:
                break
    return img

'''
def pintaMeio(img):
    for i in range(altura):
        img[i][int(largura / 2)] = np.array([0, 0, 255])
    return img
'''

def limiarizar(img):
    #corMinima = np.array([33, 70, 60])
    corMinima = np.array([0, 23, 3])
    #corMaxima = np.array([58, 109, 101])
    corMaxima = np.array([116, 218, 202])
    preto = np.array([0, 0, 0])
    for i in range(altura):
        for ii in range(largura):
            if corMinima[0] <= img[i][ii][0] <= corMaxima[0] and corMinima[1] <= img[i][ii][1] <= corMaxima[1] and corMinima[2] <= img[i][ii][2] <= corMaxima[2]:
                img[i][ii] = np.array([127, 127, 127])
            elif img[i][ii][0] != preto[0] and img[i][ii][1] != preto[1] and img[i][ii][2] != preto[2]:
                img[i][ii] = np.array([0,255,0])
    return img


def pintaMeio(img):
    for i in range(altura):
        direita = copy(largura-1)
        esquerda = 0
        while(esquerda < largura and img[i][esquerda][0] == 0 and img[i][esquerda][1] == 0 and img[i][esquerda][2] == 0):
            esquerda += 1
        while(direita > 0 and img[i][direita][0] == 0 and img[i][direita][1] == 0 and img[i][direita][2] == 0):
            direita -= 1
        if esquerda < direita:
            meio = int((esquerda + direita)/2)
            img[i][meio] = np.array([0,0,255])
    return img

'''
        while esquerda <= direita:
            media = int((esquerda + direita)/2)
            if img[i][esquerda] != np.array([0,0,0])
            esquerda += 1
            direita -= 1
'''

def identificaBuraco(img):
    meio = int(altura / 2)
    for i in range(largura):
        for ii in range(meio):
            pass


if __name__ == '__main__':
    img = cv2.imread('C:\\Users\\User\\Desktop\\Camera SlowMotion\\Materiais de Estudo\\Folhas\\amostra2.jpg')
    # define variaveis globais
    global largura
    global altura
    largura = len(img[0])
    altura = len(img)
    #kernel = np.ones((5,5),np.float32)/25
    # PRE-PROCESSAMENTO DE IMAGEM
    inicio = int(round(time.time() * 1000))
    img = mediana(img)
    #img = cv2.medianBlur(img, 5)
    fim = int(round(time.time() * 1000))
    print("Mediana: ", (fim-inicio)," ms.")
    inicio = int(round(time.time() * 1000))
    img = tiraFundo(img)
    fim = int(round(time.time() * 1000))
    print("Tira Fundo: ", (fim-inicio)," ms.")
    inicio = int(round(time.time() * 1000))
    img = pintaMeio(img)
    fim = int(round(time.time() * 1000))
    print("Pinta Meio: ", (fim-inicio)," ms.")
    inicio = int(round(time.time() * 1000))
    img = limiarizar(img)
    #a, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    fim = int(round(time.time() * 1000))
    print("Limiarizar: ", (fim-inicio)," ms.")
    arquivo = "C:\\Users\\User\\Desktop\\Camera SlowMotion\\Materiais de Estudo\\Folhas\\{0}.jpg".format(datetime.now().strftime("%d%b%Hh%Mm"))
    cv2.imwrite(arquivo, img)
    cv2.imshow("Folha", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()