//
//  Car3DModeView.swift
//  iosGiftCar
//
//  Created by  WangKai on 2018/4/28.
//  Copyright © 2018年  WangKai. All rights reserved.
//

import UIKit
import QuartzCore
import SceneKit

class Car3DModeView: UIView {

    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    */
    var carView:UIView! = nil
    var gyroView:UIView! = nil
    
    var carShip:SCNNode! = nil
    
    var gyroXShip:SCNNode! = nil
    var gyroYShip:SCNNode! = nil
    var gyroZShip:SCNNode! = nil
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.carView.frame = CGRect(x: 0, y: 0, width: frame.size.width/2, height: frame.size.height)
        self.gyroView.frame = CGRect(x: frame.size.width/2, y: 0, width: frame.size.width/2, height: frame.size.height)
        self.carView.backgroundColor = UIColor.red
        self.gyroView.backgroundColor = UIColor.brown
        self.addSubview(carView)
        self.addSubview(gyroView)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    override func draw(_ rect: CGRect) {
        let sceneCar = SCNScene(named: "art.scnassets/car_model.scn")!
  
        carShip = sceneCar.rootNode.childNode(withName: "ship", recursively: true)!
        
        let scnCarView = self.carView as! SCNView
        scnCarView.allowsCameraControl = true
        scnCarView.backgroundColor = UIColor.black
        // add a tap gesture recognizer
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(handleTap(_:)))
        scnCarView.addGestureRecognizer(tapGesture)
        
        let sceneGyro = SCNScene(named: "art.scnassets/gyro_model.scn")!
        gyroXShip = sceneGyro.rootNode.childNode(withName: "x_ship", recursively: true)!
        gyroYShip = sceneGyro.rootNode.childNode(withName: "y_ship", recursively: true)!
        gyroZShip = sceneGyro.rootNode.childNode(withName: "z_ship", recursively: true)!
        let scnGyroView = self.gyroView as! SCNView
        scnGyroView.allowsCameraControl = true
        scnGyroView.backgroundColor = UIColor.black
        scnGyroView.addGestureRecognizer(tapGesture)
    
    }
 
    func carModeUpdate(xValue:Float, yValue:Float){ // 0~1
        var x:CGFloat = 0
        var z:CGFloat = 0
        if xValue < 0{
            x = 0
        }else if xValue > 1{
            x = 1
        }else{
            x = CGFloat(xValue)
        }
        if yValue < 0{
            z = 0
        }else if yValue > 1{
            z = 1
        }else{
            z = CGFloat(yValue)
        }
        
        x = degreesToRadians(degress: x/1.0 * 360)
        z = degreesToRadians(degress: z/1.0 * 360)
        carShip.runAction(SCNAction.rotateTo(x: x, y: 0, z: z, duration: 0.1))
    }
    func gyroModeUpdate(xValue:Float, yValue:Float, zValue:Float){ // 0~360
        var x:CGFloat = 0
        var y:CGFloat = 0
        var z:CGFloat = 0
        if xValue < 0{
            x = 0
        }else if xValue > 360{
            x = 360
        }else{
            x = CGFloat(xValue)
        }
        if yValue < 0{
            y = 0
        }else if yValue > 360{
            y = 360
        }else{
            y = CGFloat(yValue)
        }
        if zValue < 0{
            z = 0
        }else if zValue > 360{
            z = 360
        }else{
            z = CGFloat(zValue)
        }
        x = degreesToRadians(degress: x)
        y = degreesToRadians(degress: y)
        z = degreesToRadians(degress: z)
        gyroXShip.runAction(SCNAction.rotateTo(x: x, y: 0, z: 0, duration: 0.1))
        gyroYShip.runAction(SCNAction.rotateTo(x: 0, y: 0, z: z, duration: 0.1))
        gyroZShip.runAction(SCNAction.rotateTo(x: 0, y: y, z: 0, duration: 0.1))
    }
    
    @objc
    func handleTap(_ gestureRecognize: UIGestureRecognizer) {
        // retrieve the SCNView
        let scnView = self.carView as! SCNView
        
        // check what nodes are tapped
        let p = gestureRecognize.location(in: scnView)
        let hitResults = scnView.hitTest(p, options: [:])
        // check that we clicked on at least one object
        if hitResults.count > 0 {
            // retrieved the first clicked object
            let result = hitResults[0]
            
            // get its material
            let material = result.node.geometry!.firstMaterial!
            
            // highlight it
            SCNTransaction.begin()
            SCNTransaction.animationDuration = 0.5
            
            // on completion - unhighlight
            SCNTransaction.completionBlock = {
                SCNTransaction.begin()
                SCNTransaction.animationDuration = 0.5
                
                material.emission.contents = UIColor.black
                
                SCNTransaction.commit()
            }
            
            material.emission.contents = UIColor.red
            
            SCNTransaction.commit()
        }
    }
    func degreesToRadians(degress:CGFloat)->CGFloat{
        return CGFloat.pi*degress/180
    }
}
