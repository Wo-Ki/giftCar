//
//  RGBColor.swift
//  使用CoreGraphic实现绘图操作
//
//  Created by  WangKai on 2016/11/29.
//  Copyright © 2016年  WangKai. All rights reserved.
//

import UIKit

class RGBColor: NSObject {

    var red = CGFloat()
    var green = CGFloat()
    var blue = CGFloat()
    var alpha = CGFloat()
    
    func colorWithRed(red:CGFloat,green:CGFloat,blue:CGFloat,alpha:CGFloat)->RGBColor{
        let color = RGBColor()
        color.red = red
        color.green = green
        color.blue = blue
        color.alpha = alpha
        
        return color
    }
    
    func colorWithUIColor(color:UIColor)->RGBColor{
        let tmpColor = RGBColor()
        var red:CGFloat = 0
        var green:CGFloat = 0
        var blue:CGFloat = 0
        var alpha:CGFloat = 0
        color.getRed(&red, green: &green, blue: &blue, alpha: &alpha)
        tmpColor.red = red
        tmpColor.green = green
        tmpColor.blue = blue
        tmpColor.alpha = alpha
        
        return tmpColor
    }
    
    func randomColor()->RGBColor{
        let color = RGBColor()
        
        color.red = CGFloat(arc4random()%256)/255
        color.green = CGFloat(arc4random()%256)/255
        color.blue = CGFloat(arc4random()%256)/255
        color.alpha = CGFloat(arc4random()%256)/255
        
        return color
    }
    
    func randomColorWithAlpha(alpha:CGFloat)->RGBColor{
        let color = RGBColor()
        
        color.red = CGFloat(arc4random()%256)/255
        color.green = CGFloat(arc4random()%256)/255
        color.blue = CGFloat(arc4random()%256)/255
        color.alpha = (alpha < 0 || alpha > 1) ? 1 : alpha
        
        return color
    }
    
 
}
