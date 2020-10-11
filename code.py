#!python3
import symengine
import numpy as np
from numpy import linalg
import seaborn as sns
import sympy as sym
import pandas as pd

while True:
    try:
        jn = int(input('Masukkan node yang diinginkan (n x n): ')) #jumlah node
        up = float(input('Masukkan temperatur atas: '))
        dn = float(input('Masukkan temperatur bawah: '))
        le = float(input('Masukkan temperatur kiri: '))
        ri = float(input('Masukkan temperatur kanan: '))
        break
    except:
        print('Mohon masukkan angka yang benar!')

maps = np.zeros(shape=(jn+2,jn+2), dtype=object) #bikin matrix kosong, size jn+2 x jn+2
#luaran matrixnya itu buat suhunya.

maps[0, :] = up
maps[:, 0] = le
maps[jn+1,:] = dn
maps[:,jn+1] = ri
maps[0, 0] = 0
maps[0,jn+1] = 0
maps[jn+1,0] = 0
maps[jn+1,jn+1] = 0

mapSymbols = '' #dipake buat operasi sympy nya nanti

n = 0
for i in range(0, jn):
    for j in range(0, jn):
        maps[i+1,j+1] = 'x' + str(i+j+n) #penambahan x0 x1 blabla
        mapSymbols += (maps[i+1,j+1]) + ',' #nambahin x0 blablablanya ke mapSymbols
    n += (jn-1)

mapSymbolsList = list(mapSymbols.split(',')) #ngejadiin mapSymbols jadi list buat for loop

mapSolving = sym.symbols(mapSymbols[:len(mapSymbols)-1]) #ngasi list symbols buat fungsi sym

eqList = []
n = 0
for i in range(0, jn):
    for j in range(0, jn):
        value1 = symengine.sympify(maps[i, j+1])
        value2 = symengine.sympify(maps[i+1, j])
        value3 = symengine.sympify(maps[i+2, j+1])
        value4 = symengine.sympify(maps[i+1, j+2])
        equation = symengine.Eq(value1 + value2 + value3 + value4 - 4*symengine.sympify(mapSymbolsList[i+j+n]), 0)
        eqList.append(equation)
    n += (jn-1)

#ngejadiin persamaan linearnya ke matrix, trus diconvert jadi array numpy
symatA, symatB = sym.linear_eq_to_matrix(eqList, mapSolving)
matA = np.array(symatA, dtype=float)
matB = np.array(symatB, dtype=float)

#numpy magic bby
solution = linalg.solve(matA,matB)

#updating the original array
n = 0
for i in range(0, jn):
    for j in range(0, jn):
        maps[i+1,j+1] = solution[i+j+n]
    n += (jn-1)

result = np.array(maps, dtype=float)
sns.heatmap(result[1:jn+1, 1:jn+1])

resultPd = pd.DataFrame(result)
filepath = str(input('Masukkan nama file Excel: ')) + '.xlsx'

resultPd.to_excel(filepath, index=False)
