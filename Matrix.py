#MATRIX.PY - two functions that multiply a vector by a matrix and a matrix by
#a matrix

import Vector

X = 0
Y = 1
Z = 2
W = 3



def VectorMatrixMult(Vec,aMatrix):
  row = 0
  col = 0
  total = 0
  newList = []
  while row < 4:
    while col < 4:
      total += Vec[col] * aMatrix[col][row]
      col = col + 1
    newList.append(total)
    row = row + 1
    col = 0
    total = 0
  return [newList[X],newList[Y],newList[Z],newList[W]]



def MatrixMatrixMult(aMatrix1,aMatrix2):
  row = 0
  col = 0
  elem = 0
  newList1 = []
  newList2 = []
  while row < 4:
    while elem < 4:
      total = 0
      while col < 4:
        total += aMatrix1[row][col] * aMatrix2[col][elem]
        col += 1
      newList1.append(total)
      col = 0
      elem += 1
    newList2.append(newList1)
    newList1 = []
    row += 1
    elem = 0
  return newList2
     