#!python3
import symengine, sympy as sym, pandas as pd, seaborn as sns, numpy as np
from numpy import linalg

"""The first part of the code will ask the user to input data."""
while True:
    try:
        node = int(input('Input node: '))
        upperTemp = float(input('Input upper temperature: '))
        lowerTemp = float(input('Input lower temperature: '))
        leftTemp  = float(input('Input left temperature: '))
        rightTemp = float(input('Input right temperature: '))
        break
    except:
        print('Please input a number.')
    
"""The second part of the code is to initialize a matrix (node+2) x (node+2) sized, filled with zeros."""
"""The matrix is then filled with user data inputted from the first part."""
nodeMatrix = np.zeros(shape=(node+2,node+2), dtype=object)
    
nodeMatrix[0, 1:node+1] = upperTemp
nodeMatrix[1:node+1, 0] = leftTemp
nodeMatrix[node+1,1:node+1] = lowerTemp
nodeMatrix[1:node+1, node+1] = rightTemp

"""The third part of the code is to fill the remaining zeros with different variables."""
nodeMatrixSymbols = ''

n = 0
for i in range(0, node):
    for j in range(0, node):
        nodeMatrix[i+1,j+1] = 'x' + str(i+j+n)
        nodeMatrixSymbols += (nodeMatrix[i+1,j+1]) + ','
    n += (node-1)

"""The fourth part of the code is to calculate the variables."""
"""This is achieved by first making (node)^2 linear equations, and then converting the equations into two matrices."""
"""The matrices can then be solved using inverse matrix method. AB = X --> A'X = B"""
nodeMatrixSymbolsList = list(nodeMatrixSymbols.split(','))

nodeMatrixSolving = sym.symbols(nodeMatrixSymbols[:len(nodeMatrixSymbols)-1])

eqList = []
n = 0
for i in range(0, node):
    for j in range(0, node):
        value1 = symengine.sympify(nodeMatrix[i, j+1])
        value2 = symengine.sympify(nodeMatrix[i+1, j])
        value3 = symengine.sympify(nodeMatrix[i+2, j+1])
        value4 = symengine.sympify(nodeMatrix[i+1, j+2])
        equation = symengine.Eq(value1 + value2 + value3 + value4 - 4*symengine.sympify(nodeMatrixSymbolsList[i+j+n]), 0)
        eqList.append(equation)
    n += (node-1)

symatA, symatB = sym.linear_eq_to_matrix(eqList, nodeMatrixSolving)
matA = np.array(symatA, dtype=float)
matB = np.array(symatB, dtype=float)

solution = linalg.solve(matA,matB)

"""The fifth part of the code is to replace the variables in the original matrix into the result from the solved equations."""
n = 0
for i in range(0, node):
    for j in range(0, node):
        nodeMatrix[i+1,j+1] = solution[i+j+n]
    n += (node-1)

"""The sixth part of the code is to plot the original matrix into a heatmap."""
result = np.array(nodeMatrix, dtype=float)
sns.heatmap(result[1:node+1, 1:node+1])

"""The seventh part of the code is to ask the user if they want to export the data to Excel."""
saveYes = str.lower(input('Save data to Excel? (y/n): '))
if 'y' in saveYes:
    resultPd = pd.DataFrame(result)
    filepath = str(input('Name the Excel file: ')) + '.xlsx'
    resultPd.to_excel(filepath, index=False)
