from motorCon import motorCon
import time

testmotor = motorCon("can0", 0x0)
secondtest = motorCon("can1", 0x2)
print("going to pos 1")
testmotor.move_motor(1, 0, 0)
time.sleep(2)
print("going to pos 0.5")
testmotor.move_motor(0.5, 0, 0)
time.sleep(2)
print("going to pos -1")
testmotor.move_motor(-1, 0, 0)
time.sleep(2)
testmotor.kill_motor()
secondtest.kill_motor()
