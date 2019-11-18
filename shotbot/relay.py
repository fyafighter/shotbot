import os, json, threading, time, random, signal

class Relay:
  def __init__(self, name, pin, timeout=10):
    self.name = name
    self.pin = pin
    self.state = 0
    #GPIO.setup(pin, GPIO.OUT)
    self.timeout = timeout
    print(self.name + " is currently off")
    
 #Setup the signal handler for timeouts. 
  def timeoutRelay(self, signum, frame):
    print('Timeout for relay', signum)
    self.switchOff()

  def switchOn(self):
    self.state = 1
    print("Turn on " + self.name + " on pin " + str(self.pin) + " and setting timeout to " + str(self.timeout))
    signal.signal(signal.SIGALRM, self.timeoutRelay)
    signal.alarm(self.timeout)
    #print(GPIO.input(self.pin))
    #GPIO.output(self.pin, GPIO.HIGH)

  def switchOff(self):
    self.state = 0
    print("Turn off " + self.name + " on pin " + str(self.pin))
    #GPIO.output(self.pin, GPIO.LOW)

  def switch(self):
    if (self.state):
      #GPIO.output(self.pin, GPIO.LOW)
      self.state = 0
      print("Turn off " + self.name + " on pin " +str(self.pin) + " and resetting timer.")
      signal.alarm(0)
    else:
      #GPIO.output(self.pin, GPIO.HIGH)
      self.state = 1
      #print("Turn on " + self.name + " on pin " + str(self.pin))
      print("Turn on " + self.name + " on pin " + str(self.pin) + " and setting timeout to " + str(self.timeout))
      signal.signal(signal.SIGALRM, self.timeoutRelay)
      signal.alarm(self.timeout)