import sys, math, pygame, pygame.gfxdraw
from pygame.locals import *

#this uses a left hand system


################################################################################################################
#CONSTANT VALUES! -                                                                                            #
#Below are the constants used to define the eye point, variables for the projection/view concatenated matrix,  #
#global ambient colour etc                                                                                     #
################################################################################################################


#cameraPosition
cameraX = 2.0
cameraY = 2.0
cameraZ = -5.0

#point Camera is looking at
lookPointX = 2.0
lookPointY = 0.0
lookPointZ = -3.0

ViewportWidth = 640
ViewportHeight = 480

ViewportX = 0
ViewportY = 0

#aspect Ratio
aspectRatio = ViewportWidth/ViewportHeight

#translation amounts for model
ModelTranslateX = 2.0
ModelTranslateY = -2.0
ModelTranslateZ = -2.0

#rotation of model
XAxisRotation = 0.0
YAxisRotation = 0.0

ZAxisRotation = 0.0 

#change to rads for their use later
XAxisRotation = math.radians(XAxisRotation)
YAxisRotation = math.radians(YAxisRotation)
ZAxisRotation = math.radians(ZAxisRotation)

#fov
FOV = 90.0

#far and nearPlanes for projection matrix

farPlane  = 250.0
nearPlane = 1.0

#constants for material

ambientMatR = 0.4
ambientMatG = 0.4
ambientMatB = 0.4

diffuseMatR = 1.0
diffuseMatG = 0.6
diffuseMatB = 0.8

specularMatR = 0.6
specularMatG = 0.6
specularMatB = 1.0

shininess = 0.02

#position of global light source
lightSourceX = 1.0
lightSourceY = 0.5
lightSourceZ = 6.0

#colour of light source
lightSourceR = 0.6
lightSourceG = 0.6 
lightSourceB = 0.8


#colour of global ambientLight
ambientLightR = 0.6
ambientLightG = 0.3 
ambientLightB = 0.4