import sys, math, pygame, pygame.gfxdraw
from pygame.locals import *

#this uses a left hand system


################################################################################################################
#CONSTANT VALUES! -                                                                                            #
#Below are the constants used to define the eye point, variables for the projection/view concatenated matrix,  #
#global ambient colour etc                                                                                     #
################################################################################################################


#cameraPosition
cameraX = 0.0
cameraY = 0.0
cameraZ = -15.0

#point Camera is looking at
lookPointX = 0.0
lookPointY = 0.0
lookPointZ = 0.0

ViewportWidth = 640
ViewportHeight = 480

ViewportX = 0
ViewportY = 0

#aspect Ratio
aspectRatio = ViewportWidth/ViewportHeight

#translation amounts for model
ModelTranslateX = 0.0
ModelTranslateY = 0.0
ModelTranslateZ = 0.0

#rotation of model
XAxisRotation = 20.0
YAxisRotation = 0.0
ZAxisRotation = 0.0 

#change to rads for their use later
XAxisRotation = math.radians(XAxisRotation)
YAxisRotation = math.radians(YAxisRotation)
ZAxisRotation = math.radians(ZAxisRotation)

#fov
FOV = 90.0

#far and nearPlanes for projection matrix

farPlane  = 1000.0
nearPlane = 1.0

#constants for material

ambientR = 1.0
ambientG = 0.2
ambientB = 0.2

diffuseR = 0.4
diffuseG = 0.5
diffuseB = 0.2

specularR = 1.0
specularG = 0.4
specularB = 0.5

shininess = 8.0

#position of global light source
lightSourceX = cameraX
lightSourceY = cameraY
lightSourceZ = cameraZ 

#colour of light source
lightSourceR = 0.5
lightSourceG = 0.6 
lightSourceB = 0.4 


#colour of global ambientLight
ambientR = 0.4
ambientG = 0.5 
ambientB = 0.0

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


class Vector:
  def __init__(self,x,y,z,w):
    self.elems = [x,y,z,w]

  def length(self):
    return math.sqrt(self.elems[0] * self.elems[0] + self.elems[1] * self.elems[1] + self.elems[2] * self.elems[2])

  def normalize(self):
    len = Vector.length(self)
    if self.elems[0] != 0:
      self.elems[0] = self.elems[0]/len
    if self.elems[1] != 0:
      self.elems[1] = self.elems[1]/len
    if self.elems[2] != 0:
      self.elems[2] = self.elems[2]/len

  def __add__(self,c):
    return Vector(self.elems[0]+c.elems[0],self.elems[1]+c.elems[1],self.elems[2]+c.elems[2],self.elems[3]+c.elems[3])

  def __sub__(self,c):
     return Vector(self.elems[0]-c.elems[0],self.elems[1]-c.elems[1],self.elems[2]-c.elems[2],self.elems[3]-c.elems[3])   

def dotProduct(vec1,vec2):
  return (vec1.elems[0] * vec2.elems[0]) + (vec1.elems[1] * vec2.elems[1]) + (vec1.elems[2] * vec2.elems[2])

def crossProduct(vec1,vec2):
  i = (vec1.elems[1] * vec2.elems[2]) - (vec1.elems[2] * vec2.elems[1])
  j = -((vec1.elems[0] * vec2.elems[2]) - (vec2.elems[0] * vec1.elems[2]))
  k = (vec1.elems[0] * vec2.elems[1]) - (vec2.elems[0] * vec1.elems[1])
  cross = Vector(i,j,k,0)
  cross.normalize()
  return cross

#########################
#MATRIX CLASS           #
#########################

class Matrix:
  def __init__(self,m11,m12,m13,m14,m21,m22,m23,m24,m31,m32,m33,m34,m41,m42,m43,m44):
    self.elems = [[m11,m12,m13,m14],
     		  [m21,m22,m23,m24],
     		  [m31,m32,m33,m34],
     		  [m41,m42,m43,m44]]
    

def VectorMatrixMult(Vec,aMatrix):
  i = 0
  j = 0
  total = 0
  newList = []
  while i < 4:
    while j < 4:
      total += Vec.elems[j] * aMatrix.elems[j][i]
      j = j + 1
    newList.append(total)
    i = i + 1
    j = 0
    total = 0
  return Vector(newList[0],newList[1],newList[2],newList[3])

