from math import sqrt
import pyperclip

site = "3"
# path width
w = 3
query = ""

# wps = {
#       2: (10.3, 86.65),
#       3: (10.3, 90.95),
#       5: (24.05, 85.7),
#       10: (37.25, 85.7),
#       12: (42.6, 91.1),
#       19: (10.3, 95.4),
#       }

wps = {
      8: (21.8, 88.45),
      6: (10.6, 87.15)
      }


# paths = {4:(2,3),
#         44:(3,2),
#         20:(3,19),
#         2020:(19,3),
#         6:(3,5),
#         66:(5,3),
#         13:(10,12),
#         1313:(12,10)
#         }


paths = {
        12:(6,8),
        13:(8,6)
        }

# all_paths = [
# [4,9.3,86.65,9.3,90.95],
# [44,11.3,90.95,11.3,86.65],
# [20,10.01471,91.90844,24.96471,96.35844],
# [2020,25.53529,94.44156,10.58529,89.99156],
# [6,10.6567,91.88422,24.4067,86.63422],
# [66,23.6933,84.76578,9.9433,90.01578],
# [13,36.53961,86.40381,41.88961,91.80381],
# [1313,43.31039,90.39619,37.96039,84.99619]
# ]

all_paths = [
    [12,10.42705,88.64,21.62705,89.94],
    [13,21.97295,86.96,10.77295,85.66]
    ] 
# virtual = [
# [44,11.3,90.95,11.3,86.65],
# [2020,25.53529,94.44156,10.58529,89.99156],
# [66,23.6933,84.76578,9.9433,90.01578],
# [1313,43.31039,90.39619,37.96039,84.99619]]

# real = [
# [4,9.3,86.65,9.3,90.95],
# [20,10.01471,91.90844,24.96471,96.35844],
# [6,10.6567,91.88422,24.4067,86.63422],
# [13,36.53961,86.40381,41.88961,91.80381]]

# link = [[2,3,4],
#         [3,2,44],
#         [3,19,20],
#         [19,3,2020],
#         [3,5,6],
#         [5,3,66],
#         [10,12,13],
#         [12,10,1313]
#         ]

link = [
        [6,8,12],
        [8,6,13]
]

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

    # B1
    x21 = x2 + dy*w/2
    y21 = y2 - dx*w/2

    xi = str(round(x11, 5))
    yi = str(round(y11, 5))
    xe = str(round(x21, 5))
    ye = str(round(y21, 5))
        
    q = "("+site+","+path+","+xi+","+yi+","+xe+","+ye
    print(q+")")
    q+=",0,0,0,0,1,1)"
  
    return q

# delete all paths first
for i in range(len(all_paths)):
    query+=f"delete from public.path where id={all_paths[i][0]};\n"; 

# insert path query
query += """insert into public.path (site_id,id,waypoint_id_1_x,waypoint_id_1_y,waypoint_id_2_x,waypoint_id_2_y,control_point_1_x,control_point_1_y,control_point_2_x,control_point_2_y,max_trans_vel,guide_regulation)\nvalues """
for k in paths.keys():
    print("For path - ", k, ", Waypoint link - ", paths[k])
    wp1 = paths[k][0]
    wp2 = paths[k][1]
    # flag = input("left(0) or right(1) ? ")
    query += cal(k,wps[wp1][0], wps[wp1][1],wps[wp2][0],wps[wp2][1]) + ",\n"

# completed waypoint insert query
query = query[:-2]+";\n"

# links updated
for i in range(len(link)):
    p = link[i][2]
    w2 = link[i][1]
    w1 = link[i][0]
    
    query += f"""\nUPDATE link
    SET path_id={p}
    WHERE waypoint_id_1={w1} AND waypoint_id_2={w2};\n"""

pyperclip.copy(query)
print("Final Query : \n",query)
print("QUERY COPIED TO CLIPBOARD!\n")