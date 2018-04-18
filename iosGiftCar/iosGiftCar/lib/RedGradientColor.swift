//
//  RedGradientColor.swift
//  使用CoreGraphic实现绘图操作
//
//  Created by  WangKai on 2016/11/29.
//  Copyright © 2016年  WangKai. All rights reserved.
//

import UIKit

class RedGradientColor: GradientColor {
    
    override func createColor() {
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let  count:size_t = 4
        let locations:[CGFloat] = [0,0.33,0.66,1]
        let colorComponents:[CGFloat] = [
            //red, green, blue, alpha
            0.85, 0, 0,  1.0,
            1, 0, 0,  1.0,
            0.85, 0.3, 0, 1.0,
            0.1, 0, 0.9, 1.0
        ]
        
        self.gradientRef = CGGradient(colorSpace: colorSpace, colorComponents: colorComponents, locations: locations, count: count)
        
    }
}