def MatrixMatrixMult(aMatrix1,aMatrix2):
  i = 0
  j = 0
  k = 0
  newList1 = []
  newList2 = []
  while i < 4:
    while k < 4:
      total = 0
      while j < 4:
        total += aMatrix1.elems[i][j] * aMatrix2.elems[j][k]
        j += 1
      newList1.append(total)
      j = 0
      k += 1
    newList2.append(newList1)
    newList1 = []
    i += 1
    k = 0
  return Matrix(newList2[0][0],newList2[0][1],newList2[0][2],newList2[0][3],newList2[1][0],newList2[1][1],newList2[1][2],newList2[1][3],newList2[2][0],newList2[2][1],newList2[2][2],newList2[2][3],newList2[3][0],newList2[3][1],newList2[3][2],newList2[3][3])
     

class Colour:
  def __init__(self,r,g,b):
    self.elems = [r,g,b]

  def __add__(self,c):
    r = self.elems[0] + c.elems[0]
    g = self.elems[1] + c.elems[1]
    b = self.elems[2] + c.elems[2]
    return Colour(r,g,b)

  def __mul__(self,c):
    r = self.elems[0] * c.elems[0]
    g = self.elems[1] * c.elems[1]
    b = self.elems[2] * c.elems[2]
    return Colour(r,g,b)

################################
#TRIANGLE CLASS                #
################################

def AveragePoint(aTriangle):
  x = (aTriangle.p1.elems[0] + aTriangle.p2.elems[0] + aTriangle.p3.elems[0])/3
  y = (aTriangle.p1.elems[1] + aTriangle.p2.elems[1] + aTriangle.p3.elems[1])/3
  z = (aTriangle.p1.elems[2] + aTriangle.p2.elems[2] + aTriangle.p3.elems[2])/3
  return Vector(x,y,z,1)


class Triangle:
  def __init__(self,p1,p2,p3,color):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3
    self.normal = Vector(0,0,0,0)
    self.AveragePoint = AveragePoint(self)
    self.Colour = color

def MultiplyTriangle(aTriangle,aMatrix):
  aTriangle.p1 = VectorMatrixMult(aTriangle.p1,aMatrix)
  aTriangle.p2 = VectorMatrixMult(aTriangle.p2,aMatrix)
  aTriangle.p3 = VectorMatrixMult(aTriangle.p3,aMatrix)
  return Triangle(aTriangle.p1,aTriangle.p2,aTriangle.p3,aTriangle.Colour)


def AveragePoint(aTriangle):
  x = (aTriangle.p1.elems[0] + aTriangle.p2.elems[0] + aTriangle.p3.elems[0])/3
  y = (aTriangle.p1.elems[1] + aTriangle.p2.elems[1] + aTriangle.p3.elems[1])/3
  z = (aTriangle.p1.elems[2] + aTriangle.p2.elems[2] + aTriangle.p3.elems[2])/3
  return Vector(x,y,z,1)

def ConvertToInts(aTriangle):
  aTriangle.p1.elems[0] = int(aTriangle.p1.elems[0])
  aTriangle.p1.elems[1] = int(aTriangle.p1.elems[1])
  aTriangle.p1.elems[2] = int(aTriangle.p1.elems[2])
  aTriangle.p1.elems[3] = int(aTriangle.p1.elems[3])
  aTriangle.p2.elems[0] = int(aTriangle.p2.elems[0])
  aTriangle.p2.elems[1] = int(aTriangle.p2.elems[1])
  aTriangle.p2.elems[2] = int(aTriangle.p2.elems[2])
  aTriangle.p2.elems[3] = int(aTriangle.p2.elems[3])
  aTriangle.p3.elems[0] = int(aTriangle.p3.elems[0])
  aTriangle.p3.elems[1] = int(aTriangle.p3.elems[1])
  aTriangle.p3.elems[2] = int(aTriangle.p3.elems[2])
  aTriangle.p3.elems[3] = int(aTriangle.p3.elems[3])
  return Triangle(Vector(aTriangle.p1.elems[0],aTriangle.p1.elems[1],aTriangle.p1.elems[2],aTriangle.p1.elems[3]),Vector(aTriangle.p2.elems[0],aTriangle.p2.elems[1],aTriangle.p2.elems[2],aTriangle.p2.elems[3]),Vector(aTriangle.p3.elems[0],aTriangle.p3.elems[1],aTriangle.p3.elems[2],aTriangle.p3.elems[3]))


