import can
import cantools
import time


class motorCon:

    def __init__(self, canID, axisID):
        self.db = cantools.database.load_file("odrive-cansimple.dbc")
        self.bus = can.Bus(canID, bustype="socketcan")
        self.axis = axisID
        self.states = {"idle": 0x01, "calib": 0x03, "closeloop": 0x08}
        self.desired_pos = 0

        self.change_state("calib")
        print("Calibrating...")

    def set_up(self):
        self.send_cmd('Set_Controller_Mode', {
                      'Input_Mode': 1, 'Control_Mode': 3})

        self.change_state("closeloop")
        print("Entering closed loop")
        time.sleep(1)

        self.send_cmd(
            'Set_Limits', {'Velocity_Limit': 4.0, 'Current_Limit': 70.0})

    def move_motor(self, pos, vel, tor):
        self.desired_pos = pos

        msg = self.db.get_message_by_name('Set_Input_Pos')
        data = msg.encode({'Input_Pos': pos, 'Vel_FF': vel, 'Torque_FF': tor})
        msg = can.Message(arbitration_id=self.axis << 5 |
                          msg.frame_id, data=data, is_extended_id=False)
        self.bus.send(msg)

    def check_if_there(self):
        msg = self.bus.recv()
        arbID = ((self.axis << 5) | self.db.get_message_by_name(
            'Get_Encoder_Estimates').frame_id)

        flag = False

        if msg.arbitration_id == arbID:
            pos = self.db.decode_message('Get_Encoder_Estimates', msg.data)[
                'Pos_Estimate']
            return abs(pos - self.desired_pos) <= 0.02

        return flag

    def kill_motor(self):
        self.change_state("idle")
        print("killed motor")

    def send_cmd(self, name_of_command, input):
        time.sleep(0.5)
        msg = self.db.get_message_by_name(name_of_command)
        data = msg.encode(input)
        msg = can.Message(arbitration_id=self.axis << 5 |
                          msg.frame_id, is_extended_id=False, data=data)
        self.bus.send(msg)

    def change_state(self, s):
        try:
            self.states[s]
        except:
            print("unknown state" + s + "inputed into change_state()")

        self.send_cmd('Set_Axis_State', {
                      'Axis_Requested_State': self.states[s]})
