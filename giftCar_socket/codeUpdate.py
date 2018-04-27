# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/26 08:24

from fabric.api import *

env.hosts = "pi@192.168.100.2"


@runs_once
@task
def local_update():
    with lcd("~/Documents/giftCar"):
        local("git add -A")
        local("git commit -m 'update 4'")
        local("git pull origin master")
        local("git push -u origin  master")


@task
def remote_update():
    with cd("/home/pi/RaspbianPython/giftCarProject"):
        # run("ls -l")
        run("git checkout -- *")
        run("git checkout master")
        run("git pull origin master")


@task
def go():
    local_update()
    remote_update()

# scp -r ../giftCar_socket pi@192.168.100.2:/home/pi/RaspbianPython/giftCarProject

# gcc speed.c -shared -lwiringPi -o speed.so