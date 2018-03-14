#include <stdio.h>
#include <wiringPi.h>

#define RAPin 24
#define RBPin 5
void countFunc();

int count=0;

void countFunc(){
    count++;
}

int main()
{
    wiringPiSetup();
    pinMode(RAPin, OUTPUT);
    pinMode(RBPin, OUTPUT);

    wiringPiISR(RAPin,INT_EDGE_BOTH,countFunc);
    wiringPiISR(RBPin,INT_EDGE_BOTH,countFunc);

    int last=0;
    while(1)
    {
        if(millis()-last>500 || last == 0){
            last = millis();
            float radiusSpeed = (count / 520.0 * (2*3.141592))*2;
            printf("Speed radius A:%.2f rad/s\n", radiusSpeed);
            printf("Speed A:%.2f m/s\n", (radiusSpeed*0.03));
            count=0;
        }
    }
}

