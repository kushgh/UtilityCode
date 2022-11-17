#include <iostream>
#include <math.h>
#include <vector>
#include <stdlib.h>
#include <chrono>
#include <thread>

#define BOT_SIZE 3
#define NUM 2
#define DELTA 0.05
#define SAFE_DISTANCE (BOT_SIZE * 1.5)

#define max(a, b) a>b?a:b
#define min(a, b) a<b?a:b

struct Point{
    double x, y;
};

int orientation(Point p, Point q, Point r){
    auto val = ((q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y));
    if (val > 0){
        // Clockwise orientation
        return 1;
    }
    else if (val < 0){
        // Counterclockwise orientation
        return 2;
    }
    // Collinear orientation
    return 0;
}
bool onSegment(Point p, Point q, Point r){
	if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
		(q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)))
		return true;
	return false;
}
bool doIntersect(Point p1, Point q1, Point p2, Point q2){
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    // General case
	if ((o1 != o2) and (o3 != o4)){
		return true;
    }
	// Special Cases
	if (((o1 == 0) and onSegment(p1, p2, q1)) ||    // p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        ((o2 == 0) and onSegment(p1, q2, q1)) ||    // p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        ((o3 == 0) and onSegment(p2, p1, q2)) ||    // p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        ((o4 == 0) and onSegment(p2, q1, q2))){       // p2 , q2 and q1 are collinear and q1 lies on segment p2q2
		return true;
    }
	// If none of the cases
	return false;
}

class Bot{
    public:
    int id;
    double th,speed;
    Point pose, tg, vel, next, dest;
    double wait_time;
    Bot(int id):id(id){
        pose.x = 1 + (rand()%1000)/10.0;
        pose.y = 1 + (rand()%1000)/10.0;
        speed = rand()%1000/1000.0;
        tg.x = 1 + (rand()%1000)/10.0;
        tg.y = 1 + (rand()%1000)/10.0;
        th =  atan2(pose.y - tg.y, pose.x - tg.x);
        wait_time = 0;

        dest.x = 1 + (rand()%1000)/10.0;
        dest.y = 1 + (rand()%1000)/10.0;
        
        std::cout<<"Created Bot "<<id<<std::endl;

        setSpeedComponents();  
        setNext();     
    }
    ~Bot(){
        std::cout<<"Destroyed Bot";
    }
    void PAUSE_JOB(){ }
    void RESUME_JOB(){ }
    void INCREASE_WAIT_COUNT(){ }
    void PAUSE_WAIT_COUNT(){ }
    void RESET_WAIT_COUNT(){ }
    
    void setSpeedComponents(){
        vel.x = speed*cos(th);
        vel.y = speed*sin(th);
    }
    void setNext(){
        next.x = 1+ (rand()%1000)/10.0;
        next.y = 1+ (rand()%1000)/10.0;
    }
    void setNextTarget(){
        tg.x = next.x;
        tg.y = next.y;
        setNext();
    }
    void updateCurrentPosition(){
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
        pose.x += vel.x;
        pose.y += vel.y;
        if (pose.x > 100){ pose.x = pose.x - 100; }
        if (pose.x < -100){ pose.x = pose.x + 100; }
        if (pose.y > 100){ pose.y = pose.y - 100; }
        if (pose.y < -100){ pose.y = pose.y + 100; }
    }
    void printPose(){ std::cout<<"\nBot ("<<id<<") at ("<<pose.x<<","<<pose.y<<") --> ("<<tg.x<<","<<tg.y<<")"; }
    void getUpdate(std::vector<Bot> &bots){
        for(auto &bot:bots){
            if (&bot == this){
                continue;
            }
            Point p={pose.x, pose.y}, t={tg.x, tg.y}, q={bot.pose.x, bot.pose.y}, f={bot.tg.x, bot.tg.y};
            if (doIntersect(p, t, q, f)){
                Point cp = {0, 0}; //  collsion point
                if (collides(bot, cp)){
                    // distance from target
                    auto dtg1 = hypot(pose.x - tg.x, pose.y - tg.y);
                    auto dtg2 = hypot(bot.pose.x - bot.tg.x, bot.pose.y - bot.tg.y);
                    // distance from collison point
                    auto dcp1 = hypot(pose.x - cp.x, pose.y - cp.y);
                    auto dcp2 = hypot(bot.pose.x - cp.x, bot.pose.y - cp.y);
                    
                    if (dcp1 < SAFE_DISTANCE || dcp2 < SAFE_DISTANCE){
                        if (wait_time == bot.wait_time){
                            if(dtg1 > dtg2){
                                PAUSE_JOB();
                                INCREASE_WAIT_COUNT();
                            }
                        else if (wait_time < bot.wait_time){
                            PAUSE_JOB();
                            INCREASE_WAIT_COUNT();
                        }
                        }
                    }
                }
            }
            else{
                RESUME_JOB();
                PAUSE_WAIT_COUNT();

            }
        }
    }
    bool collides(Bot &b, Point &cp){
        // bot 1
        auto x1=pose.x, y1 = pose.y;                             // current position
        auto tx=tg.x, ty=tg.y;
        auto angle1 = th; // angle of bot against x axis
        auto speed1 = speed;                                  // speed of bot

        // bot 2
        auto x2=b.pose.x, y2 = b.pose.y;                             // current position
        auto fx=b.tg.x, fy=b.tg.y;
        auto angle2 = b.th; // angle of bot against x axis
        auto speed2 = b.speed;                                  // speed of bot

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

        // possible collision on route Or not
        auto collision = false;;

        // collision condition
        if (ds <= BOT_SIZE*2 + 0.05*BOT_SIZE){
            collision = true;
            
            auto m1 = 0.0, m2 = 0.0;
            if (abs(tx - x1)>DELTA){
                m1 = (ty-x1)/(tx-x1);
            }
            if (abs(fx - x2)>DELTA){
            m2 = (fy-y2)/(fx-x2);
            }
            cp.x = ( (m1*x1 - m2*fx) + (fy - y1) )/(m1-m2);
            cp.y = ( (m1*m2*(x1 - fx)) + (m1*fy - m2*y1) )/(m1-m2);
        }   

        std::cout<<collision;
        return collision;
    }

};


int main(){

    std::vector<Bot> bots;
    // create bots
    for(int i = 0; i<NUM; ++i) {
        Bot temp(i+1);
        bots.push_back(temp);
    }
    auto previous_time = std::chrono::steady_clock::now();
    while (true){
        // update bot locations
        for(auto &bot:bots){        // very important to declare it as a reference and not a new variable
            bot.getUpdate(bots);
            bot.updateCurrentPosition();
            auto current_time = std::chrono::steady_clock::now();
            if (std::chrono::duration_cast<std::chrono::seconds>(current_time - previous_time).count() >= 1) { 
                bot.printPose(); 
                previous_time = std::chrono::steady_clock::now();
            }
           // if bot reached destination, select new tg
            auto px = bot.pose.x, py = bot.pose.y, tx = bot.tg.x, ty = bot.tg.y, dx = bot.next.x, dy = bot.next.y;
            if (hypot(px - tx, py - ty) < BOT_SIZE * 5 + 0.05 * BOT_SIZE) { // reached interim target
                bot.tg.x = bot.next.x;
                bot.tg.x = bot.next.y;
                bot.setNextTarget();
                if (abs(tx - dx)>DELTA && abs(ty-dy)<DELTA){ // interim target is destination
                    bot.RESET_WAIT_COUNT();
                    std::cout<<"("<<bot.id<<") Reached destination";
                }
            }
        }
    }


    return 0;

}