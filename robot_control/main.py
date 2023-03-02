import math
from motorCon import motorCon
import time

R = [0, 0, -1, 0, 1, 0, 1, 0, 0]
joint_lengths = [77.5, 0, 167, 0, 530, 410, 20]
l0 = 77.5
l1 = 0
l2 = 167
l3 = 0
l4 = 530
l5 = 410
l6 = 20

left_roll = motorCon("can0", 0x1)
left_knee = motorCon("can0", 0x0)
time.sleep(15)
left_roll.set_up()
left_knee.set_up()

# for x in range(10):
#     if x % 2 == 0:
#         left_knee.move_motor(10, 0, 0) 
#         left_roll.move_motor(5, 0, 0)
#     else:
#         left_knee.move_motor(0, 0, 0)
#         left_roll.move_motor(-5, 0, 0)

left_knee.move_motor(5, 0, 0) 
# left_roll.move_motor(5, 0, 0)

done = False
while not done:
    done = left_knee.check_if_there() #and left_roll.check_if_there()

# time.sleep(10)
# left_knee.move_motor(0, 0, 0)
# left_roll.move_motor(-5, 0, 0)

left_knee.move_motor(0, 0, 0) 
# left_roll.move_motor(0, 0, 0)

done = False
while not done:
    done = left_knee.check_if_there() #and left_roll.check_if_there()

# time.sleep(10)
left_roll.kill_motor()
left_knee.kill_motor()

def IK(targetPos):

    px = targetPos[0]
    py = targetPos[1]
    pz = targetPos[2]
    nx = R[0]
    ny = R[1]
    nz = R[2]
    sx = R[3]
    sy = R[4]
    sz = R[5]
    ax = R[6]
    ay = R[7]
    az = R[8]

    D = ((px+l6)^2+py^2+pz^2-l4^2-l5^2)/(2*l4*l5)
    
    th4 = math.atan2(-math.sqrt(1-D^2),D)
    th5 = math.atan2((math.sqrt(px+l6)^2+py^2),-pz) - math.atan2(math.sin(th4)*l4,math.cos(th4)*l4+l5)-2*math.pi
    th6 = math.atan2((-px-l6),py) 
    if (math.cos(th4+th5)*l4+math.cos(th5)*l5)<0:
        th6=th6+math.pi

    th2 = math.atan2(math.sqrt(1-(math.sin(th6)*ax+math.cos(th6)*ay)^2),math.sin(th6)*ax+cos(th6)*ay)   
    
    th1 = math.atan2(-math.sin(th6)*sx-math.cos(th6)*sy, -math.sin(th6)*nx-math.cos(th6)*ny) 
    if math.sin(th2)<0:
        th1=th1+math.pi
    
    th345=math.atan2(az, math.cos(th6)*ax-math.sin(th6)*ay)
    if (math.sin(th2)<0):
        th345=th345+math.pi

    th1 = th1 + math.pi/2
    th6 = th6 - math.pi/2
    th3 = th345 - th4 - th5  - math.pi 

    q = [th1,th2,th3,th4,th5,th6]
