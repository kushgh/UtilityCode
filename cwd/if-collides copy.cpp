    void PAUSE_JOB(){ }
    void RESUME_JOB(){ }
    void INCREASE_WAIT_COUNT(){ }
    void PAUSE_WAIT_COUNT(){ }
    void RESET_WAIT_COUNT(){ }
    
    void setNextTarget(){
        tg.x = next.x;
        tg.y = next.y;
        setPoint(next);
    }
    
    
    
    void printPose(){ std::cout<<"\nBot ("<<id<<") at ("<<pose.x<<","<<pose.y<<") --> ("<<tg.x<<","<<tg.y<<")"; }
    
