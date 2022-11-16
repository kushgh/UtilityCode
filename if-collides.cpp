#include <iostream>
#include <math.h>
// Size of the bots
#define BOT_SIZE 2

int main(){

    // bot 1
    auto x1=0.0, y1 = 20.0;                             // current position
    auto tx1=0.0, ty1 = 0.0;                            // interim target
    auto angle1 = atan2(ty1 - y1, tx1 - x1) * 180/M_PI; // angle of bot against x axis
    auto speed1 = 1.0;                                  // speed of bot

    // bot 2
    auto x2=10.0, y2 = 10.0;                            // current position
    auto tx2=-10.0, ty2 = 10.0;                         // interim target
    auto angle2 = atan2(ty2 - y2, tx2 - x2) * 180/M_PI; // angle of bot against x axis
    auto speed2 = 1.0;                                  // speed of bot

    // speed of a 
    auto xa = speed1*cos(angle1); // in x direction
    auto ya = speed1*sin(angle1); // in y direction
    // speed of b
    auto xb = speed2*cos(angle2); // in x direction
    auto yb = speed2*sin(angle2); // in y direction

    // mintime to collision 
    auto tm = ((xa - xb)*(x2 - x1) + (ya - yb)*(y2 - y1)) / ((xa - xb)*(xa - xb) + (ya - yb)*(ya - yb));
    // mindist to collision
    auto ds = hypot(tm*xa - tm*xb + x1 - x2, tm*ya - tm*yb + y1 - y2);

    // possible collision on route or not
    auto collision = false;

    // collision condition
    if (ds <= BOT_SIZE*2 + 0.05*BOT_SIZE){
        collision = true;
        // now do something
    }   

    std::cout<<collision;

    return 0;

}