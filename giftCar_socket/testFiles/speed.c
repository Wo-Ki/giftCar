#include <stdio.h>
#include <wiringPi.h>

#define RAPin 24
#define RBPin 5
void countFunc();

int count=0;

int encoder_r = 24;
int direction_r = 5;
long velocity_r = 0;

//void countFunc(){
//    count++;
//}

void countFunc(){
            if(digitalRead(encoder_r) == LOW){
                if(digitalRead(direction_r) == LOW)
                    velocity_r += 1;
                else
                    velocity_r -= 1;
              }
         else{
            if(digitalRead(direction_r) == LOW)
                velocity_r -= 1;
            else
                velocity_r += 1;
             }
}

int main()
{
    wiringPiSetup();
    pinMode(RAPin, INPUT);
    pinMode(RBPin, INPUT);

    wiringPiISR(RAPin,INT_EDGE_BOTH,countFunc);
    wiringPiISR(RBPin,INT_EDGE_BOTH,countFunc);

    int last=0;
    while(1)
    {
        if(millis()-last>500 || last == 0){
            last = millis();
            float radiusSpeed = (velocity_r / 520.0 * (2*3.141592))*2;
            printf("Speed radius A:%.2f rad/s\n", radiusSpeed);
            printf("Speed A:%.2f m/s\n", (radiusSpeed*0.03));
            velocity_r=0;
        }
    }
}

