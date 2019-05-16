#!/usr/bin/python3
# coding: utf-8
import math
from collections import  OrderedDict

# funcion que nos permite leer de un archivo el Diccionario
def readDict(file):
    data = {}
    f = open(file, encoding='utf-8')
    c = 0
    for line in f:
        c += 1
        data[f'D{c}'] = line.strip()

    return data

# funcion que nos permite leer de un archivo una consulta por defecto
def readQueryDefault(file):
    f = open(file, encoding='utf-8')
    return f.readline().strip()

# funcion que nos permite leer de un archivo la lista de palabras vacias
def readWordEmpty(file):
    listWords = []
    f = open(file, encoding='utf-8')
    for word in f:
        listWords.append(word.strip())
    return listWords

# funcion que elimina palabras vacias de nuestro diccionario
def deleteWordsEmpty(word, WORD_EMPTY):
    wordFinal = []
    for i in word.lower().split(' '):
        if not (i in WORD_EMPTY):
            wordFinal.append(i)
    return wordFinal

# funcion que convierte nuestro diccionario en una matriz con los datos basicos, para la una mejor organizacion
def generateMatrixGeneral(words, WORD_EMPTY):
    matrix = {}
    for DK, DN in words.items():
        for word in deleteWordsEmpty(DN, WORD_EMPTY):
            matrix[word] = {}

    for DK, DN in words.items():
        for word in deleteWordsEmpty(DN, WORD_EMPTY):
            matrix[word][DK] = 0

    for DK, DN in words.items():
        for word in deleteWordsEmpty(DN, WORD_EMPTY):
            matrix[word][DK] += 1
    return matrix

# funcion que convierte nuestra matriz base en una de tipo vetorial
def generateMatrixVectorial(matrixGeneral):

    # generamos la lista de todos los documentos
    dictD = {}
    matrixGeneral = dict(matrixGeneral)
    print(matrixGeneral)

    for w in matrixGeneral.values():
        for k in w.keys():
            dictD[k] = None
    # generamos la matriz base vectorial
    matrixVectorial = {}
    for generalKey, generalValue in matrixGeneral.items():
        matrixVectorial[generalKey] = {}
        for dictKey, dictValue in dictD.items():
            matrixVectorial[generalKey][dictKey] = 0

    # llenamos los datos a la matriz vectorial, con los de la matriz general
    for generalKey, generalValue in matrixGeneral.items():
        for key, value in generalValue.items():
            matrixVectorial[generalKey][key] = value

    # calculamos los datos del IDF en un diccionario para cada elemento.
    dictIDF = {}
    for key, value in matrixGeneral.items():
        aux2 = 0
        for k in value.keys():
            if k != 'Q':
                aux2 += 1
        aux =  (len(dictD.values()) - 1) / aux2 if aux2>0  else 0

        dictIDF[key] = math.log(aux, 10) if aux != 0 else 0

    # calculamos la nueva matriz vectorial con el IDF
    for vectorialKey, vectorialValue in matrixVectorial.items():
        for key, value in vectorialValue.items():
            matrixVectorial[vectorialKey][key] = value * dictIDF[vectorialKey]

    return matrixVectorial

# funcion que rellena los datos vacios de la matriz general con ceros y la convierte a binaria
def convertMatrizGeneralBinaria(matrixGeneral):
    # generamos la lista de todos los documentos
    dictD = {}
    matrixGeneral = dict(matrixGeneral)
    for w in matrixGeneral.values():
        for k in w.keys():
            dictD[k] = None

    # generamos toda la matriz
    matrixVectorial = {}
    for generalKey, generalValue in matrixGeneral.items():
        matrixVectorial[generalKey] = {}
        for dictKey, dictValue in dictD.items():
            matrixVectorial[generalKey][dictKey] = 0

    for generalKey, generalValue in matrixGeneral.items():
        for dictKey, dictValue in generalValue.items():
            matrixVectorial[generalKey][dictKey] = 1 if matrixGeneral[generalKey][dictKey] >= 1 else 0
    return matrixVectorial

# funcion que rellena los datos vacios de la matriz general con ceros y la convierte a una de frecuencia
def convertMatrizGeneralFrecu(matrixGeneral):

    # generamos la lista de todos los documentos
    dictD = {}
    matrixGeneral = dict(matrixGeneral)
    for w in matrixGeneral.values():
        for k in w.keys():
            dictD[k] = None

    # generamos toda la matriz
    matrixVectorial = {}
    for generalKey, generalValue in matrixGeneral.items():
        matrixVectorial[generalKey] = {}
        for dictKey, dictValue in dictD.items():
            matrixVectorial[generalKey][dictKey] = 0

    for generalKey, generalValue in matrixGeneral.items():
        for dictKey, dictValue in generalValue.items():
            matrixVectorial[generalKey][dictKey] = matrixGeneral[generalKey][dictKey]

    return matrixVectorial

# metodo que nos pemite hayar la silititud
def calculateSim(matrixVectorial):
    aux = {}
    dictD = {}
    for w in matrixVectorial.values():
        for k in w.keys():
            dictD[k] = None

    for D in dictD.keys():
        aux[D] = 0
        for element in matrixVectorial.keys():
            aux[D] += (matrixVectorial[element][D] * matrixVectorial[element]['Q'])
    del aux['Q']
    return OrderedDict(sorted(aux.items(), key=lambda t: t[1], reverse=True))

