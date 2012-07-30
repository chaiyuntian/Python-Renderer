import Vector
import pygame
import Matrix
import IncludesAndConstants

from pygame import *

#CONSTANT VALUES - used for element access in a point - since it is an array

X = 0
Y = 1
Z = 2
W = 3

#Constant values for RGB access

R = 0
G = 1
B = 2

##############################################################################
#EDGE CLASS - represents a 2D edge rendered to the screen using the          #
#Ax + By + C = 0 equation. This is used later to see if a pixel is within a  #
#Triangle or not                                                             #
##############################################################################

class Edge:
  def __init__(self,x1,y1,x2,y2):
    self.A = y1 - y2
    self.B = x2 - x1
    self.C = (x1*y2) - (x2*y1)
   
#Min and Max functions that find the minimum and maximum points out of three
#passed in points

def min(a,b,c):
  if a <= b and a <= c:
    return a
  if b <= a and b <= c:
    return b
  if c <= a and c <= b:
    return c

def max(a,b,c):
  if a >= b and a >= c:
    return a
  if b >= a and b >= c:
    return b
  if c >= a and c >= b:
    return c


#################################################################################
#TRIANGLE CLASS - has three points with a x,y,z coord each,a colour, a normal   #
#and a bounding box that contains the triangle for rendering                    #
#################################################################################

class Triangle:
  def __init__(self,p1,p2,p3,colour):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3

    self.AveragePoint = []
    self.normal = [0,0,0,0]
    self.colour = colour

    #define the bounding box used 
    self.boundingboxTopLeftX = min(p1[X],p2[X],p3[X])
    self.boundingboxTopLeftY = min(p1[Y],p2[Y],p3[Y])
    self.boundingboxBottomRightX = max(p1[X],p2[X],p3[X])
    self.boundingboxBottomRightY = max(p1[Y],p2[Y],p3[Y])

    #define the three edges using the point values
    self.edge1 = Edge(p1[X],p1[Y],p2[X],p2[Y])
    self.edge2 = Edge(p2[X],p2[Y],p3[X],p3[Y])
    self.edge3 = Edge(p3[X],p3[Y],p1[X],p1[Y])

    #print statements used for debugging
    #print("top left",self.boundingboxTopLeftX,self.boundingboxTopLeftY)
    #print("bottom right",self.boundingboxBotRightX,self.boundingboxBotRightX)


############################################################################
#MultiplyTriangle(aTriangle,aMatrix) - takes a triangle and a transformation
#matrix to transform the 3 points in the triangle,returns the newly transformed
#triangle
############################################################################

def MultiplyTriangle(aTriangle,aMatrix):
  aTriangle.p1 = Matrix.VectorMatrixMult(aTriangle.p1,aMatrix)
  aTriangle.p2 = Matrix.VectorMatrixMult(aTriangle.p2,aMatrix)
  aTriangle.p3 = Matrix.VectorMatrixMult(aTriangle.p3,aMatrix)
  return Triangle(aTriangle.p1,aTriangle.p2,aTriangle.p3,aTriangle.colour)


###########################################################################
#ConvertToInts(aTriangle) - casts all of the float values for the points
#for easy rendering into 2D
###########################################################################

def ConvertToInts(aTriangle):
  aTriangle.p1[X] = int(aTriangle.p1[X])
  aTriangle.p1[Y] = int(aTriangle.p1[Y])
  aTriangle.p1[Z] = int(aTriangle.p1[Z])
  aTriangle.p1[W] = int(aTriangle.p1[W])

  aTriangle.p2[X] = int(aTriangle.p2[X])
  aTriangle.p2[Y] = int(aTriangle.p2[Y])
  aTriangle.p2[Z] = int(aTriangle.p2[Z])
  aTriangle.p2[W] = int(aTriangle.p2[W])

  aTriangle.p3[X] = int(aTriangle.p3[X])
  aTriangle.p3[Y] = int(aTriangle.p3[Y])
  aTriangle.p3[Z] = int(aTriangle.p3[Z])
  aTriangle.p3[W] = int(aTriangle.p3[W])
  return Triangle(Vector(aTriangle.p1[X],aTriangle.p1[Y],aTriangle.p1[Z],aTriangle.p1[W]),
    Vector(aTriangle.p2[X],aTriangle.p2[Y],aTriangle.p2[Z],aTriangle.p2[W]),
    Vector(aTriangle.p3[X],aTriangle.p3[Y],aTriangle.p3[Z],aTriangle.p3[W]))

