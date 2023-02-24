import can
import cantools
import time

class motorCon:

    def __init__(self, canID, axisID):
        self.db = cantools.database.load_file("odrive-cansimple.dbc")
        self.bus = can.Bus(canID, bustype="socketcan")
        self.axis = axisID
        self.states = {"idle": 0x01, "calib": 0x03, "closeloop": 0x08}

        self.change_state("calib")
        print("Calibrating...")
        # time.sleep(15)

        # self.send_cmd('Set_Controller_Mode', {'Input_Mode':1, 'Control_Mode':3})

        # self.change_state("closeloop")
        # print("Entering closed loop")
        # time.sleep(1)
        
        # self.send_cmd('Set_Limits', {'Velocity_Limit':4.0, 'Current_Limit':70.0})

    def set_up(self):
        self.send_cmd('Set_Controller_Mode', {'Input_Mode':1, 'Control_Mode':3})

        self.change_state("closeloop")
        print("Entering closed loop")
        time.sleep(1)
        
        self.send_cmd('Set_Limits', {'Velocity_Limit':4.0, 'Current_Limit':70.0})

    def move_motor(self, pos, vel, tor):
        msg = self.db.get_message_by_name('Set_Input_Pos')
        data = msg.encode({'Input_Pos':pos, 'Vel_FF':vel, 'Torque_FF':tor})
        msg = can.Message(arbitration_id=self.axis << 5 | msg.frame_id, data=data, is_extended_id=False)
        self.bus.send(msg)

        msg = self.bus.recv()
        arbID = ((self.axisID << 5) | self.db.get_message_by_name('Heartbeat').frame_id)

        while(not (msg.arbitration_id == arbID and msg.data[0] & 0x01)):
            print("waiting")
        print("done")


    def kill_motor(self):
        self.change_state("idle")
        print("killed motor")

    def send_cmd(self, name_of_command, input):
        msg = self.db.get_message_by_name(name_of_command)
        data = msg.encode(input)
        msg = can.Message(arbitration_id=self.axis << 5 | msg.frame_id, is_extended_id=False, data=data)
        self.bus.send(msg)

    def change_state(self, s):
        try:
            self.states[s]
        except:
            print("unknown state" + s + "inputed into change_state()")

        self.send_cmd('Set_Axis_State', {'Axis_Requested_State': self.states[s]})

            
