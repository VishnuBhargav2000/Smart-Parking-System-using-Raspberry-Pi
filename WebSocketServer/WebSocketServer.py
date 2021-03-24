# importing dependencies
import RPi.GPIO as GPIO
import time
import asyncio
import websockets


# setting pins for pi
triggers = [7,13]  # Trigger pins
echos = [11,24]  # Echo pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def GetDistance(TRIG,ECHO):
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

    if distance > 10:
        isThere = 'F'
    else:
        isThere = 'T'

    return isThere

class SPSDriverClass:
    def __init__(self,echoPins, triggerPins):
        self.lots = [0,0]
        self.sensors = 2
        self.tempInfo = ''
        self.echoPins = echoPins
        self.triggerPins = triggerPins

    def parkingInfo(self):
            self.tempInfo = ''
            for sensor in range(self.sensors):
                self.tempInfo += GetDistance(triggerPins[sensor],echoPins[sensor])

    def reserveLot(self, lotId):
        self.lots[lotId] = 1
        time.sleep(20)
        self.lots[lotId] = 0
        

    def getFinalValue(self):
        self.parkingInfo()
        for lot in self.lots:
            if lot == 1:
                self.tempInfo[lot] = 'T'
        return self.tempInfo

async def webserver(websocket, path):
    # sends info on the parking spots to all connected clients every half-second
    while True:
        await websocket.send(SPS.getFinalValue()) # waits for new connections then sends info to all connected clients
        reserveRequest = await websocket.recv()
        print(type(reserveRequest))
        await asyncio.sleep(0.5)

SPS = SPSDriverClass(triggers,echos)
# driver code for websocket server
start_server = websockets.serve(webserver, "192.168.0.10", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



