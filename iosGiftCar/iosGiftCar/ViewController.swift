//
//  ViewController.swift
//  iosGiftCar
//
//  Created by  WangKai on 2017/12/31.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit
import WebKit

class ViewController: UIViewController,GCDAsyncSocketDelegate  {
    @IBOutlet weak var ipTextFiled: UITextField!
    
    @IBOutlet weak var portTextField: UITextField!
    @IBOutlet weak var upDown: UISlider!
    @IBOutlet weak var leftRight: UISlider!
    @IBOutlet weak var connBtn: UIButton!
    @IBOutlet weak var stopBtn: UIButton!
    @IBOutlet weak var disConnBtn: UIButton!
    @IBOutlet weak var connActivity: UIActivityIndicatorView!
    @IBOutlet weak var motionWebView: WKWebView!
    @IBOutlet weak var motionSliderH: UISlider!
    @IBOutlet weak var motionSliderV: UISlider!
    @IBOutlet weak var motionResetBtn: UIButton!
    @IBOutlet weak var motionStopLoadBtn: UIButton!
    
    @IBOutlet weak var robotArmUpSlider: UISlider!
    @IBOutlet weak var robotArmDownSlider: UISlider!
    @IBOutlet weak var robotArmLeftSlider: UISlider!
    @IBOutlet weak var robotArmRightSlider: UISlider!
    @IBOutlet weak var robotArmCleanBtn: UIButton!
    @IBOutlet weak var speedSelectSegment: UISegmentedControl!
    
    
    var clientSocket:GCDAsyncSocket!
    
