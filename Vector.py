import math

X = 0
Y = 1
Z = 2
W = 3

###################################################################################################################################
#CLASSES AND UTILITY FUNCTIONS                                                                                                    #
#below are functions, classes used by the main app to create matrices, vectors, etc and things like dot prod, cross prod etc      # 
#and triangles, lists of triangles, reading from files etc, they are grouped by class eg                                          # 
#Vector class is defined and then all the non member functions that use a vector are listed afterwards                            #
###################################################################################################################################



def max(a,b):

  if a > b:
    return a

  else:
    return b

def min(a,b):

  if a < b:
    return a

  else:
    return b

########################
#VECTORCLASS           #
########################

def length(vec):

  len = vec[X] * vec[X] + vec[Y] * vec[Y] + vec[Z] * vec[Z]
  len = math.sqrt(len)  

  return len


def normalize(vec):

  len = length(vec)

  if vec[X] != 0:
    vec[X] = vec[X]/len

  if vec[Y] != 0:
    vec[Y] = vec[Y]/len

  if vec[Z] != 0:
    vec[Z] = vec[Z]/len

  return vec

def dotProduct(vec1,vec2):
  return ((vec1[X] * vec2[X]) + (vec1[Y] * vec2[Y]) + (vec1[Z] * vec2[Z]))

def crossProduct(vec1,vec2):
  i = (vec1[Y] * vec2[Z]) - (vec2[Y] * vec1[Z])

  j = -((vec1[X] * vec2[Z]) - (vec2[X] * vec1[Z]))

  k = (vec1[X] * vec2[Y]) - (vec2[X] * vec1[Y])

  cross = [i,j,k,0]

  cross = normalize(cross)

  return cross
