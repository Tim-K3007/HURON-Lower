import serial
import serial.tools.list_ports


def serial_com():
    mega_id = "95437313734351702142"
    global port
    port = "not found"

    list_of_ports = serial.tools.list_ports.comports()

    for portInfo in list_of_ports:
        if portInfo.serial_number == mega_id:
            port = portInfo.device
            break
        # print(portInfo.serial_number)

    if port == "not found":
        print("Make sure the right board is plugged in and re-run")
        exit(-1)


if __name__ == "__main__":
    serial_com()

    ser_port = serial.Serial(port)
    counter = 0

    while counter < 1000:
        data = str(ser_port.readline())
        data = data[2:][:-5]
        print(data)
        counter = counter + 1

    serial.Serial.close()

