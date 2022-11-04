from collections import deque
from math import sin, cos, pi, atan2, hypot, sqrt, pow
import random
import time
import wx

SIZE = 600      # size of screen
COUNT = 2      # count of random static objects
SPEED = 100      # speed of bot
DELTA = 0.01
COLORS = [
    wx.RED,
]

class Bot(object):
    def __init__(self, position, target):
        self.position = position
        self.target = target
        self.speed = 1
        # padding determines how far it needs to divert / how much to go around another bot
        self.padding = 10
        # self.padding = random.random() * 8 + 16
        self.history = deque(maxlen=64)
    def update(self, bots):
        px, py = self.position
        tx, ty = self.target
        angle = atan2(ty - py, tx - px)
        dx = cos(angle)
        dy = sin(angle)
        pdx = dx
        pdy = dy
        for bot in bots:
            if bot == self:
                continue
            x, y = bot.position
            d = hypot(px - x, py - y) ** 2
            # deciding factor in robots touching each other
            p = bot.padding ** 2
            # takes a turn if another bot exists
            angle = atan2(py - y, px - x)
            dx += cos(angle) / d * p
            dy += sin(angle) / d * p
            # dx += cos(angle) / d * p
            # dy += sin(angle) / d * p
        if (pdx-dx > DELTA or pdy-dy>DELTA):
            # pause the robot
            self.set_position(self.get_position(0))
            # self.update(bots)
        angle = atan2(dy, dx)
        # angle = 2*pi
        magnitude = hypot(dx, dy)
        return angle, magnitude
    
    def set_position(self, position):
        self.position = position
        if not self.history:
            self.history.append(self.position)
            return
        x, y = self.position
        px, py = self.history[-1]
        d = hypot(px - x, py - y)
        if d >= 10:
            self.history.append(self.position)
    def get_position(self, offset):
        px, py = self.position
        tx, ty = self.target
        angle = atan2(ty - py, tx - px)
        return (px + cos(angle) * offset, py + sin(angle) * offset)
    
    def checkForCollision(self, bot, angle1, angle2):
        x1, y1 = self.position
        x2, y2 = bot.position
        xa = (self.speed)*cos(angle1)
        ya = (self.speed)*sin(angle1)
        xb = (self.speed)*cos(angle2)
        yb = (self.speed)*sin(angle2)
        mintime = -(x1*xa - xa*x2 - (x1 - x2)*xb + y1*ya - ya*y2 - (y1 - y2)*yb) / (xa**2 - 2*xa*xb + xb**2 + ya**2 - 2*ya*yb + yb**2)
        mindist = sqrt( pow(mintime*xa - mintime*xb + x1 - x2, 2) + pow(mintime*ya - mintime*yb + y1 - y2, 2) )
        
        if mindist <= 0:
            print("it will not collide")
            return True; 
        else:
            totalTime = 0
            timeleft = (mintime - totalTime)
            if mindist <= 6 + 6:
                print(f"Will collide within {timeleft}s")
                return False
            else:
                print(f"Will not collide, but reach minimum distance in {timeleft}s")
                return True
    
class Model(object):
    def __init__(self, width, height, count):
        self.width = width
        self.height = height
        self.bots = self.create_bots(count)
    def create_bots(self, count):
        result = []
        for _ in range(count):
            position = self.select_point()
            target = self.select_point()
            bot = Bot(position, target)
            result.append(bot)
        return result
    
    def select_point(self):
        # return random.choice([(-300, 0), (300, 0), (0, 300), (0, -300)])
        cx = self.width / 2.0
        cy = self.height / 2.0
        angles = [157, 314, 471, 628]
        radius = min(self.width, self.height) * 0.4
        # angle cannot be more than 2 pi = 6.28319f
        # angle = random.random() * 2 * pi
        angle = random.choice(angles)/100
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius
        return (x, y)
    
    def update(self, dt):
        data = [bot.update(self.bots) for bot in self.bots]
        for bot, (angle, magnitude) in zip(self.bots, data):
            speed = min(1, 0.2 + magnitude * 0.8)
            # slows the bot when a turn is being taken
            dx = cos(angle) * dt * SPEED * bot.speed * speed
            dy = sin(angle) * dt * SPEED * bot.speed * speed
            # dx = cos(angle) * dt * SPEED * bot.speed * speed
            # dy = sin(angle) * dt * SPEED * bot.speed * speed
            px, py = bot.position
            tx, ty = bot.target
            bot.set_position((px + dx, py + dy))
            
            # if bot reached destination, select new target
            if hypot(px - tx, py - ty) < 10:
                bot.target = self.select_point()
class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)
        self.model = Model(SIZE, SIZE, COUNT)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.timestamp = time.time()
        self.on_timer()
    def on_timer(self):
        now = time.time()
        dt = now - self.timestamp
        self.timestamp = now
        self.model.update(dt)
        self.Refresh()
        wx.CallLater(10, self.on_timer)
    def on_left_down(self, event):
        self.model.bots[0].target = event.GetPosition()
    def on_right_down(self, event):
        width, height = self.GetClientSize()
        self.model = Model(width, height, COUNT)
    def on_size(self, event):
        width, height = self.GetClientSize()
        self.model = Model(width, height, COUNT)
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        n = len(COLORS)
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        for index, bot in enumerate(self.model.bots[:n]):
            dc.SetBrush(wx.Brush(COLORS[index]))
            for x, y in bot.history:
                dc.DrawCircle(x, y, 3)
        dc.SetBrush(wx.BLACK_BRUSH)
        for index, bot in enumerate(self.model.bots[:n]):
            dc.SetPen(wx.Pen(COLORS[index]))
            x, y = bot.target
            dc.DrawCircle(x, y, 6)
        for index, bot in enumerate(self.model.bots):
            dc.SetPen(wx.BLACK_PEN)
            if index < n:
                dc.SetBrush(wx.Brush(COLORS[index]))
            elif index >= COUNT:
                dc.SetBrush(wx.BLACK_BRUSH)
                dc.SetPen(wx.WHITE_PEN)
            else:
                dc.SetBrush(wx.WHITE_BRUSH)
            x, y = bot.position
            dc.DrawCircle(x, y, 6)

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Motion')
        self.SetClientSize((SIZE, SIZE))
        Panel(self)

def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()