from time import sleep

from gpiozero import DigitalInputDevice

# Define the GPIO pins for the line sensor inputs
pins = {
    "Near": 27,
    "CLP": 17,
    "S1 (far left)": 5,
    "S2 (left)": 6,
    "S3 (mid)": 13,
    "S4 (right)": 19,
    "S5 (far right)": 26,
}

sensors = {label: DigitalInputDevice(pin) for label, pin in pins.items()}

try:
    while True:
        values = [f"{label}: {int(sensor.value)}" for label, sensor in sensors.items()]
        print(" | ".join(values))
        sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")