################################################################################
#CreateTransformedNormal(aTriangle) - this creates the normal vector for a 
#triangle AFTER the triangle has been transformed so that no matrix inversion
#is necessary for normal transforms
################################################################################


def CreateTransformedNormal(aTriangle):

  vec1 = [aTriangle.p1[X] - aTriangle.p2[X],aTriangle.p1[Y] - aTriangle.p2[Y],
          aTriangle.p1[Z] - aTriangle.p2[Z]]

  vec2 = [aTriangle.p3[X] - aTriangle.p2[X],aTriangle.p3[Y] - aTriangle.p2[Y],
          aTriangle.p3[Z] - aTriangle.p2[Z]]

  aTriangle.normal = Vector.crossProduct(vec2,vec1)

  return aTriangle.normal


################################################################################
#TestForCull(aTriangle) - takes a triangle and performs a dot product between
#a vector from the current camera position to the look point (look vector)
#and the triangle's normal to see if it is facing away from
#the camera
############################################################################### 

def TestForCull(aTriangle):
  camVector = [IncludesAndConstants.lookPointX - IncludesAndConstants.cameraX,
               IncludesAndConstants.lookPointY - IncludesAndConstants.cameraY,
               IncludesAndConstants.lookPointZ - IncludesAndConstants.cameraZ,0]

  camVector = Vector.normalize(camVector)

  normal = [aTriangle.normal[X],aTriangle.normal[Y],aTriangle.normal[Z],0]
  normal = Vector.normalize(normal)

  if Vector.dotProduct(camVector,normal) <= 0.0:
    return True
  else:
    return False


##############################################################################
#AveragePoint(aTriangle) - returns the average point within a triangle
##############################################################################

def AveragePoint(aTriangle):
  x = (aTriangle.p1[X] + aTriangle.p2[X] + aTriangle.p3[X])/3.0
  y = (aTriangle.p1[Y] + aTriangle.p2[Y] + aTriangle.p3[Y])/3.0
  z = (aTriangle.p1[Z] + aTriangle.p2[Z] + aTriangle.p3[Z])/3.0
  return [x,y,z,1.0]


##############################################################################
#IsInTriangle - given a triangle and an x,y coordinate, tests if the point is 
#within the triangle, if so it gets rendered to the screen
##############################################################################

def IsInTriangle(aTriangle,x,y):
  A1 = aTriangle.edge1.A
  B1 = aTriangle.edge1.B
  C1 = aTriangle.edge1.C

  A2 = aTriangle.edge2.A
  B2 = aTriangle.edge2.B
  C2 = aTriangle.edge2.C

  A3 = aTriangle.edge3.A
  B3 = aTriangle.edge3.B
  C3 = aTriangle.edge3.C
  
  if ((A1 * x) + (B1 * y) + C1) >= 0:
    return False
  if ((A2 * x) + (B2 * y) + C2) >= 0:
    return False
  if ((A3 * x) + (B3 * y) + C3) >= 0:
    return False
  
  return True
  
################################################################################
#TestPixels(aTriangle,y,colour,surface)-
#given a triangle and a y value in a bounding box, go from x to y and test if
#the pixel is within the box using the above function
################################################################################

def TestPixels(aTriangle,y,colour,surface):
  #get the start x coord
  startX = aTriangle.boundingboxTopLeftX
  if startX < 0:
    startX = 0
  endX = aTriangle.boundingboxBottomRightX
  if endX > 640:
    endX = 640
  while startX < endX:
    if IsInTriangle(aTriangle,startX,y) == True:

      #if in the triangle draw it to the surface using the appropriate colour
      #colors are stored in a range from 0 to 1.0, so multiply by 255
      #to get the pixel col val

      pygame.gfxdraw.pixel(surface,int(startX),int(y),
      pygame.Color(int(colour[0] * 255),int(colour[1] *255),
      int(colour[2] * 255),255))

    #increment x value
    startX += 1


##############################################################################
#drawTriangle(aTriangle,surface,colour)-
#given a triangle, a surface and a colour draw the triangle using tests
#############################################################################

def drawTriangle(aTriangle,surface,colour):
  startY = aTriangle.boundingboxTopLeftY
  if startY < 0:
    startY = 0
  endY = aTriangle.boundingboxBottomRightY
  if endY > 480:
    endY = 480
  while startY < endY:
    TestPixels(aTriangle,startY,colour,surface)
    startY += 1
 
 
