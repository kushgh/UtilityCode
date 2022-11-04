$body = $('body')
$state = $('<div class="State">').appendTo $body
w = $body.width()
h = $body.height()

startTime = null
totalTime = null

class Car
  constructor: (x0,y0,xt,yt)->
    if x0? # Allow test case
      disablerandom=true
      x0 = x0*100
      y0 = y0*100
      xt = xt*100
      yt = yt*100
      radius = 50
    view = $('<div class="Car">').appendTo $body
    reset()
  reset: ->
    outside = false
    if not disablerandom
      x0 = Math.random() * w
      y0 = Math.random() * h
      xt = Math.random() * (w/2-x0)
      yt = Math.random() * (h/2-y0)
      radius = 5 + Math.random() * 100
    checkForCollision?()
    view.css 
      width: radius*2
      height: radius*2
      marginLeft:-radius
      marginTop:-radius
  update: ->
    if x > w or x < 0 or y>h or y<0 then outside = true
    x = x0 + xt*totalTime
    y = y0 + yt*totalTime
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
       (a.xt*a.xt - 2*a.xt*b.xt + b.xt*b.xt + a.yt*a.yt - 2*a.yt*b.yt + b.yt*b.yt)
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