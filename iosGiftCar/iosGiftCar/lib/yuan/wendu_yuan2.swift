//
//  wendu_yuan2.swift
//  BlueTest2
//
//  Created by  WangKai on 2017/4/3.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class wendu_yuan2: UIView {
    var kd:CGFloat = 0
    var z:CGFloat = 0{
        didSet{
            DispatchQueue.main.async {
                self.setNeedsDisplay()
            }
        }
    }
    var jishuText:String = ""
    
    var sc:yuan2_sc!
    var zj:yuan2_zj!
    var led_jushu:led_jishu!
    
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.setchushihua()
    }
    func setchushihua(){
        kd = 20
        sc = yuan2_sc()
        sc.backgroundColor = UIColor.clear
        zj = yuan2_zj()
        zj.backgroundColor = UIColor.clear
        led_jushu = led_jishu()
        led_jushu.backgroundColor = UIColor.clear
        self.insertSubview(zj, at: 1)
        self.insertSubview(sc, at: 2)
        
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func draw(_ rect: CGRect) {
        self.draw_scdcdt(rect:rect)
        self.draw_jishu(rect:rect)
    }
    func draw_jishu(rect:CGRect){
        if rect.size.width > rect.size.height{
            led_jushu.frame = CGRect(x: 0, y: 0, width: 2*rect.size.height/3, height: rect.size.height/3)
        }else{
            led_jushu.frame = CGRect(x: 0, y: 0, width: 2*rect.size.width/3, height: rect.size.width/3)
        }
        
        led_jushu.layer.position = CGPoint(x: rect.size.width/2, y: rect.size.height/2)
        led_jushu.z = z
        led_jushu.jishuText = jishuText
        self.insertSubview(led_jushu, at: 0)
    }
    
    //添加上层，中间层。底层
    func draw_scdcdt(rect:CGRect){
        sc.frame = rect
        zj.frame = rect
        sc.sc_kd = kd+5
        zj.z = z
        zj.zj_kd = kd
    
    }
    func setKd(kd:CGFloat){
        self.kd = kd>20 ? 20 : kd
        self.setNeedsDisplay()
    }
    func setZ(z:CGFloat){
        self.z = z
        self.setNeedsDisplay()
    }
   
}
