linkkey1=(boost::format("%d:%d") % optnodes[winner][count-1] % optnodes[winner][count]).str();
linkkey2=(boost::format("%d:%d") % optnodes[winner][count] % optnodes[winner][count+1]).str();
pathid1=key_to_path_list[winner][linkkey1];
pathid2=key_to_path_list[winner][linkkey2];

// temp initial virtual waypoint of A
x1 = db_.paths[pathid1].start.x;
y1 = db_.paths[pathid1].start.y;
// temp intermediate virtual waypoint of B, from A to B
x21 = db_.paths[pathid1].end.x;
y21 = db_.paths[pathid1].end.y;
// temp intermediate virtual waypoint of B, from B to C
x23 = db_.paths[pathid2].start.x;
y23 = db_.paths[pathid2].start.y;
// temp final virtual waypoint of C
x3 = db_.paths[pathid2].end.x;
y3 = db_.paths[pathid2].end.y;


m1 = (y21-y1)/(x21-x1);  
m2 = (y3-y23)/(x3-x23);  


target_x = ( (m1*x1 - m2*x3) + (y1 - y3) )/(m1-m2);
target_y = ( (m1*m2*(x1 - x3)) + (m1*y3 - m2*y1) )/(m1-m2);