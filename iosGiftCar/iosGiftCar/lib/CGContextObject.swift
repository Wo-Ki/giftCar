//
//  CGContextObject.swift
//  使用CoreGraphic实现绘图操作
//
//  Created by  WangKai on 2016/11/29.
//  Copyright © 2016年  WangKai. All rights reserved.
//

import UIKit

//typealias size_t = Int


class CGContextObject: NSObject {
    
    typealias CGContextObjectDrawBlock_t = (_ contextObject:CGContextObject)->Void
    
    //操作句柄
    var context:CGContext! = nil
    //线头样式
    var lineCap:CGLineCap! = nil{
        didSet{
            if context != nil{
                context.setLineCap(lineCap)
                print("lineCap")
            }
        }
    }
    //线条宽度
    var lineWidth:CGFloat! = nil{

        didSet{
            if context != nil{
                context.setLineWidth(lineWidth)
                //print("lineWidth")
            }
        }
    }
    //线条颜色
    var strokeColor:RGBColor! = nil{

        didSet{
            if context != nil{
                context.setStrokeColor(red: strokeColor.red, green: strokeColor.green, blue: strokeColor.green, alpha: strokeColor.alpha)
                //print("setStrokeColor")
            }
        }
    }
    //填充颜色
    var fillColor:RGBColor! = nil {

        didSet{
            if context != nil{
                context.setFillColor(red: fillColor.red, green: fillColor.green, blue: fillColor.blue, alpha: fillColor.alpha)
                //print("fillColor")
            }
        }
    }
    
    init(context:CGContext) {
        self.context = context
    }
    /*****绘制操作流程******/
    
    //开始path
    func beginPath(){
        if (context != nil) {
            context.beginPath()
        }
    }
    
    //关闭path
    func closePath(){
        if context != nil{
            context.closePath()
        }
    }
    //线条绘制
    func strokePath(){
        if context != nil{
            context.strokePath()
        }
    }
    //填充绘制
    func fillPath(){
        if context != nil{
            context.fillPath()
        }
    }
    //线条绘制+填充绘制
    func strokeAndFillPath(){
        if context != nil{
            context.drawPath(using: CGPathDrawingMode.fillStroke)
        }
    }
    
    //绘制线条用block（beginPath + closePath + 你的绘制代码 + strokePath）
    func drawStrokeBlock(block:CGContextObjectDrawBlock_t){
        self.beginPath()
        
        let weakSelf = self
        block(weakSelf)
        
        self.closePath()
        self.strokePath()
    }
    
    //填充区域用block(beginPath + closePath + 你的绘制代码 + fillPath)
    func drawFillBlock(block:CGContextObjectDrawBlock_t){
        self.beginPath()
        
        let weakSelf = self
        block(weakSelf)
        
        self.closePath()
        self.fillPath()
    }
    
    //绘制+填充
    func drawStrokeAndFillBlock(block:CGContextObjectDrawBlock_t){
        self.beginPath()
        
        let weakSelf = self
        block(weakSelf)
        
        self.closePath()
        self.strokeAndFillPath()
    }
    
    //绘制线条用blcok，是否关闭曲线用closePath
    func drawStrokeBlock(block:CGContextObjectDrawBlock_t,closePath:Bool){
        self.beginPath()
        
        let weakSelf = self
        
        block(weakSelf)
        
        if closePath {
            self.closePath()
        }
        self.strokePath()
    }
    
    //填充用block，是否关闭曲线用closePath
    func drawFillBlock(block:CGContextObjectDrawBlock_t,closePath:Bool){
        self.beginPath()
        
        let weakSelf = self
        block(weakSelf)
        
        if closePath{
            self.closePath()
        }
        self.fillPath()
    }
    
    //绘制加填充，绘制用block，是否关闭曲线用closePath
    func drawStrokeAndFiilBlock(block:CGContextObjectDrawBlock_t,closePath:Bool){
        self.beginPath()
        
        let weakSelf = self
        block(weakSelf)
        
        if closePath{
            self.closePath()
        }
        self.strokeAndFillPath()
    }
    
    /********绘制图片API*********/
    
