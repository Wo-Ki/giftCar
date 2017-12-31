//
//  socketCrtl.swift
//  iosGiftCar
//
//  Created by  WangKai on 2017/12/31.
//  Copyright © 2017年  WangKai. All rights reserved.
//

import UIKit

class socketCrtl: NSObject,GCDAsyncSocketDelegate {
    var clientSocket:GCDAsyncSocket!
    var serverIP = ""
    var serverPort = 0
    init(serverIP:String, serverPort:Int) {
        super.init()
        self.clientSocket = GCDAsyncSocket()
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.clientSocket.delegate = self
        self.clientSocket.delegateQueue = DispatchQueue.global()
        
    }
    // 连接
    func connect()->Bool{
        do{
            try clientSocket.connect(toHost: serverIP, onPort: UInt16(serverPort))
        }catch{
            print("try connect error:\(error)")
            return false
        }
        return true
    }
    func socketDidDisconnect(_ sock: GCDAsyncSocket!, withError err: Error!) {
        print("Disconnect!!!")
        
    }
}
