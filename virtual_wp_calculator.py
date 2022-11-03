from math import sqrt
import pyperclip

# wps = {
#       2: (10.3, 86.65),
#       3: (10.3, 90.95),
#       5: (24.05, 85.7),
#       10: (37.25, 85.7),
#       12: (42.6, 91.1),
#       19: (25.25, 95.4),
#       }

# link = {"2:3":4,
#         "3:2":44,
#         "3:19":20,
#         "19:3":2020,
#         "3:5":6,
#         "5:3":66,
#         "10:12":13,
#         "12:10":1313
#         }

# paths = {4:(2,3),
#         44:(3,2),
#         20:(3,19),
#         2020:(19,3),
#         6:(3,5),
#         66:(5,3),
#         13:(10,12),
#         1313:(12,10)
#         }

wps = {
      8: (21.8, 88.45),
      6: (10.6, 87.15)
      }

link = {"6:8":12,
        "8:6":13
        }


paths = {
        12:(6,8),
        13:(8,6)
        }


site = "3"
# path width
w = 3
def cal(path, x1, y1, x2, y2):
    path = str(path)
    # req's
    dx = x1 - x2
    dy = y1 - y2
    dist = sqrt(dx*dx + dy*dy)
    dx /= dist
    dy /= dist

    # A1
    x11 = x1 + dy*w/2
    y11 = y1 - dx*w/2

    # A2
    x12 = x1 - dy*w/2
    y12 = y1 + dx*w/2

    # B1
    x21 = x2 + dy*w/2
    y21 = y2 - dx*w/2

    # B2
    x22 = x2 - dy*w/2
    y22 = y2 + dx*w/2

    # if f:
    #     xi = str(round(min(x11, x12), 5))
    #     yi = str(round(max(y11, y12), 5))
    #     xe = str(round(min(x21, x22), 5))
    #     ye = str(round(max(y21, y22), 5))
    # else:
    xi = str(round(x11, 5))
    yi = str(round(y11, 5))
    xe = str(round(x21, 5))
    ye = str(round(y21, 5))
        
    q = "("+site+","+path+","+xi+","+yi+","+xe+","+ye
    print(q+")")
    q+=",0,0,0,0,1,1)"
    # print("A1 = (", x11, y11, ")")
    # print("A2 = (", x12, y12, ")")
    # print("B1 = (", x21, y21, ")")
    # print("B2 = (", x22, y22, ")")
    
    return q

# all req inputs A and B
# x1 = float(input("Enter X1: "))
# y1 = float(input("Enter Y1: "))
# x2 = float(input("Enter X2: "))
# y2 = float(input("Enter Y2: "))

query = """insert into public.path (site_id,id,waypoint_id_1_x,waypoint_id_1_y,waypoint_id_2_x,waypoint_id_2_y,control_point_1_x,control_point_1_y,control_point_2_x,control_point_2_y,max_trans_vel,guide_regulation)\nvalues """
for k in paths.keys():
    print("For path - ", k, ", Waypoint link - ", paths[k])
    wp1 = paths[k][0]
    wp2 = paths[k][1]
    # flag = input("left(0) or right(1) ? ")
    query += cal(k,wps[wp1][0], wps[wp1][1],wps[wp2][0],wps[wp2][1]) + ",\n"
    
query = query[:-2]+";"

pyperclip.copy(query)
print("Final Query : \n",query)
print("QUERY COPIED TO CLIPBOARD!\n")