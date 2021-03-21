# importing dependencies
import RPi.GPIO as GPIO
import time
import asyncio
import websockets


# setting pins for pi
triggers = [pin1,pin2]  # Trigger pins (viable pins - [7,13])
echos = [pin1,pin2]  # Echo pins  (viable pins - [11, 24]) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)


def GetDistance(TRIG,ECHO, carDistance):
    # driver code for ultrasonic sensor thats connected to raspberry pi
    # returns a string (True/False) based on the distance data accquired from the sensor
    # True = if distance greater than a pre defined value, False if lesser. which indicates if a spot is taken or available

    isThere = 'T'
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > carDistance:

        isThere = 'F'
    else:
        isThere = 'T'

    return isThere

def GetInfo():
    NumberOfSensors = 2 # number of Hc-SR04 modules used
    carDistance = 5 # distance between Hc-SC04 module and a car parked in the respective parking lot
    info = ''
    for sensor in range(NumberOfSensors):
        info += GetDistance(triggers[sensor],echos[sensor],carDistance)
    return info


async def webserver(websocket, path):
    # sends info on the parking spots to all connected clients every half-second
    while True:
        await websocket.send(GetInfo())  # waits for new connections then sends info to all connected clients
        await asyncio.sleep(0.5)

# driver code for websocket server
start_server = websockets.serve(webserver, "IP", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