def CreateTransformedNormal(aTriangle):
  aTriangle.normal = crossProduct(aTriangle.p2-aTriangle.p1,aTriangle.p3-aTriangle.p1)
  return aTriangle.normal

def TestForCull(aTriangle):
  camVector = Vector(lookPointX - cameraX,lookPointY - cameraY,lookPointZ - cameraZ,0)
  normal = Vector(aTriangle.normal.elems[0],aTriangle.normal.elems[1],aTriangle.normal.elems[2],0)
  normal.normalize()
  print(normal.elems)
  if dotProduct(normal,camVector) < 0:
    return False
  else:
    return True


#CLASSES RELATED TO TRIANGLES - EDGES AND SPANS

class Edge:
  def __init__(self,x1,y1,x2,y2): 
    if y1 < y2:
      self.topY = y1
      self.initialX = x1
      if (y2-y1) == 0:
        self.dxPerScanLine = 0
      else:
        m = (y2 - y1)/(x2-x1)
        self.dxPerScanLine = 1/m
    else:
      self.topY = y2
      self.initialX = x2
      if (y2-y1) == 0:
        self.dxPerScanLine = 0
      else:
        m = (y2 - y1)/(x2-x1)
        self.dxPerScanLine = 1/m
    self.YLength = abs(y2-y1)

class Span:
  def __init__(self,x1,x2):
    self.x1 = x1
    self.x2 = x2

def DrawSpan(span,y,surface,colour):
  xDiff = abs(span.x2 - span.x1)
  if xDiff == 0:
    return
  #do a test here instead of clipping
  if span.x1 > 640:
    return
  if span.x2 < 0:
    return
  if span.x1 < 0:
    span.x1 = 0
  if span.x2 > 640:
    span.x2 = 640
  xStart = span.x1
  while xStart < span.x2:
    pygame.gfxdraw.pixel(surface,int(xStart),int(y),pygame.Color(int(colour.elems[0] * 255),int(colour.elems[1] *255),int(colour.elems[2] * 255),255))
    xStart += 1
    

def DrawSpansBetweenEdges(edge1,edge2,surface,colour):
  yStart = edge1.topY
  xStart = edge1.initialX
  xEnd = edge2.initialX
  i = 0
  while i < edge1.YLength:
    span = Span(xStart + i * edge1.dxPerScanLine,xEnd + i * edge2.dxPerScanLine)
    DrawSpan(span,yStart+i,surface,colour)
    i += 1
  

#Drawing a triangle

def drawTriangle(aTriangle,surface,colour):
  x1 = aTriangle.p1.elems[0]
  y1 = aTriangle.p1.elems[1]
  x2 = aTriangle.p2.elems[0]
  y2 = aTriangle.p2.elems[1]
  x3 = aTriangle.p3.elems[0]
  y3 = aTriangle.p3.elems[1]
  edges = [Edge(x1,y1,x2,y2),Edge(x2,y2,x3,y3),Edge(x3,y3,x1,y1)]
  DrawSpansBetweenEdges(edges[0],edges[2],surface,colour)
  DrawSpansBetweenEdges(edges[0],edges[1],surface,colour)
  DrawSpansBetweenEdges(edges[1],edges[2],surface,colour)
 



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
ambient = Colour(ambientR,ambientG,ambientB)
specular = Colour(specularR,specularG,specularB)
diffuse = Colour(diffuseR,diffuseG,diffuseB)

#create a material
material1 = Material(ambient,specular,diffuse,shininess)

#create the lightpoint

lightPoint = Vector(lightSourceX,lightSourceY,lightSourceZ,1)
  

def Diffuse(aNormal,aTrianglePoint):
  lightVec = Vector(lightPoint.elems[0] - aTrianglePoint.elems[0],lightPoint.elems[1] - aTrianglePoint.elems[1],lightPoint.elems[2] - aTrianglePoint.elems[2],lightPoint.elems[3] - aTrianglePoint.elems[3])
  return max(dotProduct(lightVec,aNormal),0)  