    func drawImage(image:UIImage, point:CGPoint){
        image.draw(at: point)
    }
    func drawImage(image:UIImage, point:CGPoint,blendMode:CGBlendMode,alpha:CGFloat){
        image.draw(at: point, blendMode: blendMode, alpha: alpha)
    }
    func drawImage(image:UIImage,rect:CGRect,blendMode:CGBlendMode,alpha:CGFloat){
        image.draw(in: rect, blendMode: blendMode, alpha: alpha)
    }
    func drawImage(image:UIImage,rect:CGRect){
        image.draw(in: rect)
    }
    
    /*********保存操作*********/
    
    //将当前设置存取到栈区中（入栈操作）
    func saveStateToStack(){
        if context != nil{
            context.saveGState()
        }
    }
    //从栈中取出之前保存的设置（出栈操作）
    func restoreStateFromStack(){
        if context != nil{
            context.restoreGState()
        }
    }
    
    /********图形绘制API*********/
    
    //移动到起始点
    func moveToStartPoint(point:CGPoint){
        if (context != nil){
           context.move(to: point)
        }
    }
    //添加一个点，与上一个点连接
    func addLineToPoint(point:CGPoint){
        if context != nil{
            context.addLine(to: point)
        }
    }
    //添加二次贝塞尔线，point是结束点，pointOne是控制点1，pointTwo是控制点2
    func addCurveToPoint(point:CGPoint,pointOne:CGPoint,pointTwo:CGPoint){
        if context != nil{
            context.addCurve(to: point, control1: pointOne, control2: pointTwo)

        }
    }

    //添加一次贝塞尔曲线，point是结束点，controlPoint是控制点
    func addQuadCurveToPoint(point:CGPoint,controlPoint:CGPoint){
        if context != nil{
            context.addQuadCurve(to: point, control: controlPoint)
        }
    }
    //在指定的区域填充彩色的矩形，rect为制定区域，gradientColor为渐变色对象
    func drawLinearCradientAtClipToRect(rect:CGRect,gradientColor:GradientColor){
        self.saveStateToStack()
        
        if context != nil{
            context.clip(to: rect)
            context.drawLinearGradient(gradientColor.gradientRef as! CGGradient, start: gradientColor.gradientStarPoint, end: gradientColor.gradientEndPoint, options: CGGradientDrawingOptions.drawsBeforeStartLocation)
        }
        self.restoreStateFromStack()
    }
    //添加一个矩形
    func addRect(rect:CGRect){
        if context != nil{
            context.addRect(rect)
            //print("addRect")
        }
    }
    //在给定的矩形中绘制椭圆
    func addEllopseInRect(rect:CGRect){
        if context != nil{
            context.addEllipse(in: rect)
        }
    }
    //将string绘制在给定的点上，attribute为富文本设置（可以为空）
    func drawString(string:NSString,point:CGPoint,attribute:Dictionary<NSAttributedStringKey,Any>){
        string.draw(at: point, withAttributes:  attribute)
    
    }
    //将string绘制在制定的区域
    func drawString(string:NSString,rect:CGRect,attribute:Dictionary<NSAttributedStringKey,Any>){
        string.draw(in: rect, withAttributes: attribute)
    }
    //将富文本绘制在制定的点上
    func drawAttributedString(string:NSAttributedString,point:CGPoint){
        string.draw(at: point)
    }
    //将富文本绘制在制定的矩形中
    func drawAttributeString(string:NSAttributedString,rect:CGRect){
        string.draw(in: rect)
    }

    /******重写setter getter方法*****/

//    func setStrokeColor(strokeColor:RGBColor){
//        if context != nil{
//            context.setFillColor(red: strokeColor.red, green: strokeColor.green, blue: strokeColor.blue, alpha: strokeColor.alpha)
//            
//        }
//    }
//        func setFillColor(fillColor:RGBColor){
//            if context != nil{
//                context.setFillColor(red: fillColor.red, green: fillColor.green, blue: fillColor.blue, alpha: fillColor.alpha)
//                print("setFillColor")
//            }
//        }
//        
//    
//    func setLineWidth(lineWidth:CGFloat){
//        if context != nil{
//            context.setLineWidth(lineWidth)
//        }
//    }
//    
//    func setLineCap(lineCap:CGLineCap){
//        if context != nil{
//            context.setLineCap(lineCap)
//        }
//    }
}
