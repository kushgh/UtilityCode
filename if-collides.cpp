#include <iostream>
#include <math.h>
#include <vector>
#include <stdlib.h>
#include <chrono>
#include <thread>

// Size of the bots
#define BOT_SIZE 2
#define NUM 4

struct Bot{
    int id;
    double x, y, th, tx, ty, speed, vel_x, vel_y, next_x, next_y;
    void setValues(){
        x = 1+ (rand()%1000)/10.0;
        y = 1+ (rand()%1000)/10.0;
        th = (rand()%6)/1.0;;
        speed = rand()%10/10.0;
        tx = 1+ (rand()%1000)/10.0;
        ty = 1+ (rand()%1000)/10.0;
         
        setSpeedComponents();  
        setNextTarget();     
    }
    void setSpeedComponents(){
        vel_x = speed*cos(th);
        vel_y = speed*sin(th);
    }
    void setNextTarget(){
        next_x = 1+ (rand()%1000)/10.0;
        next_y = 1+ (rand()%1000)/10.0;
    }
    void resetTarget(){
        tx = next_x;
        ty = next_y;
        setNextTarget();
    }
    void updateCurrentPosition(){
        std::this_thread::sleep_for(std::chrono::milliseconds(300));
        x += 1.0;
        y += 1.0;
    }
    void update(std::vector<Bot> bots){
        for(auto bot:bots){
            if (&bot == this){
                continue;
            }
            if doIntersect(){};
        }
    }
};

bool collision(Bot b1, Bot b2){
    
    // bot 1
    auto x1=b1.x, y1 = b1.y;                             // current position
    auto tx1=b1.tx, ty1 = b1.ty;                            // interim target
    auto angle1 = b1.th; // angle of bot against x axis
    auto speed1 = b1.speed;                                  // speed of bot

    // bot 2
    auto x2=b2.x, y2 = b2.y;                             // current position
    auto tx2=b2.tx, ty2 = b2.ty;                            // interim target
    auto angle2 = b2.th; // angle of bot against x axis
    auto speed2 = b2.speed;                                  // speed of bot


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
        //
    }   

    std::cout<<collision;
    return collision;
}

int main(){

    std::vector<Bot> bots;

    for(auto bot:bots){
        bot.update();
    }
    for(auto bot:bots){
        // if bot reached destination, select new target
        bot.updateCurrentPosition();
        auto px = bot.x, py = bot.y, tx = bot.tx, ty = bot.ty;
        if (hypot(px - tx, py - ty) < BOT_SIZE * 2 + 0.05 * BOT_SIZE) {
            bot.tx = bot.next_x;
            bot.tx = bot.next_y;
            bot.resetTarget();
        }
    }


    return 0;

}