import math, random

startTime = None
totalTime = None

w = 2
h = 2

class Car:
  def __init__(self, x0,y0,xt,yt):
    if x0: # Allow test case
      self.disablerandom=True
      self.x0 = x0*100
      self.y0 = y0*100
      self.xt = xt*100
      self.yt = yt*100
      self.radius = 50
    self.reset()
  def reset(self):
    self.outside = False
    if not self.disablerandom:
      self.y0 = random.random() * h
      self.xt = random.random() * (w/2-x0)
      self.x0 = random.random() * w
      self.yt = random.random() * (h/2-self.y0)
      self.radius = 5 + random.random() * 100
    checkForCollision()
    
  def update(self):
    if x > w or x < 0 or y>h or y<0:
        self.outside = True
    x = self.x0 + self.xt*totalTime
    y = self.y0 + self.yt*totalTime
    view.css left: x
    view.css top: h-y
    
class CollisionChecker
  constructor: (a, b)->
    mindist=0
    mintime=0
    checkForCollision()
  checkForCollision: ->
    mintime = 
      -(a.x0*a.xt - a.xt*b.x0 - (a.x0 - b.x0)*b.xt + a.y0*a.yt - a.yt*b.y0 - (a.y0 - b.y0)*b.yt) /
      (math.pow(a.xt,2) - 2*a.xt*b.xt + math.pow(b.xt,2) + math.pow(a.yt,2) - 2*a.yt*b.yt + math.pow(b.yt,2))
    mindist = math.sqrt(
      math.pow(mintime*a.xt - mintime*b.xt + a.x0 - b.x0, 2) + 
      math.pow(mintime*a.yt - mintime*b.yt + a.y0 - b.y0, 2)
    )
  renderCounter: ->
    mintimeView = math.round(mintime*100)/100
    mindistView = math.round(mindist*10)/10
    minedgedistView = math.round((mindist-a.radius-b.radius)*10)/10
    if mintime <= 0
          """Will never collide (diverging)<br>"""
    else
      timeleft = math.round((mintime - totalTime)*100)/100
      if mindist <= a.radius + b.radius
        """Will collide within #{timeleft}s<br>"""
      else
        """Will not collide, but reach minimum distance in #{timeleft}s<br>, distance: #{mindistView}px<br>"""

a = new Car()
b = new Car()
checker = new CollisionChecker a, b

startTime = new Date().getTime()/1000.0
setInterval ->
  totalTime = new Date().getTime()/1000.0 - startTime
  a.update()
  b.update()
  checker.renderCounter()
  if a.outside or b.outside 
    console.log 'reset'
    startTime = new Date().getTime()/1000.0
    a.reset()
    b.reset()
    checker.checkForCollision()