def Specular(aTrianglePoint,aNormal):
  V = Vector(cameraX - aTrianglePoint.elems[0],cameraY - aTrianglePoint.elems[1],cameraZ - aTrianglePoint.elems[2],1 - aTrianglePoint.elems[3])
  V.normalize() 
  lightVec = Vector(lightPoint.elems[0] - aTrianglePoint.elems[0],lightPoint.elems[1] - aTrianglePoint.elems[1],lightPoint.elems[2] - aTrianglePoint.elems[2],lightPoint.elems[3] - aTrianglePoint.elems[3])
  lightVec.normalize
  H = lightVec + V
  H.normalize()
  d = dotProduct(aNormal,H)
  return pow(max(d,0),shininess)

def CalculateColour(aTriangle):
  ambientFactor = material1.ambient * ambient
  diffuseFactor = Diffuse(aTriangle.normal,AveragePoint(aTriangle))
  newDiffuse = Colour(diffuseFactor*lightSourceR,diffuseFactor*lightSourceG,diffuseFactor*lightSourceB)
  diffuseFactor = newDiffuse * material1.diffuse
  specularFactor = Specular(AveragePoint(aTriangle),aTriangle.normal)
  newSpecular = Colour(specularFactor*lightSourceR,specularFactor*lightSourceG,specularFactor*lightSourceB)
  specularFactor = newSpecular * material1.specular
  endColour = ambientFactor + diffuseFactor + specularFactor
  if endColour.elems[0] > 1.0:
    endColour.elems[0] = 1.0
  if endColour.elems[1] > 1.0:
    endColour.elems[1] = 1.0
  if endColour.elems[2] > 1.0:
    endColour.elems[2] = 1.0
  return Colour(endColour.elems[0],endColour.elems[1],endColour.elems[2])
  
  
  

##############################################################################################
#Creating App variables - eg creating necessary matrices from the above classes and the      #
#constants defined at the start of the file                                                  #
##############################################################################################

#WORLD MATRIX
identityMatrix = Matrix(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)

worldMatrix = Matrix(1,0,0,0,0,1,0,0,0,0,1,0,ModelTranslateX,ModelTranslateY,ModelTranslateZ,1)

xRotateMatrix = Matrix(1,0,0,0,0,math.cos(XAxisRotation),-(math.sin(XAxisRotation)),0,0,math.sin(XAxisRotation),math.cos(XAxisRotation),0,0,0,0,1)
  
yRotateMatrix = Matrix(math.cos(YAxisRotation),0,-(math.sin(YAxisRotation)),0,0,1,0,0,math.sin(YAxisRotation),0,math.cos(YAxisRotation),0,0,0,0,1)

zRotateMatrix = Matrix(math.cos(ZAxisRotation),math.sin(ZAxisRotation),0,0,-(math.sin(ZAxisRotation)),math.cos(ZAxisRotation),0,0,0,0,1,0,0,0,0,1)

identityMatrix = MatrixMatrixMult(xRotateMatrix,identityMatrix)

identityMatrix = MatrixMatrixMult(yRotateMatrix,identityMatrix)

identityMatrix = MatrixMatrixMult(zRotateMatrix,identityMatrix)

worldMatrix = MatrixMatrixMult(worldMatrix,identityMatrix)


#VIEW MATRIX
#creating a view matrix involves look,up and right vectors, and depending on the orientation and components of the look
#vector 

lookVector = Vector(lookPointX - cameraX,lookPointY - cameraY,lookPointZ - cameraZ,0.0)
lookVector.normalize()

rightVector = crossProduct(Vector(0,1,0,0),lookVector)
rightVector.normalize()

upVector = crossProduct(lookVector,rightVector)
upVector.normalize()


