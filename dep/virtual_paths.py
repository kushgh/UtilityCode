import pyperclip

query = ""

all_paths = [
[4,11.29548,86.55502,17.94548,16.85502],
[44,17.94662,90.86782,11.29662,10.21782],
[20,17.94211,90.82466,26.24211,25.12466],
[2020,26.24445,95.29479,17.94445,16.84479],
[6,17.94442,90.84446,25.04442,23.94446],
[66,25.04471,85.59727,17.94471,16.84727],
[13,38.24238,85.57682,43.59238,42.47682],
[1313,43.5951,91.00114,38.2451,37.15114]]


virtual = [
[44,17.94662,90.86782,11.29662,10.21782],
[2020,26.24445,95.29479,17.94445,16.84479],
[66,25.04471,85.59727,17.94471,16.84727],
[1313,43.5951,91.00114,38.2451,37.15114]]

real = [
[4,11.29548,86.55502,17.94548,16.85502],
[20,17.94211,90.82466,26.24211,25.12466],
[6,17.94442,90.84446,25.04442,23.94446],
[13,38.24238,85.57682,43.59238,42.47682]]

link = [[2,3,4],
        [3,2,44],
        [3,19,20],
        [19,3,2020],
        [3,5,6],
        [5,3,66],
        [10,12,13],
        [12,10,1313]
        ]

# delete all paths first
for i in range(len(all_paths)):
    query+="delete from public.path where id={all_paths[0]};\n"; 

# real paths updated
for i in range(len(real)):
    id = real[i][0]
    x1 = real[i][1]
    y1 = real[i][2]
    x2 = real[i][3]
    y2 = real[i][4]
    query += f"""\nUPDATE path
    SET waypoint_id_1_x={x1},waypoint_id_1_y={y1},waypoint_id_2_x={x2},waypoint_id_2_y={y2}
    WHERE id={id};"""

query +="""
insert into public.path (site_id,id,waypoint_id_1_x,waypoint_id_1_y,waypoint_id_2_x,waypoint_id_2_y,control_point_1_x,control_point_1_y,control_point_2_x,control_point_2_y,max_trans_vel,guide_regulation)
values """

# virtual paths added
site = "1"
for i in range(len(virtual)):
    id = virtual[i][0]
    xi = virtual[i][1]
    yi = virtual[i][2]
    xe = virtual[i][3]
    ye = virtual[i][4]
    query += f"({site},{id},{xi},{yi},{xe},{ye},0,0,0,0,1,1),"


query += ";"

# links updated
for i in range(len(link)):
    p = link[i][2]
    w2 = link[i][1]
    w1 = link[i][0]
    
    query += f"""\nUPDATE link
    SET path_id={p}
    WHERE waypoint_id_1={w1} AND waypoint_id_2={w2};"""


pyperclip.copy(query)





















# all_paths = [[4,9.30452,86.74498,15.95452,17.04498],
# [44,15.95338,91.03218,9.30338,10.38218],
# [20,15.95789,91.07534,24.25789,25.37534],
# [2020,24.25555,95.50521,15.95555,17.05521],
# [6,15.95558,91.05554,23.05558,24.15554],
# [66,23.05529,85.80273,15.95529,17.05273],
# [13,36.25762,85.82318,41.60762,42.72318],
# [1313,41.6049,91.19886,36.2549,37.34886]]
