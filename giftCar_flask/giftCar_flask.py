# coding:utf-8

from flask import Flask, render_template

from carCtrl import CarCtrlClass
import carCtrl
app = Flask(__name__)
myCarCtrl = carCtrl.CarCtrlClass(29, 12, 15, 16, 0)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/carEvents/<direction>')
def carEvents(direction):
    (dir, value) = direction.split("-")
    print dir, value
    if dir == 'go':
        if value == "true":
            myCarCtrl.go(True)
        else:
            myCarCtrl.go(False)
    elif dir == "down":
        if value == "true":
            myCarCtrl.down(True)
        else:
            myCarCtrl.down(False)
    elif dir == "left":
        if value == "true":
            myCarCtrl.left(True)
        else:
            myCarCtrl.left(False)
    elif dir == "right":
        if value == "true":
            myCarCtrl.right(True)
        else:
            myCarCtrl.right(False)
    elif dir == "stop":
        myCarCtrl.stop()
    return dir


if __name__ == '__main__':
    app.run(host="192.168.100.2", port=8989, debug=True)
    # app.run(host="192.168.100.3", port=8989, debug=True)
