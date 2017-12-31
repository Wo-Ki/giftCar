# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/29 08:28

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="192.168.100.3", port=8989, debug=True)
