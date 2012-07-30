import IncludesAndConstants
import Matrix
import Triangle
import Vector

from IncludesAndConstants import *

X = 0
Y = 1
Z = 2
W = 3



##############################################################################################
#Creating App variables - eg creating necessary matrices from the above classes and the      #
#constants defined at the start of the file                                                  #
##############################################################################################

#WORLD MATRIX
identityMatrix = [[1,0,0,0],
		  [0,1,0,0],
		  [0,0,1,0],
		  [0,0,0,1]]



worldMatrix = [[1,0,0,0],
	       [0,1,0,0],
               [0,0,1,0],
               [ModelTranslateX,ModelTranslateY,ModelTranslateZ,1]]



xRotateMatrix = [[1,0,0,0],
		[0,math.cos(XAxisRotation),-(math.sin(XAxisRotation)),0],
		[0,math.sin(XAxisRotation),math.cos(XAxisRotation),0],
		[0,0,0,1]]

  
yRotateMatrix = [[math.cos(YAxisRotation),0,(math.sin(YAxisRotation)),0],
		[0,1,0,0],
                [-math.sin(YAxisRotation),0,math.cos(YAxisRotation),0],
                [0,0,0,1]]
		

zRotateMatrix = [[math.cos(ZAxisRotation),-math.sin(ZAxisRotation),0,0],
		[math.sin(ZAxisRotation),math.cos(ZAxisRotation),0,0],
		[0,0,1,0],
		[0,0,0,1]]

identityMatrix = Matrix.MatrixMatrixMult(xRotateMatrix,identityMatrix)

identityMatrix = Matrix.MatrixMatrixMult(yRotateMatrix,identityMatrix)

identityMatrix = Matrix.MatrixMatrixMult(zRotateMatrix,identityMatrix)

worldMatrix = Matrix.MatrixMatrixMult(worldMatrix,identityMatrix)


#VIEW MATRIX
#creating a view matrix involves look,up and right vectors, and depending on the orientation and components of the look
#vector 

lookVector = [lookPointX - cameraX,lookPointY - cameraY,lookPointZ - cameraZ,0.0]
lookVector = Vector.normalize(lookVector)

rightVector = Vector.crossProduct([0,1,0,0],lookVector)
rightVector = Vector.normalize(rightVector)

upVector = Vector.crossProduct(lookVector,rightVector)
upVector = Vector.normalize(upVector)


CameraPos = [cameraX,cameraY,cameraZ,1]


viewMatrix = [[rightVector[X],upVector[X],lookVector[X],0],
              [rightVector[Y],upVector[Y],lookVector[Y],0],
              [rightVector[Z],upVector[Z],lookVector[Z],0],
              [-(Vector.dotProduct(CameraPos,rightVector)),-(Vector.dotProduct(CameraPos,upVector)),-(Vector.dotProduct(CameraPos,lookVector)),1]]


ScreenMatrix = [[ViewportWidth/2,0,0,0],
                [0,-ViewportHeight/2,0,0],
		[0,0,1,0],
		[ViewportWidth/2,ViewportHeight/2,0,1]]

#PROJECTION MATRIX

yScale = (math.cos(FOV/2)/math.sin(FOV/2))
xScale = yScale / aspectRatio
zf = farPlane/(farPlane - nearPlane)
zn = -(nearPlane * farPlane)/(farPlane-nearPlane)

projectionMatrix = [[xScale,0,0,0],
		    [0,yScale,0,0],
	            [0,0,zf,1],
		    [0,0,zn,0]]

#PERSPECTIVE DIVISON

def PerspDiv(aTriangle):
  aTriangle.p1 = perspectiveDivision(aTriangle.p1)
  aTriangle.p2 = perspectiveDivision(aTriangle.p2)
  aTriangle.p3 = perspectiveDivision(aTriangle.p3)
  return Triangle.Triangle(aTriangle.p1,aTriangle.p2,aTriangle.p3,aTriangle.colour)

def perspectiveDivision(point):
  point[X] /= point[W]
  point[Y] /= point[W]
  point[Z] /= point[W]
  point[W] /= point[W]
  return [point[0],point[1],point[2],point[3]]

def discardTriangle(triangle):
  if triangle.p1[Z] == 0:
    return True;
  if triangle.p2[Z] == 0:
    return True;
  if triangle.p3[Z] == 0:
    return True;
  return False

#Creating a mastertransformMatrix

viewProjectionMatrix = Matrix.MatrixMatrixMult(viewMatrix,projectionMatrix,)

########################################################################################################################
#FILE READING CODE######################################################################################################
########################################################################################################################

def FileRead(triangleList,fileName):
  f = open(fileName,"r")
  vertexList = [];
  for line in f:
    data = line
    data = data.split()
    if data[0] == "v":
      x = float(data[1])
      y = float(data[2])
      z = float(data[3])

      point = [x,y,z,1]
      vertexList.append(point)

    elif data[0] == "f":
      vec1 = vertexList[int(data[1])-1]
      vec2 = vertexList[int(data[2])-1]
      vec3 = vertexList[int(data[3])-1]
      triangleList.append(Triangle.Triangle(vec1,vec2,vec3,[1,1,1]))
  f.close()

  return triangleList