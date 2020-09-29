#! /usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, division
import rospy
import numpy as np
import cv2
from geometry_msgs.msg import Twist, Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3
import math
import time
from tf import transformations
import sys


n = None

ang = None
dist = None
t_muda_direcao = None

max_angular = None
max_linear = None

contador = 0
pula = 100

if __name__=="__main__":

    rospy.init_node("square")

    t0 = rospy.get_rostime()

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    
    n=1
    
    ang = math.pi/2
    dist = 5
    t_muda_direcao = 5
    
    max_angular = 0.4
    max_linear = 0.4

    while not rospy.is_shutdown():
        print("t0", t0)
        if t0.nsecs == 0:
            t0 = rospy.get_rostime()
            print("waiting for timer")
            continue        
        t1 = rospy.get_rostime()
        elapsed = (t1 - t0)
        print("Passaram ", elapsed.secs, " segundos")
        rospy.sleep(1.0)

        if elapsed.secs % t_muda_direcao == 0:
            print("Mudando de direção.")
            vel_parado = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
            vel_reto = Twist(Vector3(max_linear, 0, 0), Vector3(0, 0, 0))
            vel_muda_direcao = Twist(Vector3(0, 0, 0), Vector3(0, 0, max_angular))

            sleep_muda_direcao = abs(ang/max_angular)
            sleep_reto = abs(dist/max_linear)
            
            if n % 2 != 0:
                print(vel_reto, "\n",  sleep_reto)
                velocidade_saida.publish(vel_reto)
                rospy.sleep(sleep_reto)
                velocidade_saida.publish(zero)
                n+=1
                
            elif n % 2 == 0:
                print(vel_muda_direcao, "\n",  sleep_muda_direcao)
                velocidade_saida.publish(vel_muda_direcao)
                rospy.sleep(sleep_muda_direcao)
                velocidade_saida.publish(zero)
                n+=1
                
            else:
                print("Alguma coisa deu errado.")
            
            if n % 8 == 0:
                print("Terminou um ciclo")