from collections import deque
from math import sin, cos, pi, atan2, hypot, sqrt, pow
import random
import time
import wx
from linesegmentintersect import doIntersect, roundTo90, absDistance
from colorama import Fore


SIZE = 600      # size of screen
COUNT = 3     # count of all bots
SPEED = 100      # speed of bot
DELTA = 0.0001
BOT_SIZE = 6
COLORS = [
    wx.RED,
    wx.BLUE,
    wx.YELLOW
]
bot_to_color = {1:"RED", 2: "BLUE", 3:"YELLOW"}

class Bot(object):
    def __init__(self, position, target, id):
        self.id = id
        self.position = position
        self.target = target
        self.speed = 1
        self.move = True
        # padding determines how far it needs to divert / how much to go around another bot
        self.padding = 40
        # self.padding = random.random() * 8 + 16
        self.history = deque(maxlen=64)
        self.waitTime = 0
    def update(self, bots):
        px, py = self.position
        tx, ty = self.target
        angle1 = atan2(ty - py, tx - px)
        
        for bot in bots:
            if bot == self:
                continue
            x, y = bot.position
            fx, fy = bot.target
            angle2 = atan2(fy - y, fx - x)
            
            # d = hypot(px - x, py - y) ** 2
            # # deciding factor in robots touching each other
            # p = bot.padding ** 2
            # # takes a turn if another bot exists
            # angle = atan2(py - y, px - x)
            # dx += cos(angle) / d * p
            # dy += sin(angle) / d * p
            
            # only check for collision if line segments(bot to target) intersect
            if doIntersect((px, py), (tx, ty), (x, y), (fx, fy)):
                # self.collides(bot, roundTo90(angle1), roundTo90(angle2))
                if(self.collides(bot, angle1, angle2)):
                    cpx, cpy = self.collisionPoint((px, py), (tx, ty), (x, y), (fx, fy))    # collision point x and y
                    d1 = absDistance((px, py), (tx, ty))
                    d2 = absDistance((x , y), (fx, fy))
                    
                    if (absDistance((px, py), (cpx, cpy)) < 50 or absDistance((x , y), (cpx, cpy)) < 50) and d1 > d2:
                        if self.id == 1:
                            print(Fore.RED + f"Avoiding collision by stopping bot {self.id}")
                        elif self.id == 2:
                            print(Fore.BLUE + f"Avoiding collision by stopping bot {self.id}")
                        else:
                            print(Fore.YELLOW + f"Avoiding collision by stopping bot {self.id}")
                        
                        self.speedStop()
                        self.waitTime += 1
                        
                        if self.waitTime > bot.waitTime + 200:
                            self.speedReset()
                            print(f"Reset speed for bot {self.id}")
            else:
                self.speedReset()     
                        
        # restricting its movement by rounding angle to 90 or 1.5708
        # angle = roundTo90(angle)
        return angle1
    
    def speedFast(self):
        self.speed = 5
    
    def speedStop(self):
        self.speed = 0
        
    def speedReset(self):
        self.speed = 1
        
    def speedSlow(self):
        self.speed -= 0.2
        
    def collisionPoint(self, p,t, q, f):
        (px, py) = p
        (tx, ty) = t 
        (x, y)   = q
        (fx, fy) = f
        m1 = (ty-py)/(tx-px)  
        # slope of intermediate to final
        m2 = (fy-y)/(fx-x)

        intersect_x = ( (m1*px - m2*fx) + (fy - py) )/(m1-m2)
        intersect_y = ( (m1*m2*(px - fx)) + (m1*fy - m2*py) )/(m1-m2)
        return intersect_x, intersect_y
        
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
    
    # collision detector
    def collides(self, bot, angle1, angle2):
        px, py = self.position
        x, y = bot.position
        xa = (self.speed)*cos(angle1)
        ya = (self.speed)*sin(angle1)
        xb = (self.speed)*cos(angle2)
        yb = (self.speed)*sin(angle2)
        
        def calculateTime(px, py, x, y):
            tm = ((xa - xb)*(x - px) + (ya - yb)*(y - py)) / ((xa - xb)**2 + (ya - yb)**2)
            return tm
        def calculateDist(tm):
            ds = sqrt( pow(tm*xa - tm*xb + px - x, 2) + pow(tm*ya - tm*yb + py - y, 2) )
            return ds
        
        mintime = 0
        mintime_left = 0
        mintime_right = 0
        
        if xa-xb>DELTA or ya-yb>DELTA:
            mintime = calculateTime(px, py, x, y) 
            # 65% left of mid of bot
            mintime_left = calculateTime(px-BOT_SIZE*0.65, py-BOT_SIZE*0.65, x-BOT_SIZE*0.65, y-BOT_SIZE*0.65) 
            # 65% right of mid of bot
            mintime_right = calculateTime(px+BOT_SIZE*0.65, py+BOT_SIZE*0.65, x+BOT_SIZE*0.65, y+BOT_SIZE*0.65)
        mindist_right = calculateDist(mintime_right)
        mindist_left = calculateDist(mintime_left)
        mindist = calculateDist(mintime)
        
        if mindist <= 0:
            return False; 
        else:
            totalTime = 0
            timeleft = (mintime - totalTime)/10
            if (mindist <= 30 or mindist_left <= 30 or mindist_right <= 30) and mintime>0:
                # print(Fore.WHITE + f"{bot_to_color[self.id]}({self.id}) Might collide with {bot_to_color[bot.id]}({bot.id}) within {timeleft:.2f}ms")
                print(Fore.WHITE + f"({self.id}) Might collide with ({bot.id}) within {timeleft:.2f}ms")
                return True
            else:
                return False
            
        
     
class Model(object):
    def __init__(self, width, height, count):
        self.width = width
        self.height = height
        self.bots = self.create_bots(count)
    
    def create_bots(self, count):
        result = []
        for i in range(count):
            position = self.select_point()
            target = self.select_target()
            bot = Bot(position, target, i + 1)
            result.append(bot)
        return result
    
    def select_point(self):
        cx = self.width / 2.0
        cy = self.height / 2.0
        # angles = [157, 314, 471, 628]
        radius = min(self.width, self.height) * 0.4
        # angle cannot be more than 2 pi = 6.28319f
        angle = random.random() * 2 * pi
        # angle = random.choice(angles)/100
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius
        return (x, y)
    
    def select_target(self):
        cx = self.width / 2.0
        cy = self.height / 2.0
        # angles = [157, 314, 471, 628]
        radius = min(self.width, self.height) * 0.4
        # angle cannot be more than 2 pi = 6.28319f
        angle = random.random() * 2 * pi
        # angle = random.choice(angles)/100
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius
        return (x, y)
    
    def update(self, dt):
        data = [bot.update(self.bots) for bot in self.bots]
        for bot, (angle) in zip(self.bots, data):
            # changes the direction and slows the bot when a turn is being taken
            dx = cos(angle) * dt * SPEED * bot.speed 
            dy = sin(angle) * dt * SPEED * bot.speed 
            px, py = bot.position
            tx, ty = bot.target
            bot.set_position((px + dx, py + dy))
            # if bot reached destination, select new target
            if hypot(px - tx, py - ty) < 7:
                bot.target = self.select_target()
                bot.waitTime = 0
        
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