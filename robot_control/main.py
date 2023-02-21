from motorCon import motorCon
import time

right_roll = motorCon("can0", 0x1)
right_knee = motorCon("can0", 0x0)
time.sleep(15)

# for x in range(10):
#     if x % 2 == 0:
#         right_knee.move_motor(10, 0, 0) 
#         right_roll.move_motor(5, 0, 0)
#     else:
#         right_knee.move_motor(0, 0, 0)
#         right_roll.move_motor(-5, 0, 0)

right_knee.move_motor(10, 0, 0) 
right_roll.move_motor(5, 0, 0)
right_knee.move_motor(0, 0, 0)
right_roll.move_motor(-5, 0, 0)

right_roll.kill_motor()
right_knee.kill_motor()
