#include <stdio.h>
#include <wiringPi.h>

int encoder_r = 5;
int direction_r = 6;
long velocity_r = 0;

void rightCountFunc(){
        if(digitalRead(encoder_r) == LOW){
            if(digitalRead(direction_r) == LOW)
                velocity_r++;
            else
                velocity_r--;
          }
         else{
            if(digitalRead(direction_r) == LOW)
                velocity_r--;
            else
                velocity_r++;
             }
}

int returnRightCount(){
    return velocity_r;
}

int main()
{
    wiringPiSetup();
    pinMode(direction_r, INPUT);
    pinMode(velocity_r, INPUT);
    wiringPiISR(encoder_r,INT_EDGE_BOTH,rightCountFunc);
}