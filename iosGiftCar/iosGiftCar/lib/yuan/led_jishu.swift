//
//  led_jishu.swift
//  BlueTest2
//
//  Created by  WangKai on 2017/4/3.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class led_jishu: UIView {
    var gradientlayer:CAGradientLayer!
    var gradientlayer2:CAGradientLayer!
    var shapelayer:CAShapeLayer!
    var arrayColor:[CGColor]!
    var arrayColor2:[CGColor]!
    var label:UILabel!
    var label2:UILabel!
    var font1:UIFont!
    var font2:UIFont!
    var z:CGFloat = 0{
        didSet{
            self.setNeedsDisplay()
        }
    }
    var jishuText:String = ""
    override init(frame: CGRect) {
        super.init(frame: frame)
        csh()
    }
    func csh(){
        gradientlayer = CAGradientLayer(layer: layer)
        arrayColor = [UIColor.init(red: 1, green: 0.50196, blue: 0, alpha: 1).cgColor,UIColor.white.cgColor]
        gradientlayer.colors = arrayColor
        gradientlayer.startPoint = CGPoint(x: 0, y: 0)
        gradientlayer.endPoint = CGPoint(x: 0, y: 1.5)
        gradientlayer.cornerRadius = 7
        
        gradientlayer2 = CAGradientLayer(layer: layer)
        arrayColor2 = [UIColor.clear.cgColor,UIColor.init(red: 1, green: 1, blue: 1, alpha: 0.3).cgColor]
        gradientlayer2.colors = arrayColor2
        gradientlayer2.startPoint = CGPoint(x: 0, y: 0)
        gradientlayer2.endPoint = CGPoint(x: 0.7, y: 0.5)
        gradientlayer2.cornerRadius = 7.0
        
        label = UILabel()
        label.textAlignment = NSTextAlignment(rawValue: 1)!
        label.textColor = UIColor.black
        
        label2 = UILabel()
        label2.textAlignment = NSTextAlignment(rawValue: 1)!
        label2.textColor = UIColor.red
        
        self.layer.addSublayer(gradientlayer)
        self.layer.addSublayer(gradientlayer2)
        self.insertSubview(label, at: 1)
        self.insertSubview(label2, at: 1)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func schcs(rect:CGRect){
        gradientlayer.frame = rect
        gradientlayer2.frame = rect
        
        label.frame = rect
        font1 = UIFont(name: "DBLCDTempBlack", size: rect.size.height/2)
        label.font = font1
        if jishuText == "℃"{
            label.text = String(format: "%.2f", z)
        }else if jishuText == "%"{
         label.text = String(format: "%.2f", z)
        
        }
        
        label2.frame = CGRect(x: 4*rect.size.width/5, y: 0, width: rect.size.width/5, height: rect.size.height/3)
        font2 = UIFont(name: "DBLCDTempBlack", size: rect.size.height/4)
        label2.font = font2
        label2.text = jishuText
    }
    
    override func draw(_ rect: CGRect) {
        schcs(rect: rect)
    }
   
}
