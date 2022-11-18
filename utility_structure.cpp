/**
  * @file utility_functions.hpp
  * @brief contains some utility functions and bot class
  * @copyright 2020 KENCONTROLS CO. Ltd. All Rights Reserved
  */
#pragma once
#include <iostream>
#include <math.h>
#include <vector>
#include <stdlib.h>
#include <chrono>
#include <thread>


#define max(a, b) a>b?a:b
#define min(a, b) a<b?a:b

#define BOT_LENGTH getLength()
#define BOT_BREADTH getBreadth()
#define BOT_SIZE ((max(BOT_LENGTH, BOT_BREADTH))/2)
#define NUM getNumberOfBots()
#define DELTA 0.05
#define SAFE_DISTANCE (BOT_SIZE * 1.5)

namespace ats_library {
    /**
    * @fn split
    * @brief split string with comma
    * @param str inputted string
    * @param del token to split string
    * @return  splitted strings
    */
   inline std::vector<std::string> split(std::string str, char del){
       int first=0;
       int last=str.find_first_of(del);

       std::vector<std::string> result;

       while(first<str.size()){
           std::string substr(str, first, last-first);

           result.push_back(substr);

           first=last+1;
           last=str.find_first_of(del, first);

           if(last==std::string::npos){
               last=str.size();
           }
       }

       return result;
   }

    /**
    * @struct Point
    * @brief stores a 2D point
    * @param x double x coordinate
    * @param y double y coordinate
    */
    struct Point{
        double x, y;
    };

    /**
    * @fn orientation
    * @brief finds the orientation of 2 line segments
    * @param p is the starting point of a line segment
    * @param q is the ending point of a line segment
    * @param r is the starting/ending point of another line segment
    * @return  whether the line segments are clockwise, anti clockwise or collinear
    */
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

    /**
    * @fn onSegment
    * @brief finds the orientation of 2 line segments
    * @param p is the starting point of a line segment
    * @param q is the starting/ending point of another line segment
    * @param r is the ending point of a line segment
    * @return whether the line segments are on each other
    */
    bool onSegment(Point p, Point q, Point r){
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)))
            return true;
        return false;
    }

    /**
    * @fn doIntersect
    * @brief finds if two line segments intersect
    * @param p1 is the starting point of a line segment
    * @param q1 is the ending point of a line segment
    * @param p2 is the starting point of another line segment
    * @param q2 is the ending point of another line segment
    * @return  true is line segments intersect, false otherwise
    */
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

}
