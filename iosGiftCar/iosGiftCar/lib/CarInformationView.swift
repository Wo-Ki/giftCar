//
//  CarInformationView.swift
//  BlueTest2
//
//  Created by  WangKai on 2017/3/30.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class CarInformationView: UIView {

    var arrowSpeedLayer:CAShapeLayer! = nil
    var speedLast:Float = 0
    var speedNow:Float = 0
    var speedLabel:UILabel! = nil
    var levelCircle:UIView! = nil
    var leftImage:UIImageView! = nil
    var rightImage:UIImageView! = nil
    var backImage:UIImageView! = nil
    var  hum:wendu_yuan2!
    var tem:wendu_yuan2!
    var gyroscopeX:CAShapeLayer! = nil
    var gyroscopeY:CAShapeLayer! = nil
    var gyroscopeZ:CAShapeLayer! = nil
    var commpassLayer:CAShapeLayer! = nil
    
    var sr04Layer:CAShapeLayer! = nil
    var sr04View:[UIView] = []
    
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.speedLast = 0
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
        drawSpeed()
        drawGradienter()
        drawLeftRightBack()
        drawHum()
        drawTem()
        drawGyroscope()
        drawCompass()
        drawSr04()
        
    }
    func degreesToRadians(degress:CGFloat)->CGFloat{
        return CGFloat.pi*degress/180
    }
    func UIColorFromRGB(rgbValue: UInt) -> UIColor {
        return UIColor(
            red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
            green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
            blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
            alpha: CGFloat(1.0)
        )
    }
    func drawSpeed(){
      
        
        let path = UIBezierPath(arcCenter: CGPoint(x:100,y:100), radius: CGFloat((80.0-4.0)/2.0), startAngle: degreesToRadians(degress: 0), endAngle: degreesToRadians(degress: 180), clockwise: false)
        let trackLayer = CAShapeLayer(layer: self.layer)
        trackLayer.frame = CGRect(x: 0, y: 0, width: 200, height: 200)
        self.layer.addSublayer(trackLayer)
        trackLayer.fillColor = UIColor.clear.cgColor
        trackLayer.strokeColor = UIColor.blue.cgColor
        trackLayer.opacity = 0.7
        trackLayer.lineCap = kCALineCapRound
        trackLayer.lineWidth = 4
        trackLayer.path = path.cgPath
       // trackLayer.strokeEnd = 0
    
        let gradientLayer = CALayer(layer: self.layer)
        let gradientLayer1 = CAGradientLayer(layer: self.layer)
        gradientLayer1.frame = CGRect(x: 60, y: 60, width: 80, height: 40)
        gradientLayer1.colors = [UIColor.green.cgColor,UIColor.yellow.cgColor,UIColor.orange.cgColor,UIColor.red.cgColor]
        // gradientLayer1.locations = [0,0.2,0.4,0.9,1]
        gradientLayer1.startPoint = CGPoint(x: 0, y: 0)
        gradientLayer1.endPoint = CGPoint(x: 1, y: 0)
        gradientLayer.addSublayer(gradientLayer1)

        gradientLayer.mask = trackLayer
        self.layer.addSublayer(gradientLayer)
        
        arrowSpeedLayer = CAShapeLayer()
        arrowSpeedLayer.frame = CGRect(x: 100, y: 100, width: 0, height: 0)
        let linePath = UIBezierPath()
        linePath.move(to: CGPoint(x: 0, y: 0))
        linePath.addLine(to: CGPoint(x: -40, y: 0))
        arrowSpeedLayer.path = linePath.cgPath
        
        arrowSpeedLayer.fillColor = nil
        arrowSpeedLayer.strokeColor = UIColor.red.cgColor
        arrowSpeedLayer.lineWidth = 3
        arrowSpeedLayer.lineCap = kCALineCapRound
        self.layer.addSublayer(arrowSpeedLayer)
        
        speedLabel = UILabel(frame: CGRect(x: 60, y: 105, width: 80, height: 27))
        speedLabel.center = CGPoint(x: 100, y: 122)
        let font = UIFont(name: "Zapfino", size: 14)
        speedLabel.textAlignment = .center
        speedLabel.font = font
        speedLabel.adjustsFontSizeToFitWidth = true
        speedLabel.text =  "\(String.init(format: "%.2f", (speedNow/100.0*8.17)))cm/s"
        self.addSubview(speedLabel)
        
    }
    func updateSpeed(speed:Float){  //speed 0-100
        
        if speed != speedLast{
            speedNow = speed
            let angle = CGFloat(speed)*CGFloat(1.8)
            let angle2 = CGFloat(speed - speedLast)*CGFloat(1.8)
            
            //calculate the time of the anmitaion
            let ti = fabs(Double(speed - speedLast))*0.01
            print(ti)
            //rotate the arrow
            arrowSpeedLayer.transform = CATransform3DRotate(arrowSpeedLayer.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(speedLast)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.arrowSpeedLayer.add(animation, forKey: "rotateAnimation")
            speedLabel.text = "\(String.init(format: "%.2f", (speed/100.0*8.17)))cm/s"
            speedLast = speed
        }
    }
    func drawLeftRightBack(){
         leftImage = UIImageView(image: #imageLiteral(resourceName: "LeftOff.png"))
        leftImage.frame = CGRect(x: 45, y: 50, width: 25, height: 25)
        self.addSubview(leftImage)
        
         rightImage = UIImageView(image: #imageLiteral(resourceName: "RightOff.png"))
        rightImage.frame = CGRect(x: 130, y: 50, width: 25, height: 25 )
        self.addSubview(rightImage)
        
        backImage = UIImageView(image: #imageLiteral(resourceName: "BackOff.png"))
        backImage.frame = CGRect(x: 150, y: 80, width: 25, height: 25)
        self.addSubview(backImage)
    }
    func updataLeftRightBackLight(direction:Int){
        switch direction {
        case 10:
            leftImage.image = #imageLiteral(resourceName: "LeftOff.png")
        case 11:
            leftImage.image =  #imageLiteral(resourceName: "LeftOn.png")
        case 20:
            rightImage.image = #imageLiteral(resourceName: "RightOff.png")
        case 21:
            rightImage.image = #imageLiteral(resourceName: "RightOn.png")
        case 30:
            backImage.image = #imageLiteral(resourceName: "BackOff.png")
        case 31:
            backImage.image = #imageLiteral(resourceName: "BackOn.png")
        default:
            leftImage.image = #imageLiteral(resourceName: "LeftOff.png")
            rightImage.image = #imageLiteral(resourceName: "RightOff.png")
            backImage.image = #imageLiteral(resourceName: "BackOff.png")
        }
    }
    func drawGradienter(){
        let context = CGContextObject(context: UIGraphicsGetCurrentContext()!)
        context.drawStrokeBlock { (context) in
            context.strokeColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.lineWidth = 3
            context.addEllopseInRect(rect: CGRect(x: 850, y: 50, width: 100, height: 100))
            context.lineWidth = 1
            context.moveToStartPoint(point: CGPoint(x: 900, y: 100))
            context.addLineToPoint(point: CGPoint(x: 900, y: 110))
            context.addLineToPoint(point: CGPoint(x: 900, y: 90))
            context.moveToStartPoint(point: CGPoint(x: 900, y: 100))
            context.addLineToPoint(point: CGPoint(x: 910, y: 100))
            context.addLineToPoint(point: CGPoint(x: 890, y: 100))
        }
        levelCircle = UIView(frame: CGRect(x: 900, y: 100, width: 10, height: 10))
        levelCircle.center = CGPoint(x: 900, y: 100)
        levelCircle.backgroundColor = UIColor.red
        levelCircle.layer.cornerRadius = 5
        levelCircle.layer.shadowColor = UIColor.black.cgColor
        levelCircle.layer.shadowOffset = CGSize(width: 3, height: 3)
        levelCircle.layer.shadowOpacity = 0.6
        self.addSubview(levelCircle)
    }
    
    func updateLevelCircle(mpudata:[String:Int]){
        let x = CGFloat(mpudata["AX"]!) + 900
        let y = CGFloat(mpudata["AY"]!) + 100
        UIView.animate(withDuration: 0.2, delay: 0, options: .curveEaseInOut, animations: { 
            self.levelCircle.center = CGPoint(x: x, y: y)
        }, completion: nil)
    }
    
    func drawHum(){
         hum = wendu_yuan2(frame: CGRect(x: 150, y: 200, width: 100, height: 100))
        hum.kd = 10
        hum.backgroundColor = UIColor.clear
        hum.jishuText = "%"
        self.addSubview(hum)
        
        let context = CGContextObject(context: UIGraphicsGetCurrentContext()!)
        context.drawString(string: "Tem", point: CGPoint.init(x: 70, y: 290), attribute: [:])
        context.drawString(string: "Hum", point: CGPoint.init(x: 190, y: 290), attribute: [:])
    }
    func drawTem(){
         tem = wendu_yuan2(frame: CGRect(x: 30, y: 200, width: 100, height: 100))
        tem.kd = 10
        tem.jishuText =  "℃"
        tem.backgroundColor = UIColor.clear
        self.addSubview(tem)
        
    }
  
    func updateHum(hum:Float){
        self.hum.z = CGFloat(hum)
     
    }
    func updateTem(tem:Float){
        self.tem.z = CGFloat(tem)
    }
    
    func drawGyroscope(){
        let context = CGContextObject(context: UIGraphicsGetCurrentContext()!)
        context.drawStrokeBlock { (context) in
            context.strokeColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.lineWidth = 1
            context.addEllopseInRect(rect: CGRect(x: 700, y:200, width: 80, height: 80))
        
            context.strokeColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.lineWidth = 1
            context.addEllopseInRect(rect: CGRect(x: 800, y:200, width: 80, height: 80))
            
            context.strokeColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.lineWidth = 1
            context.addEllopseInRect(rect: CGRect(x: 900, y:200, width: 80, height: 80))
            
        }
        context.drawFillBlock { (context) in
            context.fillColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.addEllopseInRect(rect: CGRect(x: 738 , y:238, width: 4, height: 4))
            context.fillColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.addEllopseInRect(rect: CGRect(x: 838 , y:238, width: 4, height: 4))
            context.fillColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.addEllopseInRect(rect: CGRect(x: 938 , y:238, width: 4, height: 4))
        }

        context.drawString(string: "X", point: CGPoint.init(x: 738, y: 290), attribute: [:])
       context.drawString(string: "Y", point: CGPoint.init(x: 838, y: 290), attribute: [:])
        context.drawString(string: "Z", point: CGPoint.init(x: 938, y: 290), attribute: [:])
        
        gyroscopeX = CAShapeLayer(layer: layer)
        gyroscopeDir(gyr: gyroscopeX, rect: CGRect(x: 738, y: 200, width: 4, height: 80))
        gyroscopeY = CAShapeLayer(layer: layer)
        gyroscopeDir(gyr: gyroscopeY, rect: CGRect(x: 838, y: 200, width: 4, height: 80))
        gyroscopeZ = CAShapeLayer(layer: layer)
        gyroscopeDir(gyr: gyroscopeZ, rect: CGRect(x: 938, y: 200, width: 4, height: 80))

    }
    func gyroscopeDir(gyr:CAShapeLayer,rect:CGRect){
        gyr.frame = rect
        let linePath = UIBezierPath()
        linePath.move(to: CGPoint(x: 2, y: 10))
        linePath.addLine(to: CGPoint(x: 2, y: 70))
         linePath.move(to: CGPoint(x: 2, y: 10))
        linePath.addLine(to: CGPoint(x: 0, y: 15))
        linePath.move(to: CGPoint(x: 2, y: 10))
        linePath.addLine(to: CGPoint(x: 4, y: 15))
        gyr.path = linePath.cgPath
        gyr.lineWidth = 2
        gyr.strokeColor = UIColor.black.cgColor
        gyr.lineJoin = kCALineJoinRound
        gyr.lineCap = kCALineJoinRound
        self.layer.addSublayer(gyr)
    }
    func updateGyroscope(data:[String:Int]){
        updateGyroscopeX(x: CGFloat(data["GX"]!))
        updateGyroscopeY(y: CGFloat(data["GY"]!))
        updateGyroscopeZ(z: CGFloat(data["GZ"]!))
    }
    var lastX:CGFloat = 0
    func updateGyroscopeX(x:CGFloat){
        if x != lastX{
            let angle = CGFloat(x)*CGFloat(1.8)
            let angle2 = CGFloat(x - lastX)*CGFloat(1.8)
            let ti = fabs(Double(x - lastX))*0.01
            gyroscopeX.transform = CATransform3DRotate(gyroscopeX.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(lastX)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.gyroscopeX.add(animation, forKey: "rotateAnimation")
            lastX = x
        }
    }
    var lastY:CGFloat = 0
    func updateGyroscopeY(y:CGFloat){
        if y != lastY{
            let angle = CGFloat(y)*CGFloat(1.8)
            let angle2 = CGFloat(y - lastY)*CGFloat(1.8)
            let ti = fabs(Double(y - lastY))*0.01
            gyroscopeY.transform = CATransform3DRotate(gyroscopeY.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(lastY)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.gyroscopeY.add(animation, forKey: "rotateAnimation")
            lastY = y
        }
    }
    var lastZ:CGFloat = 0
    func updateGyroscopeZ(z:CGFloat){
        if z != lastZ{
            let angle = CGFloat(z)*CGFloat(1.8)
            let angle2 = CGFloat(z - lastZ)*CGFloat(1.8)
            let ti = fabs(Double(z - lastZ))*0.01
            gyroscopeZ.transform = CATransform3DRotate(gyroscopeZ.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(lastZ)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.gyroscopeZ.add(animation, forKey: "rotateAnimation")
            lastZ = z
        }
    }
    
    func drawCompass(){
        let context = CGContextObject(context: UIGraphicsGetCurrentContext()!)
        context.drawStrokeBlock { (context) in
            context.strokeColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.lineWidth = 3
            context.addEllopseInRect(rect: CGRect(x: 700, y: 50, width: 100, height: 100))
            context.lineWidth = 1
            context.moveToStartPoint(point: CGPoint(x: 700, y: 100))
            context.addLineToPoint(point: CGPoint(x: 710, y: 100))
            context.moveToStartPoint(point: CGPoint(x: 800, y: 100))
            context.addLineToPoint(point: CGPoint(x: 790, y: 100))
            context.moveToStartPoint(point: CGPoint(x: 750, y: 50))
            context.addLineToPoint(point: CGPoint(x: 750, y: 60))
            context.moveToStartPoint(point: CGPoint(x: 750, y: 150))
            context.addLineToPoint(point: CGPoint(x: 750, y: 140))
        }
        context.drawFillBlock { (context) in
            context.fillColor = RGBColor().colorWithRed(red: 0, green: 0, blue: 0, alpha: 1)
            context.addEllopseInRect(rect: CGRect(x: 748 , y:98, width: 4, height: 4))
        }
        commpassLayer = CAShapeLayer(layer: layer)
        gyroscopeDir(gyr: commpassLayer, rect: CGRect(x: 748, y: 60, width: 4, height: 80))
    }
    var lastValue:CGFloat = 0
    func updateCommpass(value:CGFloat){
        if value != lastValue{
            let angle = CGFloat(value)*CGFloat(1.8)
            let angle2 = CGFloat(value - lastValue)*CGFloat(1.8)
            let ti = fabs(Double(value - lastValue))*0.01
            commpassLayer.transform = CATransform3DRotate(commpassLayer.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(lastValue)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.commpassLayer.add(animation, forKey: "rotateAnimation")
            lastValue = value
        }

    }
    
  
    
    func drawSr04(){
        let context = UIGraphicsGetCurrentContext()
        context?.addArc(center: CGPoint.init(x: 470, y: 300), radius: 200, startAngle:degreesToRadians(degress: 0), endAngle: degreesToRadians(degress: 180), clockwise: true)
       
        context?.setFillColor(UIColor.black.cgColor)
        context?.setStrokeColor(UIColor.green.cgColor)
        context?.setLineWidth(1)
        context?.closePath()
        context?.setLineCap(CGLineCap.round)
        context?.drawPath(using: .fillStroke)
        
        let context2 = CGContextObject(context: UIGraphicsGetCurrentContext()!)
        context2.drawStrokeBlock { (context) in
            context.lineWidth = 1
            context.strokeColor = RGBColor().colorWithUIColor(color: UIColor(red: 0, green: 255, blue: 0, alpha: 0.5))
            context.lineCap = CGLineCap.square
            for i in 1...5{
                let x:CGFloat = 470 - cos(degreesToRadians(degress: CGFloat(30)*CGFloat(i)))*200
                let y:CGFloat = 300 - sin(degreesToRadians(degress: CGFloat(30)*CGFloat(i)))*200
                context.moveToStartPoint(point: CGPoint(x: 470, y: 300))
                context.addLineToPoint(point: CGPoint(x: x, y: y))
            }
 
        }
        for i in 1...3{
            context?.addArc(center: CGPoint.init(x: 470, y: 300), radius: CGFloat(i)*50, startAngle:degreesToRadians(degress: 0), endAngle: degreesToRadians(degress: 180), clockwise: true)
            context?.setStrokeColor(UIColor.init(red: 0, green: 255, blue: 0, alpha: 0.5).cgColor)
            context?.setLineCap(CGLineCap.square)
            context?.setLineWidth(1)
            context?.drawPath(using: CGPathDrawingMode.stroke)
        }

        sr04Layer = CAShapeLayer(layer: layer)
        sr04Layer.frame = CGRect(x: 470, y: 300, width: 0, height: 0)
        let path = UIBezierPath()
        path.move(to: CGPoint(x: 0, y: 0))
        path.addLine(to: CGPoint(x: -200, y: 0))
        
        sr04Layer.path = path.cgPath
        sr04Layer.fillColor = nil
        sr04Layer.strokeColor = UIColor.red.cgColor
        sr04Layer.lineWidth = 2
        sr04Layer.lineCap = kCALineCapRound
        self.layer.addSublayer(sr04Layer)
        
  
    }
    
    var lastDegress:CGFloat = 0
    func updateSr04(length:CGFloat,degress:CGFloat){
        
        if degress != lastDegress{
            let angle = CGFloat(degress)*CGFloat(1.8)
            let angle2 = CGFloat(degress - lastDegress)*CGFloat(1.8)
            let ti = fabs(Double(degress - lastDegress))*0.01
            sr04Layer.transform = CATransform3DRotate(sr04Layer.transform, degreesToRadians(degress: CGFloat(angle2)), 0, 0, 1)
            let animation = CABasicAnimation()
            animation.keyPath = "transform.rotation.z"
            animation.duration = ti
            animation.fromValue = degreesToRadians(degress: CGFloat(lastDegress)*1.8)
            animation.toValue = degreesToRadians(degress: angle)
            self.sr04Layer.add(animation, forKey: "rotateAnimation")
            lastDegress = degress
        }
        
        if length >= 0 && length <= 200{
            let point = CGPoint(x: -cos(degreesToRadians(degress: degress*1.8))*length+470, y: -sin(degreesToRadians(degress: degress*1.8))*length+300)
            
            let view = UIView(frame: CGRect(x: 0, y: 0, width: 5, height: 5))
            view.center = point
            view.backgroundColor = UIColor.red
            view.layer.cornerRadius = 2.5
            self.addSubview(view)
            sr04View.append(view)
        }
  
        if degress <= 3 || degress >= 98{
//            sr04Data = []
//            sr04Cotext?.clear(CGRect(x: 470-100, y: 300-100, width: 200, height: 100))
            for i in sr04View{
                i.removeFromSuperview()
            }
        }

    }

}