CameraPos = Vector(cameraX,cameraY,cameraZ,1)
viewMatrix = Matrix(rightVector.elems[0],upVector.elems[0],lookVector.elems[0],0,rightVector.elems[1],upVector.elems[1],lookVector.elems[1],0,rightVector.elems[2],upVector.elems[2],lookVector.elems[2],0,-(dotProduct(CameraPos,rightVector)),-(dotProduct(CameraPos,upVector)),-(dotProduct(CameraPos,lookVector)),1)
ScreenMatrix = Matrix(ViewportWidth/2,0,0,0,0,-ViewportHeight/2,0,0,0,0,1,0,ViewportWidth/2,ViewportHeight/2,0,1)

#PROJECTION MATRIX

yScale = (math.cos(FOV/2)/math.sin(FOV/2))
xScale = yScale * aspectRatio
zf = farPlane/(farPlane -nearPlane)
zn = -zf*nearPlane

projectionMatrix = Matrix(xScale,0,0,0,0,yScale,0,0,0,0,zf,1,0,0,zn,0)

#PERSPECTIVE DIVISON

def PerspDiv(aTriangle):
  aTriangle.p1 = perspectiveDivision(aTriangle.p1)
  aTriangle.p2 = perspectiveDivision(aTriangle.p2)
  aTriangle.p3 = perspectiveDivision(aTriangle.p3)
  return Triangle(aTriangle.p1,aTriangle.p2,aTriangle.p3,aTriangle.Colour)

def perspectiveDivision(point):
  point.elems[0] /= point.elems[3]
  point.elems[1] /= point.elems[3]
  point.elems[2] /= point.elems[3]
  point.elems[3] /= point.elems[3]
  return Vector(point.elems[0],point.elems[1],point.elems[2],point.elems[3])

def discardTriangle(triangle):
  if triangle.p1.elems[3] == 0:
    return True;
  if triangle.p2.elems[3] == 0:
    return True;
  if triangle.p3.elems[3] == 0:
    return True;
  return False

#Creating a mastertransformMatrix

viewProjectionMatrix = MatrixMatrixMult(projectionMatrix,viewMatrix)

########################################################################################################################
#FILE READING CODE######################################################################################################
########################################################################################################################

def FileRead(triangleList):
  f = open("triangles.txt","r")
  for line in f:
    data = line
    data = data.split()
    x1 = float(data[0])
    y1 = float(data[1])
    z1 = float(data[2])
    x2 = float(data[3])
    y2 = float(data[4])
    z2 = float(data[5])
    x3 = float(data[6])
    y3 = float(data[7])
    z3 = float(data[8])
    vec1 = Vector(x1,y1,z1,1)
    vec2 = Vector(x2,y2,z2,1)
    vec3 = Vector(x3,y3,z3,1)
    triangleList.append(Triangle(vec1,vec2,vec3,Colour(1,1,1)))
  f.close()
  return triangleList

########################################################################################################################
#MAIN PROGRAM                                                                                                          #
#Below we have all the necessary function calls and program logic to create loads of triangles and hopefully rasterize #
#a model as necessary!                                                                                                 #
########################################################################################################################

#all the necessary stuff to set up a graphics window using pygame

pygame.init()

#set up the window itself
windowSurface = pygame.display.set_mode((640,480),0,32)

#test triangle data

#create a list of triangles
triangleList = []

#read triangle data from a file
triangleList = FileRead(triangleList)

copyList = []



#transform triangles
for t in triangleList:
  t = MultiplyTriangle(t,worldMatrix)
  t.normal = CreateTransformedNormal(t)
  t.Colour = CalculateColour(t)
  t = MultiplyTriangle(t,viewProjectionMatrix)
  copyList.append(t)

triangleList = copyList
copyList = []

#test for z = 0
for t in triangleList:
  if discardTriangle(t) == False:
    copyList.append(t)

triangleList = copyList
copyList = []


#do other things
for t in triangleList:
  t = PerspDiv(t)
  t = MultiplyTriangle(t,ScreenMatrix)
  copyList.append(t)

triangleList = copyList
copyList = []

#sort triangles by z
triangleList = sorted(triangleList,key = lambda triangle: triangle.AveragePoint.elems[2])

triangleList.reverse()

#get rid of unneeded triangles
for t in triangleList:
  if TestForCull(t) == True:
    copyList.append(t)

triangleList = copyList
  
#draw triangles
for t in triangleList:
  drawTriangle(t,windowSurface,t.Colour)
  #print(t.p1.elems)



pygame.display.update()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
