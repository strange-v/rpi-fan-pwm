import os
import time
import RPi.GPIO as gpio


PIN_FAN = 18
PWM_FREQ = 60
INTERVAL = 5
FAN_MIN_SPEED = 20
FAN_MAX_SPEED = 100
FAN_START_SPEED = 50
TEMP_MIN = 35
TEMP_MAX = 70

currentSpeed = 0


def getTemperature():
    value = os.popen(
        r'vcgencmd measure_temp | egrep -o "[0-9]*\.[0-9]*"').readline()
    return float(value)


def setFanSpeed(speed):
    global currentSpeed

    if currentSpeed == 0:
        fan.ChangeDutyCycle(FAN_START_SPEED)
        time.sleep(1)

    fan.ChangeDutyCycle(speed)
    currentSpeed = speed


def handleFanSpeed():
    temp = getTemperature()

    #(x - input_start) / (input_end - input_start) * (output_end - output_start) + output_start
    value = (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN) * \
        (FAN_MAX_SPEED - FAN_MIN_SPEED) + FAN_MIN_SPEED
    speed = int(round(value))
    if (speed < FAN_MIN_SPEED):
        speed = FAN_MIN_SPEED

    setFanSpeed(speed)
    #print('temp: {}, speed: {}'.format(temp, speed))


def initFan():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_FAN, gpio.OUT, initial=gpio.LOW)
    return gpio.PWM(PIN_FAN, PWM_FREQ)


try:
    fan = initFan()
    fan.start(0)

    while True:
        handleFanSpeed()
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    fan.stop()

