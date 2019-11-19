import os, json, threading, time, random, signal

class GPIO:
  @staticmethod
  def OUT():
    return
  @staticmethod
  def LOW():
    return
  @staticmethod
  def HIGH():
    return
  @staticmethod
  def setup(x, y):
    print("setup debug")
  @staticmethod
  def input(x):
    print("input debug")
    return 1
  @staticmethod
  def output(x,y):
    print("switched debug")

def timeoutRelay(relay):
  print('Timeout after '+str(relay.timeout)+' for relay')
  relay.switchOff()
 
class Relay:
  def __init__(self, name, pin, timeout=10):
    self.name = name
    self.pin = pin
    self.state = 0
    self.timer = None
    GPIO.setup(pin, GPIO.OUT)
    self.timeout = timeout
    print(self.name + " is currently off")

  def serialize(self):
        return {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'timeout': self.timeout
        }

  def check(self):
    print(self.name +" is  "+str(GPIO.input(self.pin)))
    self.state=GPIO.input(self.pin)

  def switchOn(self):
    self.state = 1
    print("Turn on " + self.name + " on pin " + str(self.pin) + " and setting timeout to " + str(self.timeout))
    self.timer = threading.Timer(self.timeout, timeoutRelay, args=[self])
    self.timer.start()
    #CAUTION: We do not know what the motor will do if we signal up and down at the same
    #time, so we will try to avoid that.
    if (self.name=='up') and GPIO.input(6):
      print("Received a signal that to move up but down is currently on. Switching")
      GPIO.output(6, GPIO.HIGH)
    elif (self.name=='down') and GPIO.input(13):
      print("Get the status of the up relay. It is on. Switch it off")
      GPIO.output(22, GPIO.HIGH)
    GPIO.output(self.pin, GPIO.LOW)

  def switchOff(self):
    self.state = 0
    print("Turn off " + self.name + " on pin " +str(self.pin) + " and resetting timer.")
    GPIO.output(self.pin, GPIO.HIGH)
    if self.timer:
      self.timer.cancel()

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