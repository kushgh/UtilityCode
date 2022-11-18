from math import sin, cos, pi, atan2, hypot, sqrt, pow




px, py = 0, 20
tx, ty = 0, 0
angle1 = atan2(ty - py, tx - px)

x, y = 10, 10
fx, fy = -10, 10
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
    
