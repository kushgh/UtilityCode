target_x = 16.95
target_y = 90.95

if (True):
    # linkkey1=(boost::format("%d:%d") % optnodes[winner][count-1] % optnodes[winner][count]).str()
    # linkkey2=(boost::format("%d:%d") % optnodes[winner][count] % optnodes[winner][count+1]).str()
    # pathid1=key_to_path_list[winner][linkkey1]
    # pathid2=key_to_path_list[winner][linkkey2]
    pathid1=4
    pathid2=20
    
    # temp initial virtual waypoint of A
    x1 = 9.75701
    y1 = 87.48974
    # temp intermediate virtual waypoint of B, from A to B
    x21 = 16.407
    y21 = 91.789
    # temp intermediate virtual waypoint of B, from B to C
    x23 = 16.477
    y23 = 91.831
    # temp final virtual waypoint of C
    x3 = 24.777
    y3 = 96.281

    # if paths are single-single, take default values commenting as not really necessary
    # if(x21 == x23 && y21 == y23) break

    # if paths are multi-single, single-multi, multi-multi, or single-single calculate intersection
    # slope of initial to intermediate
    m1 = (y21-y1)/(x21-x1)  
    # slope of intermediate to final
    m2 = (y3-y23)/(x3-x23)  

    # the tolerance value of difference in slopes
    delta = 0.0001
    if (abs(m1-m2)>delta):  # if the slopes vary significantly
        # calculate intersection point
        target_x = ( (m1*x1 - m2*x3) + (y3 - y1) )/(m1-m2)
        target_y = ( (m1*m2*(x1 - x3)) + (m1*y3 - m2*y1) )/(m1-m2)
        x = input()
    x = input()



# Json target_pose = Json::object 
#     "x", target_x,
#     "y", target_y,
#     "th", botstatus_[bot_id].pose_th*180.0/M_PI


