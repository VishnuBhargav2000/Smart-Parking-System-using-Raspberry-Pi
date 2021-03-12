#importing dependencies
import RPi.GPIO as GPIO
import time
import asyncio
import websockets

#setting pins for pi 
TRIG=7
ECHO=11
GPIO.setmode(GPIO.BOARD)


def GetInfo():
    # driver code for ultrasonic sensor thats connected to raspberry pi
    # returns a string (True/False) based on the distance data accquired from the sensor
    # True = if distance greater than a pre defined value, False if lesser. which indicates if a spot is taken or available 
    isThere = True
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
    GPIO.output(TRIG,False)
    time.sleep(0.2)
    
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    if distance > 10:
        isThere = False
    else:
        isThere = True
    return str(isThere)    


async def webserver(websocket, path):
    # sends info on the parking spots to all connected clients every half-second
    while True:
        await websocket.send(GetInfo()) # waits for new connections then sends info to all connected clients
        await asyncio.sleep(0.5) 

# driver code for websocket server
start_server = websockets.serve(webserver, "192.168.0.8", 5678) 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

