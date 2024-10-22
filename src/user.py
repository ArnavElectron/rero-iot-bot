# User code

# TODO : integrate with backend to receive user code and insert into main()

# Imports
import time

from motor.motor import Motor

# Global settings
SLAVE_ID_1 = 7
SLAVE_ID_2 = 6

rightMotor = Motor(SLAVE_ID_1)
leftMotor = Motor(SLAVE_ID_2)


# Add another layer of 'abstraction'
# These are the actual functions to be given to the users


def set_right_speed(speed):
    rightMotor.setSpeed(speed)


def set_left_speed(speed):
    leftMotor.setSpeed(speed)


def get_right_speed():
    return rightMotor.getSpeed()


def get_left_speed():
    return leftMotor.getSpeed()


def get_right_direction():
    return rightMotor.getDirection()


def get_left_direction():
    return leftMotor.getDirection()


def stop_right():
    return rightMotor.haltMotor()


def stop_left():
    return leftMotor.haltMotor()


def main():

    # Example user code

    stop_right()
    stop_left()
    print("Running motor.py...")
    time.sleep(2)

    set_right_speed(25)
    set_left_speed(25)
    time.sleep(5)

    print("Right Motor :", get_right_speed(), get_right_direction())
    print("Left Motor :", get_left_speed(), get_left_direction())
    time.sleep(5)

    stop_right()
    stop_left()
    time.sleep(2)

    set_right_speed(-25)
    set_left_speed(-25)
    time.sleep(5)

    print("Right Motor :", get_right_speed(), get_right_direction())
    print("Left Motor :", get_left_speed(), get_left_direction())
    time.sleep(5)

    stop_right()
    stop_left()


if __name__ == "__main__":
    main()
