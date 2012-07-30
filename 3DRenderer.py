##############################################################################
#3dRenderer.py - a software renderer that uses pygame to render model data
#declared at the command prompt. The model data is represented as a list of
#triangle vertices
#############################################################################

import pygame
import IncludesAndConstants
import AppInfo
import Lighting
import Triangle
import sys

from pygame import *

X = 0
Y = 1
Z = 2

if len(sys.argv) > 1:
  fileName = sys.argv[1]
else :
  print("Please supply a file name!")
  sys.exit()


#quick little bubblesort algorithm to sort the triangles into z order
def bubbleSortTriangles(triangleList):
  size = len(triangleList)
  passes = size - 2
  i = 0
  while i < passes:
    j = 0
    while j < (size - 1) :
      if triangleList[j].AveragePoint[Z] < triangleList[j+1].AveragePoint[Z] :
        temp = triangleList[j]
        triangleList[j] = triangleList[j+1]
        triangleList[j+1] = temp
      j += 1
    i += 1
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

#create a list of values
triangleList = []

#read triangle data from a file
triangleList = AppInfo.FileRead(triangleList,fileName)


copyList = []

#transform each of the triangles by the world matrix
#also, create the normals and calculate the color of lighting

for t in triangleList:
  t = Triangle.MultiplyTriangle(t,AppInfo.worldMatrix)
  t = Triangle.MultiplyTriangle(t,AppInfo.viewMatrix)
  t.normal = Triangle.CreateTransformedNormal(t)
  t.colour = Lighting.CalculateColour(t)
  copyList.append(t)
  

triangleList = copyList
copyList = []
  

#get rid of unneeded triangles in the copylist
for t in triangleList:
  #t.normal = Triangle.CreateTransformedNormal(t)
  if Triangle.TestForCull(t) == False:
    copyList.append(t)

#set the triangleList to point at the new copylist
triangleList = copyList
copyList = []

#do projection
for t in triangleList:
  t = Triangle.MultiplyTriangle(t,AppInfo.projectionMatrix)
  copyList.append(t)

triangleList = copyList
copyList = []


#do perspective division for perspective

for t in triangleList:
  t = AppInfo.PerspDiv(t)
  t = Triangle.MultiplyTriangle(t,AppInfo.ScreenMatrix)
  copyList.append(t)

triangleList = copyList
copyList = []


#clip in z
for t in triangleList:
  averagePt = Triangle.AveragePoint(t)
  if averagePt[2] < 1.0 or averagePt[2] > 0.0 :
    copyList.append(t)

triangleList = copyList
copyList = []

for t in triangleList:
  t.AveragePoint = Triangle.AveragePoint(t)

#sort triangles by z
triangleList = bubbleSortTriangles(triangleList)


  
#draw triangles
for t in triangleList:
  Triangle.drawTriangle(t,windowSurface,t.colour)
  #print(t.AveragePoint[2])



pygame.display.update()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      IncludesAndConstants.sys.exit()
