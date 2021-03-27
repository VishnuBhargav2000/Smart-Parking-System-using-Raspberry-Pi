# importing dependencies
import RPi.GPIO as GPIO
import time
import asyncio
import websockets
from datetime import datetime, timedelta 


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
    def __init__(self,triggerPins, echoPins):
        self.lots = [0,0,0,0,0,0]
        self.reservedLots = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}
        self.sensors = 2
        self.tempInfo = ''
        self.echoPins = echoPins
        self.triggerPins = triggerPins
        self.reserveTime = 1


    def parkingInfo(self):
            self.tempInfo = ''
            for sensor in range(self.sensors):
                self.tempInfo += GetDistance(self.triggerPins[sensor],self.echoPins[sensor])

    def reserveLot(self, lotId):
        self.lots[lotId] = 1
        self.reservedLots[lotId] = datetime.now() + timedelta(hours = self.reserveTime)
        

    def getFinalValue(self):
        self.parkingInfo()
        self.validateReservations()
        for lot in range(len(self.lots)):
            if self.lots[lot] == 1:
                self.tempInfo = self.tempInfo[:lot]+'T'+self.tempInfo[lot+1:]
        return self.tempInfo

    def validateReservations(self):
        now = datetime.now()
        for slot in self.reservedLots.keys():
            if now > reservedLots[slot]:
                self.lots[slot] = 0

async def handler(websocket, path):
    while True:
        await websocket.send(SPS.getFinalValue())
        reserveRequest = await websocket.recv()
        if int(reserveRequest) != -1:
            print(reserveRequest)
            SPS.reserveLot(int(reserveRequest))
        await asyncio.sleep(0.5)



SPS = SPSDriverClass(triggers,echos)

# driver code for websocket server
start_server = websockets.serve(handler, "192.168.0.9", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()






