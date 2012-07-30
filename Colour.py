R = 0
G = 1
B = 2

class Colour:
  def __init__(self,r,g,b):
    self.data = [r,g,b]

  def __add__(self,c):
    r = self.data[R] + c.data[R]
    g = self.data[G] + c.data[G]
    b = self.data[B] + c.data[B]
    return Colour(r,g,b)

  def __getitem__(self,a):
    return self.data[a]     

  def __mul__(self,c):
    r = self[R] * c[R]
    g = self[G] * c[G]
    b = self[B] * c[B]
    return Colour(r,g,b)
  
 