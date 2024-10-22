import struct
import time

import serial

PORT = "/dev/ttyACM0"
SERIAL_BAUD = 115200
COMM = serial.Serial(PORT, SERIAL_BAUD, timeout=1)

START_BYTE = 0xAA
END_BYTE = 0xBB

RIGHT_MOTOR = 7
LEFT_MOTOR = 6


def send_command(command_byte, slaveID, data=None):

    message = [START_BYTE, command_byte, slaveID]

    if data is not None:
        message.extend(struct.pack(">H", data))
    message.append(END_BYTE)

    COMM.write(bytearray(message))

    print("Sent bytes: [", ", ".join(f"0x{b:02X}" for b in message), "]")


def read_arduino():

    while COMM.in_waiting == 0:
        pass

    while COMM.in_waiting > 0:
        print(COMM.readline().decode("utf-8").strip())


def wait_for_arduino():

    msg = ""

    while msg.find("ARDUINO_READY") == -1:
        if COMM.in_waiting > 0:
            msg = COMM.readline().decode("utf-8").strip()
            print(msg)


def setSpeed(slaveID, speed):
    send_command(0x01, slaveID, speed)


def getSpeed(slaveID):
    send_command(0x02, slaveID)
    read_arduino()


def motorEnableForward(slaveID):
    send_command(0x03, slaveID)


def motorEnableBackward(slaveID):
    send_command(0x04, slaveID)


def motorBrakeForward(slaveID):
    send_command(0x05, slaveID)


def motorBrakeBackward(slaveID):
    send_command(0x06, slaveID)


def motorDisable(slaveID):
    send_command(0x07, slaveID)


def setRightSpeed(speed):
    setSpeed(RIGHT_MOTOR, speed)


def setLeftSpeed(speed):
    setSpeed(LEFT_MOTOR, speed)


def getRightSpeed():
    getSpeed(RIGHT_MOTOR)


def getLeftSpeed():
    getSpeed(LEFT_MOTOR)


def rightForward():
    motorEnableForward(RIGHT_MOTOR)


def leftForward():
    motorEnableForward(LEFT_MOTOR)


def rightBackward():
    motorEnableBackward(RIGHT_MOTOR)


def leftBackward():
    motorEnableBackward(LEFT_MOTOR)


def rightBrakeForward():
    motorBrakeForward(RIGHT_MOTOR)


def rightBrakeBackward():
    motorBrakeBackward(RIGHT_MOTOR)


def leftBrakeForward():
    motorBrakeForward(LEFT_MOTOR)


def leftBrakeBackward():
    motorBrakeBackward(LEFT_MOTOR)


def rightDisable():
    motorDisable(RIGHT_MOTOR)


def leftDisable():
    motorDisable(LEFT_MOTOR)


def main():

    wait_for_arduino()

    setRightSpeed(0)
    setLeftSpeed(0)

    rightForward()
    leftForward()
    time.sleep(3)

    rightBrakeForward()
    leftBrakeForward()
    time.sleep(3)

    rightBackward()
    leftBackward()
    time.sleep(3)

    rightBrakeBackward()
    leftBrakeBackward()
    time.sleep(3)

    rightDisable()
    leftDisable()


if __name__ == "__main__":
    main()
