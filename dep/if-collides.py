from math import sin, cos, pi, atan2, hypot, sqrt, pow

# bot 1
px, py = 0, 20
tx, ty = 0, 0
angle1 = atan2(ty - py, tx - px) * 180/pi
speed1 = 1

# bot 2
x, y = 10, 10
fx, fy = -10, 10
angle2 = atan2(fy - y, fx - x) * 180/pi
speed2 = 1

xa = speed1*cos(angle1)
ya = speed1*sin(angle1)
xb = speed2*cos(angle2)
yb = speed2*sin(angle2)

# a , b = xa**2 + ya**2, xb**2 + yb**2

tm = ((xa - xb)*(x - px) + (ya - yb)*(y - py)) / ((xa - xb)**2 + (ya - yb)**2)

ds = sqrt( pow(tm*xa - tm*xb + px - x, 2) + pow(tm*ya - tm*yb + py - y, 2) )

collision = False
if ds <= 4:
    collision = True
                
print(collision)

# m1 = (ty-py)/(tx-px)  
# # slope of intermediate to final
# m2 = (fy-y)/(fx-x)

# intersect_x = ( (m1*px - m2*fx) + (fy - py) )/(m1-m2)
# intersect_y = ( (m1*m2*(px - fx)) + (m1*fy - m2*py) )/(m1-m2)

# print()
  