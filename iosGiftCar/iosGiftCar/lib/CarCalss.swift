//
//  CarCalss.swift
//  iosGiftCar
//
//  Created by  WangKai on 2018/4/17.
//  Copyright © 2018年  WangKai. All rights reserved.
//

import Foundation
import UIKit

class CarClass: NSObject {

    class func dealWithReceiveData(carInformationView: CarInformationView,data: Data){ // 处理下发的数据，更新视图
        if let json = try? JSON(data: data){
//            print("json result:",json)
            if(json["M"] == "update"){
                if(json["K"] == "dht11"){ // dht11
                    
                    if let hum = json["V"]["hum"].float{
                        print("hum:",hum)
                        carInformationView.updateHum(hum: hum)
            
                    }
                    if let tem = json["V"]["tem"].float{
                        print("tem:",tem)
                        carInformationView.updateTem(tem: tem)
                    }
                }else if(json["K"] == "mpu9250"){
                    // accelerate
                    let ay = json["V"]["ax"].float! / 16384.0// 因为实际轴和显示轴不一致,所以x对应y，16384.0为最大值,ay为角度
                    let ax = json["V"]["ay"].float! / 16384.0
                    let _ = json["V"]["az"].float! / 16384.0
                    
                    // gyro
                    let gx = json["V"]["gx"].float! / 250.0 * 360 // gx,gy,gz转换成角度，最大值为250
                    let gy = json["V"]["gy"].float! / 250.0 * 360
                    let gz = json["V"]["gz"].float! / 250.0 * 360
                    
                    carInformationView.updateLevelCircle(xValue: -ax, yValue: -ay)
                    carInformationView.updateGyroscope(x: gx, y: gy, z: gz)
                }
                else if(json["K"] == "avoid"){
                    print("avoid status:",json["V"])
                    
                }else if(json["K"] == "speed"){
                    let speed = json["V"].float!
                    print("carInformationView:",speed)
                    carInformationView.updateSpeed(speed: speed)
                }
            }
        }
    }
}
