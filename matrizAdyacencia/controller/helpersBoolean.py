#!/usr/bin/python3
# coding: utf-8

from controller.helpersVectProb import generateMatrixGeneral, convertMatrizGeneralFrecu, readWordEmpty, readDict, readQueryDefault

# funcion que nos permite encontrar la consulta
def consulta(D1, operador, D2):
  aux = {}
  if operador == 'and':
    for k in D1.keys():
      aux[k] = D1[k] and D2[k]
  elif operador == 'or':
    for k in D1.keys():
      aux[k] = D1[k] or D2[k]
  return aux

# metodo que nos pemite imprimir la matriz boolena por consola, por motivos de pruebas
def imprimirMatriz(matriz):
  cabecera = f'{" ": ^10}'
  for value in matriz.values():
    for key in value.keys():
      cabecera += f'{key: ^10}'  
    break
  cuerpo = {}

  for key in matriz.keys():
    cuerpo[key] = ""

  for key, value in matriz.items():
    for key2, value2 in value.items():
      cuerpo[key] += f'{value2: ^10}'
  
  print(cabecera)
  for key, value in cuerpo.items():
    print(f'{key: ^10}',value )


DICT = readDict('data/dict')
DICT['Q'] = readQueryDefault('data/queryDefaultVectProb')
WORDS_EMPTY = readWordEmpty('data/words_empty')

MATRIZ = generateMatrixGeneral(DICT, WORDS_EMPTY)
MATRIZ = convertMatrizGeneralFrecu(MATRIZ)
for k,v in MATRIZ.items():
    del MATRIZ[k]['Q']


def recursividad(listCad):
    n = len(listCad)
    listCad[0] = listCad[0][1::]
    listCad[n-1] = listCad[n-1][:-1:]

    if listCad[0].startswith('(') or listCad[n-1].endswith(')'):
        print('caso recursivo ', listCad)
        if listCad[0].startswith('('):
            return consulta(recursividad(listCad[:-2]),listCad[1],MATRIZ[listCad[n-1]])
        else:
            return consulta(MATRIZ[listCad[0]], listCad[1], recursividad(listCad[2::]) )
    else:
        print('caso base: ', listCad[0], listCad[1], listCad[2])
        return consulta(MATRIZ[listCad[0]], listCad[1], MATRIZ[listCad[2]])
