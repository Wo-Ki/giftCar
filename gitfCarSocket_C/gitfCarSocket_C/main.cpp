//
//  main.cpp
//  gitfCarSocket_C
//
//  Created by  WangKai on 2018/3/16.
//  Copyright © 2018年  WangKai. All rights reserved.
//

#include <iostream>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>


#define HOST "192.168.100.3"
#define PORT 8989
#define SIZE 256

int main(){
    int fd;
    fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in saddr;
    bzero(&saddr, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_port = htons(PORT);
    saddr.sin_addr.s_addr = inet_addr(HOST);
    
    int conn;
    conn = connect(fd, (struct sockaddr*)&saddr, sizeof(saddr));
    if(conn<0){
        perror("conn error");
        exit(1);
    }
    
    char buf[SIZE];
    while(fgets(buf, SIZE, stdin) != NULL){
        printf("%s", buf);
        write(fd, buf, SIZE);
        bzero(buf, SIZE);
    }
    
    return 0;
}