    override func viewDidLoad() {
       
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        leftRight.sizeToFit()
        upDown.transform = CGAffineTransform(rotationAngle: 1.571)
        
        upDown.isEnabled = false
        leftRight.isEnabled = false
        stopBtn.isEnabled = false
        disConnBtn.isEnabled = false
        connActivity.isHidden = true
        
        motionSliderH.isEnabled = false
        motionSliderV.isEnabled = false
        motionResetBtn.isEnabled = false
        
        robotArmUpSlider.isEnabled = false
        robotArmDownSlider.isEnabled = false
        robotArmLeftSlider.isEnabled = false
        robotArmRightSlider.isEnabled = false
        robotArmCleanBtn.isEnabled = false
        
        speedSelectSegment.selectedSegmentIndex = 0
        speedSelectSegment.addTarget(self, action: #selector(ViewController.speedSelectFunc(_:)), for: .valueChanged)
        
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    @objc func speedSelectFunc(_ segmented:UISegmentedControl){
        if(segmented.selectedSegmentIndex == 0){
            print("选择低速")
            upDown.maximumValue = 30
            upDown.minimumValue = -30
        }
        else if(segmented.selectedSegmentIndex == 1){
            print("选择中速")
            upDown.maximumValue = 60
            upDown.minimumValue = -60
        }
        else if(segmented.selectedSegmentIndex == 2){
            print("选择高速")
            upDown.maximumValue = 100
            upDown.minimumValue = -100
        }
    }
    // 摄像头网页
    @IBAction func motionFlashBtnDidTouched(_ sender: UIButton) {
        let motionUrl = URL(string: "http://192.168.100.2:9090/video/")
        let motionRequest = URLRequest(url: motionUrl!)
        motionWebView.load(motionRequest)
        
    }
    @IBAction func motionStopLoadBtnTouched(_ sender: UIButton) {
        motionWebView.stopLoading()
    }

    
    @IBAction func disConnDidTouched(_ sender: UIButton) {
        clientSocket.disconnect()
    }
    @IBAction func connDidTouched(_ sender: UIButton) {
        if ipTextFiled.text == nil || portTextField.text == nil{
            alertFunc(title: "错误", message: "IP和Port不能为空！")
        }else{
            let ip = self.ipTextFiled.text!
            let port = self.portTextField.text!
            clientSocket = GCDAsyncSocket()
            clientSocket.delegate = self
            clientSocket.delegateQueue = DispatchQueue.global()
            connActivity.isHidden = false
            connActivity.startAnimating()
            do{
                try clientSocket.connect(toHost: ip, onPort: UInt16(port)!)
            }catch{
                print("try connect error:\(error)")
                alertFunc(title: "连接错误", message: "ip或port有误")
            }
        }
    }
    func socketDidDisconnect(_ sock: GCDAsyncSocket!, withError err: Error!) {
        print("Disconnected!!!")
        stopBtn.isEnabled = false
        upDown.isEnabled = false
        leftRight.isEnabled = false
        connBtn.isEnabled = true
        disConnBtn.isEnabled = false
        connActivity.stopAnimating()
        connActivity.isHidden = true
        motionSliderH.isEnabled = false
        motionSliderV.isEnabled = false
        motionResetBtn.isEnabled = false
        
        robotArmUpSlider.isEnabled = false
        robotArmDownSlider.isEnabled = false
        robotArmLeftSlider.isEnabled = false
        robotArmRightSlider.isEnabled = false
        robotArmCleanBtn.isEnabled = false
        alertFunc(title: "提示", message: "已经断开连接")
    }
    func socket(_ sock: GCDAsyncSocket!, didRead data: Data!, withTag tag: Int) {
        let readData = String.init(data: data, encoding: String.Encoding.utf8)
        print("---Data Recv----")
        print(readData!)
        
        DispatchQueue.main.async {
            
        }
        //每次读取数据后，都要调用一次监听数据的方法
        clientSocket.readData(withTimeout: -1, tag: 0)
    }
    func socket(_ sock: GCDAsyncSocket!, didConnectToHost host: String!, port: UInt16) {
        print("Connect successfully")
        connActivity.stopAnimating()
        connActivity.isHidden = true
        upDown.isEnabled = true
        leftRight.isEnabled = true
        stopBtn.isEnabled = true
        disConnBtn.isEnabled = true
        connBtn.isEnabled = false
        
        motionSliderH.isEnabled = true
        motionSliderV.isEnabled = true
        motionResetBtn.isEnabled = true
        
        robotArmUpSlider.isEnabled = true
        robotArmDownSlider.isEnabled = true
        robotArmLeftSlider.isEnabled = true
        robotArmRightSlider.isEnabled = true
        robotArmCleanBtn.isEnabled = true
        clientSocket.readData(withTimeout: -1, tag: 0)
    }
    var lastLeftRight = 0
    @IBAction func leftRightChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(value - lastLeftRight) >= 5 || lastLeftRight == 0{
            lastLeftRight = value
            let str = "{\"LR\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
        
    }
    @IBAction func leftRightChanged(_ sender: UISlider) {
        leftRight.setValue(0, animated: true)
        let str = "{\"LR\":0},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        
    }
    var lastUpDown = 0
    @IBAction func upDownChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastUpDown - value) >= 5 || lastUpDown == 0{
            lastUpDown = value
            let str = "{\"UD\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
        
    }
    @IBAction func upDownChanged(_ sender: UISlider) {
        upDown.setValue(0, animated: true)
        let str = "{\"UD\":0},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        
    }
    @IBAction func stopBtnTouched(_ sender: UIButton) {
        var str = "{\"LR\":0},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        str = "{\"UD\":0},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    // 摄像头云台控制
    var lastMotionH = 0
    @IBAction func motionSliderHChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastMotionH - value) >= 5 || lastMotionH == 0{
            lastMotionH = value
            let str = "{\"YH\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
        
    }
    var lastMotionV = 0
    @IBAction func motionSliderVCHanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastMotionV - value) >= 5 || lastMotionV == 0{
            lastMotionV = value
            let str = "{\"YV\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
    }
    
    @IBAction func motionResetBtnTouched(_ sender: UIButton) {
        motionSliderV.setValue(0, animated: true)
        motionSliderH.setValue(0, animated: true)
        let str = "{\"YH\":0},{\"YV\":0}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        lastMotionH = 0
        lastMotionV = 0
    }
    
    // 机械臂控制函数
    var lastArmUp = 0
    @IBAction func robotArmUpSliderChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastArmUp - value) >= 2 || lastArmUp == 0{
            lastArmUp = value
            let str = "{\"AU\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
    }
    var lastArmDown = 0
    @IBAction func robotArmDownSliderChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastArmDown - value) >= 2 || lastArmDown == 0{
            lastArmDown = value
            let str = "{\"AD\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
    }
    var lastArmLeft = 0
    @IBAction func robotArmLeftSliderChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastArmLeft - value) >= 2 || lastArmLeft == 0{
            lastArmLeft = value
            let str = "{\"AL\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
    }
    var lastArmRight = 0
    @IBAction func robotArmRightSliderChanging(_ sender: UISlider) {
        let value = Int(sender.value)
        if abs(lastArmRight - value) >= 2 || lastArmRight == 0{
            lastArmRight = value
            let str = "{\"AR\":"+String(value)+"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
      
    }
    @IBAction func robotArmCleanBtnTouched(_ sender: UIButton) {
        let str = "{\"AC\":1},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    
    func alertFunc(title:String, message:String) {
        let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let alertAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(alertAction)
        self.present(alertController, animated: true, completion: nil)
    }
}

