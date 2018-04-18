//
//  yuan2_zj.swift
//  BlueTest2
//
//  Created by  WangKai on 2017/4/3.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class yuan2_zj: UIView {

    var point:CGPoint! = nil
    var zj_kd:CGFloat = 0
    var z1:CGFloat = 0,z2:CGFloat = 0
    var bj:CGFloat!
    
    var rect1:CGRect!,rect2:CGRect! // 渐变色
    var z:CGFloat = 0{
        didSet{
            self.setNeedsDisplay()
        }
    }
    var gradientlayer1:CAGradientLayer!,gradientlayer2:CAGradientLayer!
    var shapelayer:CAShapeLayer!
    var array1:[CGColor]!,array2:[CGColor]!
    var apath:UIBezierPath!
    var animation:CABasicAnimation!
    var layer_d:CALayer!
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.chushihua()
    }
    func chushihua(){
        zj_kd = 20
        gradientlayer1 = CAGradientLayer(layer: layer)
        gradientlayer2 = CAGradientLayer(layer: layer)
        
        //渐变范围
        gradientlayer1.startPoint = CGPoint(x: 1, y: 0.15)
        gradientlayer1.endPoint = CGPoint(x: 1, y: 0.4)
        gradientlayer2.startPoint = CGPoint(x: 1, y: 0.2)
        gradientlayer2.endPoint = CGPoint(x: 1, y: 0.4)
        
        array1 = [UIColor.yellow.cgColor,UIColor.green.cgColor]
        array2 = [UIColor.yellow.cgColor,UIColor.red.cgColor]
        
        //渐变开始
        gradientlayer1.colors = array1
        gradientlayer2.colors = array2
        
        //渐变层合并一个层，方便控制
        layer_d = CALayer(layer: layer)
        layer_d.insertSublayer(gradientlayer1, at: 0)
        layer_d.insertSublayer(gradientlayer2, at: 0)
        
        //设置蒙版
        shapelayer = CAShapeLayer(layer: layer)
        shapelayer.fillColor = UIColor.clear.cgColor
        shapelayer.strokeColor = UIColor.red.cgColor
        shapelayer.backgroundColor = UIColor.clear.cgColor
        shapelayer.lineJoin = kCALineJoinRound
        shapelayer.lineCap = kCALineCapRound
        shapelayer.frame = CGRect(x: 0, y: 0, width: 0, height: 0)
        
    }
    
    func setcanshu(rect:CGRect){
        bj = (rect.size.height>rect.size.width ? rect.size.width/2 : rect.size.height/2) - zj_kd/2
        point = CGPoint(x: rect.size.width/2, y: rect.size.height/2)
        rect1 = CGRect(x: rect.size.width/2 - bj - zj_kd/2, y: rect.size.height/2 - bj-zj_kd/2, width: bj+zj_kd/2, height: 2*bj+zj_kd)
        rect2 = CGRect(x: rect.size.width/2, y: rect.size.height/2-bj-zj_kd/2, width: bj+zj_kd/2, height: 2*bj+zj_kd)
        
        gradientlayer1.frame = rect1
        gradientlayer2.frame = rect2
        
        layer_d.frame = rect
        
        if shapelayer.frame.origin.x == 0 || shapelayer.frame.origin.y == 0 || shapelayer.frame.size.width == 0 || shapelayer.frame.size.height == 0{
            shapelayer.frame = rect
            shapelayer.transform = CATransform3DMakeRotation(CGFloat.pi/4, 0, 0, 1)
        }
        shapelayer.lineWidth = zj_kd
        apath = UIBezierPath()
        apath.addArc(withCenter: point, radius: bj-2, startAngle: CGFloat(M_PI)/2, endAngle: CGFloat.pi*2, clockwise: true)
        shapelayer.path = apath.cgPath
        if(z>z1){
            z1 = 0.001+z/90>0.999 ? 1 : 0.001+z/90
        }else{
         z1 = 0.001+z/90<0 ? 0.001 : 0.001+z/90
        }
        shapelayer.strokeEnd = z1
        layer_d.mask = shapelayer
        self.layer.addSublayer(layer_d)
    }
    override func draw(_ rect: CGRect) {
        setcanshu(rect: rect)
        //draw_yy()
    }
    //设置阴影
    func draw_yy(){
        self.layer.shadowOffset = CGSize(width: 5, height: 5)
        self.layer.shadowRadius = 5
        self.layer.shadowColor = UIColor.black.cgColor
        self.layer.shadowOpacity = 1
    }
    
    func setZj_kd(zj_kd:CGFloat){
        self.zj_kd = zj_kd
        self.setNeedsDisplay()
    }
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
