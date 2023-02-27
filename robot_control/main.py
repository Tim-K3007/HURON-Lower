from motorCon import motorCon
import time

left_roll = motorCon("can0", 0x1)
left_knee = motorCon("can0", 0x0)
time.sleep(15)
left_roll.set_up()
left_knee.set_up()
time.sleep(1)

# for x in range(10):
#     if x % 2 == 0:
#         left_knee.move_motor(10, 0, 0) 
#         left_roll.move_motor(5, 0, 0)
#     else:
#         left_knee.move_motor(0, 0, 0)
#         left_roll.move_motor(-5, 0, 0)

left_knee.move_motor(10, 0, 0) 
left_roll.move_motor(5, 0, 0)

# done = False
# while not done:
#     done = left_knee.check_heartbeat() and left_roll.check_heartbeat()

time.sleep(10)
# left_knee.move_motor(0, 0, 0)
# left_roll.move_motor(-5, 0, 0)

left_knee.move_motor(0, 0, 0) 
left_roll.move_motor(0, 0, 0)

# done = False
# while not done:
#     done = left_knee.check_heartbeat() and left_roll.check_heartbeat()

time.sleep(10)
left_roll.kill_motor()
left_knee.kill_motor()
