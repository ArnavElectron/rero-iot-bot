# Python code to run the RMCS-2303 Motor Driver
# Abandon all hope, ye who enter

# Imports
import minimalmodbus

# Global settings
PORT = "/dev/ttyUSB0"
BAUD = 9600
TIMEOUT = 4


# Motor Class
class Motor:

    # Initialize connection
    def __init__(self, slave_id):
        self.driver = minimalmodbus.Instrument(PORT, slave_id)
        self.driver.serial.baudrate = BAUD
        self.driver.serial.timeout = TIMEOUT
        self.driver.mode = minimalmodbus.MODE_ASCII

    # Reset drive -- loads default values for:
    #   - Position Proportional Gain
    #   - Position Integral Gain
    #   - Velocity Feed Forward Gain
    #   - Lines Per Rotation
    #   - Acceleration
    #   - Speed
    #   - LSB & MSB Of Position
    def __reset_drive(self):
        self.driver.write_register(registeraddress=4, value=0, functioncode=6)

        control_value = (self.driver.address << 8) | 0xFF
        self.driver.write_register(
            registeraddress=0, value=control_value, functioncode=6
        )
        # Now power reset the drive to load defaults

    # Restarts the driver
    def __restart_drive(self):
        self.driver.write_register(registeraddress=2, value=0x0900, functioncode=6)

    # Enable motor in Digital Mode and set direction
    def __enable_digital_mode(self, direction):
        if direction == 0:
            control_value = 0x0101
        elif direction == 1:
            control_value = 0x0109
        self.driver.write_register(
            registeraddress=2, value=control_value, functioncode=6
        )

    # Disable motor in Digital Mode
    def __disable_digital_mode(self, direction):
        if direction == 0:
            control_value = 0x0100
        elif direction == 1:
            control_value = 0x0108
        self.driver.write_register(
            registeraddress=2, value=control_value, functioncode=6
        )

    # Brake motor -- applies reverse polarity (not recommended)
    def __brake_motor(self, direction):
        if direction == 0:
            control_value = 0x0104
        elif direction == 1:
            control_value = 0x010C
        self.driver.write_register(
            registeraddress=2, value=control_value, functioncode=6
        )

    # Stops motor -- maintains position (not recommended)
    def __stop_motor(self):
        self.driver.write_register(registeraddress=2, value=0x0701, functioncode=6)

    # Stops motor -- power cutoff (recommended)
    def __e_stop_motor(self):
        self.driver.write_register(registeraddress=2, value=0x0700, functioncode=6)

    # Sets encoder count to 0
    def __set_home_position(self):
        self.driver.write_register(2, 0x0800, 0, functioncode=6)

    # Set speed of motor
    # TODO : map speed to actual RPM
    def setSpeed(self, speed):
        if speed < 0:
            self.__enable_digital_mode(direction=1)
        else:
            self.__enable_digital_mode(direction=0)
        self.driver.write_register(registeraddress=14, value=abs(speed), functioncode=6)

    # Get speed of motor
    # TODO : map actual RPM to speed
    def getSpeed(self):
        speed = self.driver.read_register(
            registeraddress=24, number_of_decimals=0, functioncode=3
        )
        if speed > 32765:
            speed = speed - 65535
        return speed

    # Get direction of motor
    def getDirection(self):
        direction_code = self.driver.read_register(registeraddress=2, functioncode=3)
        direction = None
        if direction_code == 0x0101:
            direction = 0
        elif direction_code == 0x0109:
            direction = 1
        return direction

    # Halt motor -- maps to :
    #   - self.__brake_motor() (not recommended)
    #   - self.__stop_motor() (not recommended)
    #   - self.__e_stop_motor() (recommended)
    def haltMotor(self):
        self.__e_stop_motor()
