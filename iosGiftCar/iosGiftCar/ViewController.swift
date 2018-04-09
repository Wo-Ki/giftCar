//
//  ViewController.swift
//  iosGiftCar
//
//  Created by  WangKai on 2017/12/31.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit
import WebKit

class ViewController: UIViewController,GCDAsyncSocketDelegate,UIScrollViewDelegate  {
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
    @IBOutlet weak var viewModeSelectSegment: UISegmentedControl!
    @IBOutlet weak var scrollMode: UIScrollView!
    
    
    var clientSocket:GCDAsyncSocket!
    var beatTimer:Timer!
    
    override func viewDidLoad() {
       
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        leftRight.sizeToFit()
        upDown.transform = CGAffineTransform(rotationAngle: 1.571)
        motionSliderV.transform = CGAffineTransform(rotationAngle: 1.571)
        self.scrollMode.frame = CGRect(x: 0, y: 50, width: self.view.frame.size.width, height: self.view.frame.size.height/2)
        self.scrollMode.contentSize = CGSize(width: 3*self.view.frame.size.width, height: self.view.frame.size.height/2)
        self.scrollMode.isPagingEnabled=true
        self.scrollMode.showsVerticalScrollIndicator=false
        self.scrollMode.showsHorizontalScrollIndicator=false
        self.scrollMode.delegate = self
        
        self.motionWebView
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
    // scorll
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        let pageWidth=self.scrollMode.frame.size.width
        if scrollView.contentOffset.x < pageWidth/6{
            viewModeSelectSegment.selectedSegmentIndex=0
        }
        if scrollView.contentOffset.x > pageWidth*3/6{
            viewModeSelectSegment.selectedSegmentIndex=1
        }
        if scrollView.contentOffset.x > pageWidth*5/6{
            viewModeSelectSegment.selectedSegmentIndex=2
        }
    }
    @IBAction func viewModeSelectChanged(_ sender: UISegmentedControl) {
        if sender.selectedSegmentIndex == 0{
            UIView.animate(withDuration: 0.5, animations: {
                self.scrollMode.contentOffset=CGPoint(x: 0, y: 0)
            })
        }else if sender.selectedSegmentIndex == 1{
            UIView.animate(withDuration: 0.5, animations: {
                self.scrollMode.contentOffset=CGPoint(x: self.view.frame.size.width, y: 0)
                
            })
        }else if sender.selectedSegmentIndex == 2{
            UIView.animate(withDuration: 0.5, animations: {
                self.scrollMode.contentOffset=CGPoint(x: self.view.frame.size.width*2, y: 0)
                
            })
        }
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
        DispatchQueue.main.async {
            self.stopBtn.isEnabled = false
            self.upDown.isEnabled = false
            self.leftRight.isEnabled = false
            self.connBtn.isEnabled = true
            self.disConnBtn.isEnabled = false
            self.connActivity.stopAnimating()
            self.connActivity.isHidden = true
            self.motionSliderH.isEnabled = false
            self.motionSliderV.isEnabled = false
            self.motionResetBtn.isEnabled = false
            
            self.robotArmUpSlider.isEnabled = false
            self.robotArmDownSlider.isEnabled = false
            self.robotArmLeftSlider.isEnabled = false
            self.robotArmRightSlider.isEnabled = false
            self.robotArmCleanBtn.isEnabled = false
            self.beatTimer.invalidate()
            self.alertFunc(title: "提示", message: "已经断开连接")
        }
        
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
        DispatchQueue.main.async {
            print("Connect successfully")
            self.connActivity.stopAnimating()
            self.connActivity.isHidden = true
            self.upDown.isEnabled = true
            self.leftRight.isEnabled = true
            self.stopBtn.isEnabled = true
            self.disConnBtn.isEnabled = true
            self.connBtn.isEnabled = false
            
            self.motionSliderH.isEnabled = true
            self.motionSliderV.isEnabled = true
            self.motionResetBtn.isEnabled = true
            
            self.robotArmUpSlider.isEnabled = true
            self.robotArmDownSlider.isEnabled = true
            self.robotArmLeftSlider.isEnabled = true
            self.robotArmRightSlider.isEnabled = true
            self.robotArmCleanBtn.isEnabled = true
            
             self.beatTimer = Timer.scheduledTimer(timeInterval: 3, target: self, selector: #selector(ViewController.beatFunc), userInfo: nil, repeats: true)
            
            self.clientSocket.readData(withTimeout: -1, tag: 0)
        }
        
    }
    @objc func beatFunc(){
        if(clientSocket.isConnected){
            let str = "{\"M\":\"b\"},"
            clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        }
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
        let str = "{\"M\":\"stop\"},"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
//        str = "{\"UD\":0},"
//        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
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

