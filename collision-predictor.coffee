$body = $('body')
$state = $('<div class="State">').appendTo $body
w = $body.width()
h = $body.height()

startTime = null
totalTime = null

class Car
  constructor: (@x0,@y0,@xt,@yt)->
    if @x0? # Allow test case
      @disablerandom=true
      @x0 = @x0*100
      @y0 = @y0*100
      @xt = @xt*100
      @yt = @yt*100
      @radius = 50
    @view = $('<div class="Car">').appendTo $body
    @reset()
  reset: ->
    @outside = false
    if not @disablerandom
      @x0 = Math.random() * w
      @y0 = Math.random() * h
      @xt = Math.random() * (w/2-@x0)
      @yt = Math.random() * (h/2-@y0)
      @radius = 5 + Math.random() * 100
    checkForCollision?()
    @view.css 
      width: @radius*2
      height: @radius*2
      marginLeft:-@radius
      marginTop:-@radius
  update: ->
    if @x > w or @x < 0 or @y>h or @y<0 then @outside = true
    @x = @x0 + @xt*totalTime
    @y = @y0 + @yt*totalTime
    @view.css left: @x
    @view.css top: h-@y
    
class CollisionChecker
  constructor: (@a, @b)->
    @mindist=0
    @mintime=0
    @checkForCollision()
  checkForCollision: ->
    @mintime = 
      -(@a.x0*@a.xt - @a.xt*@b.x0 - (@a.x0 - @b.x0)*@b.xt + @a.y0*@a.yt - @a.yt*@b.y0 - (@a.y0 - @b.y0)*@b.yt) /
      (Math.pow(@a.xt,2) - 2*@a.xt*@b.xt + Math.pow(@b.xt,2) + Math.pow(@a.yt,2) - 2*@a.yt*@b.yt + Math.pow(@b.yt,2))
    @mindist = Math.sqrt(
      Math.pow(@mintime*@a.xt - @mintime*@b.xt + @a.x0 - @b.x0, 2) + 
      Math.pow(@mintime*@a.yt - @mintime*@b.yt + @a.y0 - @b.y0, 2)
    )
  renderCounter: ->
    mintimeView = Math.round(@mintime*100)/100
    mindistView = Math.round(@mindist*10)/10
    minedgedistView = Math.round((@mindist-@a.radius-@b.radius)*10)/10
    if @mintime <= 0
      @mindist = Math.round(@mindist)
      $state
        .css color: 'green' 
        .html """
          Will never collide (diverging)<br>
          Minimum center distance: #{mindistView}px<br>
          Minimum edge distance: #{minedgedistView}px<br>
          Time from start of min. dist.: #{mintimeView}s
				"""
    else
      timeleft = Math.round((@mintime - totalTime)*100)/100
      if @mindist <= a.radius + b.radius
        $state
          .css color: 'red'
          .html """
            Will collide within #{timeleft}s<br>
            Minimum center distance: #{mindistView}px<br>
            Minimum edge distance: #{minedgedistView}px<br>
            Time from start of min. dist.: #{mintimeView}s
					"""
      else
        $state
          .css color: '#990'
          .html """
            Will not collide, but reach minimum distance in #{timeleft}s<br>
            Minimum center distance: #{mindistView}px<br>
            Minimum edge distance: #{minedgedistView}px<br>
            Time from start of min. dist.: #{mintimeView}s
					"""
    
# Test case 1
#a = new Car(2,5,1,2/3)
#b = new Car(5,2,-2/3,4/3)

# Random
a = new Car()
b = new Car()
checker = new CollisionChecker a, b

a.view.css backgroundColor: 'red'
b.view.css backgroundColor: 'blue'

startTime = new Date().getTime()/1000.0
setInterval ->
  totalTime = new Date().getTime()/1000.0 - startTime
  a.update()
  b.update()
  checker.renderCounter()
  if a.outside or b.outside 
    console.log 'reset'
    startTime = new Date().getTime()/1000.0
    w = $body.width() # Get viewport dimensions again in case of resize
    h = $body.height()
    a.reset()
    b.reset()
    checker.checkForCollision()