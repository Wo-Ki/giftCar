//
//  yuan2_sc.swift
//  BlueTest2
//
//  Created by  WangKai on 2017/4/3.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class yuan2_sc: UIView {

    var shaperlayer:CAShapeLayer!
    var point:CGPoint! //中心坐标
    var bj:CGFloat = 0 //半斤
    var sc_kd:CGFloat = 0{ //温度计线宽
        didSet{
            self.setNeedsDisplay()
        }
    }
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.chushihua()
    }
    func chushihua(){
        shaperlayer = CAShapeLayer(layer: layer)
        shaperlayer.fillColor = UIColor.clear.cgColor
        shaperlayer.strokeColor = UIColor.red.cgColor
        shaperlayer.backgroundColor = UIColor.clear.cgColor
        shaperlayer.lineJoin = kCALineJoinRound
        shaperlayer.lineCap = kCALineCapRound
        shaperlayer.frame = CGRect(x: 0, y: 0, width: 0, height: 0)
    }
    func setcanshu(rect:CGRect){
        bj = rect.size.height > rect.size.width ? rect.size.width/2 : rect.size.height/2 - sc_kd/2
        
        point = CGPoint(x: rect.size.width/2, y: rect.size.height/2)
        if shaperlayer.frame.origin.x == 0 || shaperlayer.frame.origin.y == 0 || shaperlayer.frame.size.width == 0 || shaperlayer.frame.size.height == 0{
            shaperlayer.frame = rect
            shaperlayer.lineWidth = sc_kd
            let apath = UIBezierPath(arcCenter: point, radius: bj, startAngle: CGFloat.pi/2.0, endAngle: 2*CGFloat.pi, clockwise: true)
            shaperlayer.path = apath.cgPath
            shaperlayer.strokeEnd = 1
            
            //为了旋转角度
            shaperlayer.transform = CATransform3DMakeRotation(CGFloat.pi/4, 0, 0, 1)
        }
        
    }
    override func draw(_ rect: CGRect) {
        self.setcanshu(rect: rect)
        self.draw_jby()
        self.draw_mb();
    }
    func draw_jby(){
        let components:[CGFloat] = [
            0,0,0,0.1, // start color
            1,1,1,0.5,
            0,0,0,0,1  //end color
        ]
        
        let space = CGColorSpaceCreateDeviceRGB()
        let gradient = CGGradient(colorSpace: space, colorComponents: components, locations: nil, count: 3)
        
        let start = point
        let end = point
        
        let startRadius = bj+sc_kd/2
        let endRadius = bj - sc_kd/2
        
        let graCtx = UIGraphicsGetCurrentContext()
        graCtx?.drawRadialGradient(gradient!, startCenter: start!, startRadius: startRadius, endCenter: end!, endRadius: endRadius, options: CGGradientDrawingOptions(rawValue: 0))
    }
    func draw_mb(){
        self.layer.mask = shaperlayer
    }
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func setSc_kd(sc_kd:CGFloat){
        self.sc_kd = sc_kd
        self.setNeedsDisplay()
    }

}
