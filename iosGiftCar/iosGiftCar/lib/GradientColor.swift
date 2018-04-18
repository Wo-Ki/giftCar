//
//  GradientColor.swift
//  使用CoreGraphic实现绘图操作
//
//  Created by  WangKai on 2016/11/29.
//  Copyright © 2016年  WangKai. All rights reserved.
//

import UIKit

class GradientColor: NSObject {

    //渐变色对象
    var gradientRef:Any! = nil
    //渐变色绘制起始点
    var gradientStarPoint:CGPoint! = nil
    //渐变色绘制结束点
    var gradientEndPoint:CGPoint! = nil
    
    func createColor(){
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        
        let count:size_t = 3
        let locations:[CGFloat] = [0.0,0.5,1.0]
        let colorComponents:[CGFloat] = [
            //red, green, blue, alpha
            0.254, 0.599, 0.82,  1.0,
            0.192, 0.525, 0.75,  1.0,
            0.096, 0.415, 0.686, 1.0
        ]
        
        gradientRef = CGGradient(colorSpace: colorSpace, colorComponents: colorComponents, locations: locations, count: count)
        
        
        
    }
    
    func createColorWithStartPoint(startPoint:CGPoint,endPoint:CGPoint)->GradientColor{
        let color = GradientColor()
        color.gradientStarPoint = startPoint
        color.gradientEndPoint = endPoint
        
        color.createColor()
        
        return color
    }
}
