#include <stdio.h>
#include <wiringPi.h>

#define RAPin 24
#define RBPin 25
void countFunc();

int count=0;

int encoder_r = 5;
int direction_r = 6;
long velocity_r = 0;

//void countFunc(){
//    count++;
//}

void countFunc(){
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

int returnCount(){
    printf("velocity_r%d\n",velocity_r);
    return velocity_r;
}
int main()
{
    wiringPiSetup();
    pinMode(direction_r, INPUT);
    pinMode(velocity_r, INPUT);

    wiringPiISR(encoder_r,INT_EDGE_BOTH,countFunc);
//    wiringPiISR(RBPin,INT_EDGE_BOTH,countFunc);

//    int last=0;
//    while(1)
//    {
//        if(millis()-last>500 || last == 0){
//            last = millis();
//            float radiusSpeed = (velocity_r / 520.0 * (2*3.141592))*2;
//            printf("Speed radius A:%.2f rad/s\n", radiusSpeed);
//            printf("Speed A:%.2f m/s\n", (radiusSpeed*0.03));
//              printf("velocity_r:%d\n", velocity_r);
//            velocity_r=0;
//        }
//    }
//    while(1){
//        ;
//    }
}

