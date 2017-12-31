//
//  ViewController.swift
//  iosGiftCar
//
//  Created by  WangKai on 2017/12/31.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class ViewController: UIViewController,GCDAsyncSocketDelegate {
    @IBOutlet weak var ipTextFiled: UITextField!
    
    @IBOutlet weak var portTextField: UITextField!
    @IBOutlet weak var upDown: UISlider!
    @IBOutlet weak var leftRight: UISlider!
    @IBOutlet weak var connBtn: UIButton!
    @IBOutlet weak var stopBtn: UIButton!
    @IBOutlet weak var disConnBtn: UIButton!
    @IBOutlet weak var connActivity: UIActivityIndicatorView!
    

    var clientSocket:GCDAsyncSocket!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        upDown.transform = CGAffineTransform(rotationAngle: 1.571)
    
        leftRight.sizeToFit()
       
        upDown.isEnabled = false
        leftRight.isEnabled = false
        stopBtn.isEnabled = false
        disConnBtn.isEnabled = false
        connActivity.isHidden = true
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
        clientSocket.readData(withTimeout: -1, tag: 0)
    }
    @IBAction func leftRightChanging(_ sender: UISlider) {
        let str = "{\"LR\":"+String(sender.value)+"}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    @IBAction func leftRightChanged(_ sender: UISlider) {
        leftRight.setValue(0, animated: true)
        let str = "{\"LR\":"+String(sender.value)+"}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    @IBAction func upDownChanging(_ sender: UISlider) {
        let str = "{\"UD\":"+String(sender.value)+"}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    @IBAction func upDownChanged(_ sender: UISlider) {
        upDown.setValue(0, animated: true)
        let str = "{\"UD\":"+String(sender.value)+"}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    @IBAction func stopBtnTouched(_ sender: UIButton) {
        var str = "{\"LR\":0}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
        str = "{\"UD\":0}"
        clientSocket.write(str.data(using: String.Encoding.utf8), withTimeout: -1, tag: 0)
    }
    
    
    func alertFunc(title:String, message:String) {
        let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let alertAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(alertAction)
        self.present(alertController, animated: true, completion: nil)
    }
}

