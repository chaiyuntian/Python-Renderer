import Vector
import Colour
import Triangle
import IncludesAndConstants

from IncludesAndConstants import *

X = 0
Y = 1
Z = 2
W = 3

R = 0
G = 1
B = 2

##########################################################
#LIGHTING RELATED CLASSES - materials, colours,lights etc#
##########################################################


class Material:
  def __init__(self,ambient,diffuse,specular,shininess):
    self.ambient = ambient
    self.diffuse = diffuse
    self.specular = specular
    self.shininess = shininess


#create components from colour for material
#ambient = Colour.Colour(ambientR,ambientG,ambientB)
#specular = Colour.Colour(specularR,specularG,specularB)
#diffuse = Colour.Colour(diffuseR,diffuseG,diffuseB)

#create a material
#material1 = Material(ambient,specular,diffuse,shininess)

#create the lightpoint

lightPoint = [lightSourceX,lightSourceY,lightSourceZ,1]
  
#diffuse light value calculation

def Diffuse(aNormal,aTrianglePoint):
  lightVec = [ lightPoint[X] - aTrianglePoint[X],
               lightPoint[Y] - aTrianglePoint[Y],
               lightPoint[Z] - aTrianglePoint[Z],
               lightPoint[W] - aTrianglePoint[W]]

  lightVec = Vector.normalize(lightVec)
  #print(lightVec[X],lightVec[Y],lightVec[Z])
  #print(Vector.length(lightVec))
  aNormal = Vector.normalize(aNormal)

  return max(Vector.dotProduct(lightVec,aNormal),0)  

#specular light calculation

def Specular(aNormal,aTrianglePoint):
  eyeVector = [cameraX - aTrianglePoint[X],
               cameraY - aTrianglePoint[Y],
               cameraZ - aTrianglePoint[Z],
               1.0     - aTrianglePoint[3]]

  eyeVector = Vector.normalize(eyeVector)
 
  lightVec = [lightPoint[X] - aTrianglePoint[X],
              lightPoint[Y] - aTrianglePoint[Y],
              lightPoint[Z] - aTrianglePoint[Z],
              lightPoint[W] - aTrianglePoint[W]]
  
  lightVec = Vector.normalize(lightVec)

  #caculate the half vector
  H = [lightVec[X] + eyeVector[X],
       lightVec[Y] + eyeVector[Y],
       lightVec[Z] + eyeVector[Z],
       lightVec[W] + eyeVector[W]]

  #now normalize and dot the half with the normal vec,
  #use the shininess constant defined in IncludesAndConstants.py
  H = Vector.normalize(H)
  d = Vector.dotProduct(aNormal,H)
  return math.pow(max(d,0),shininess)


#calculatecolour - calls all the different functions for ambient, diffuse, spec values
def CalculateColour(aTriangle):

  AmbColour = [0.0,0.0,0.0]
  AmbColour[R] = ambientMatR * ambientLightR
  AmbColour[G] = ambientMatG * ambientLightG
  AmbColour[B] = ambientMatB * ambientLightB

  DiffuseColour = [0.0,0.0,0.0]
  DiffuseFactor = Diffuse(aTriangle.normal,Triangle.AveragePoint(aTriangle))
  #print(DiffuseFactor)

  DiffuseColour[R] = DiffuseFactor * diffuseMatR * lightSourceR
  DiffuseColour[G] = DiffuseFactor * diffuseMatG * lightSourceG
  DiffuseColour[B] = DiffuseFactor * diffuseMatB * lightSourceB
  #print(DiffuseColour[R],DiffuseColour[G],DiffuseColour[B])

  SpecularColour = [0.0,0.0,0.0]
  SpecularFactor = Specular(aTriangle.normal,Triangle.AveragePoint(aTriangle))
  #print(SpecularFactor)

  SpecularColour[R] = SpecularFactor * specularMatR * lightSourceR
  SpecularColour[G] = SpecularFactor * specularMatG * lightSourceG
  SpecularColour[B] = SpecularFactor * specularMatB * lightSourceB
  #print(SpecularColour[R],SpecularColour[G],SpecularColour[B])

  endColour = [0.0,0.0,0.0]
  endColour[R] = AmbColour[R] + DiffuseColour[R] + SpecularColour[R]
  endColour[G] = AmbColour[G] + DiffuseColour[G] + SpecularColour[G]
  endColour[B] = AmbColour[B] + DiffuseColour[B] + SpecularColour[B]
  

  #if >1, clamp the values
  if endColour[R] > 1.0:
    endColour[R] = 1.0

  if endColour[G] > 1.0:
    endColour[G] = 1.0

  if endColour[B] > 1.0:
    endColour[B] = 1.0

  return Colour.Colour(endColour[R],endColour[G],endColour[B])