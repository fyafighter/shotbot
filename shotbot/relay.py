import os, json, threading, time, random
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def timeoutRelay(relay):
  print('Timeout after '+str(relay.countdown)+' for ' + relay.name)
  relay.changeGPIO(GPIO.HIGH)
  relay.completion_time = None
 
class Relay:
  def __init__(self, name, pin, timeout=10):
    self.name = name
    self.pin = pin
    self.state = 0
    self.timer = None
    self.completion_time = False
    GPIO.setup(pin, GPIO.OUT)
    self.timeout = timeout
    self.countdown = timeout
    GPIO.setup(self.pin, GPIO.OUT)
    print(self.name + " is currently off")

  def serialize(self):
        return {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'timeout': self.timeout
        }

  def check(self):
    GPIO.setup(self.pin, GPIO.IN)
    print(self.name +" is  "+str(GPIO.input(self.pin)))
    self.state=GPIO.input(self.pin)
    GPIO.setup(self.pin, GPIO.OUT)

  def check_pin(self, pin):
    GPIO.setup(pin, GPIO.IN)
    status = GPIO.input(self.pin)
    print(str(pin) +" is  "+str(status))
    GPIO.setup(pin, GPIO.OUT)
    return status

  def switchOn(self, countdown=-1):
    self.state = 1
    if (countdown==-1):
      print("Using default timeout for the relay")
      self.countdown = self.timeout
    else:
      self.countdown = countdown
    print("Turn on " + self.name + " on pin " + str(self.pin) + " and setting timeout to " + str(self.countdown))
    self.timer = threading.Timer(self.countdown, timeoutRelay, args=[self])
    self.timer.start()
    self.completion_time = datetime.now() + timedelta(seconds=self.countdown)
    #CAUTION: We do not know what the motor will do if we signal up and down at the same
    #time, so we will try to avoid that.
    if (self.name=='up') and (self.check_pin(6)==0):
      print("Received a signal to move up but down is currently on. Switching")
      GPIO.output(6, GPIO.HIGH)
    elif (self.name=='down') and (self.check_pin(13)==0):
      print("Get the status of the up relay. It is on. Switch it off")
      GPIO.output(22, GPIO.HIGH)
    GPIO.output(self.pin, GPIO.LOW)

  def changeGPIO(self, gpio):
    GPIO.setup(self.pin, GPIO.OUT)
    GPIO.output(self.pin, gpio)

  def switchOff(self):
    self.state = 0
    print("Turn off " + self.name + " on pin " +str(self.pin) + " and resetting timer.")
    self.changeGPIO(GPIO.HIGH)
    if self.timer and self.timer.is_alive():
      self.timer.cancel()
      time.sleep(0.1)
      if self.timer.is_alive():
        print("Failed to kill the time out thread")
        time.sleep(self.timeout)
      else: 
        print("Killed the timer")
        self.completion_time = None

  def setState(self, state):
    if state!=self.state:
      self.switch()
    else:
      if self.timer:
        print("Restarting the timer for multiple button press")
        if self.timer.is_alive():
          self.timer.cancel()
          self.timer = threading.Timer(self.timeout, timeoutRelay, args=[self])
          self.timer.start()

  def switch(self):
    if (self.state):
      self.switchOff()
    else:
      self.switchOn()
  
  def time_remaining(self):
    if self.completion_time:
      print((self.completion_time - datetime.now()).seconds)
      return (self.completion_time - datetime.now()).seconds
    return 0
