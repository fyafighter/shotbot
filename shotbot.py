#import RPi.GPIO as GPIO
import signal, os

#GPIO.setmode(GPIO.BCM)

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

relay1 = Relay("Auto", 4, 5)
relay2 = Relay("Up", 22, 30)
relay3 = Relay("Down", 6, 30)
relay4 = Relay("Power", 26, 90)

while True:
    choice = raw_input("> ")
    choice = choice.lower()

    if ((choice == 'exit') or (choice == 'q') or (choice == 'quit')):
        print("Good bye.")
        relay1.switchOff()
        relay2.switchOff()
        relay3.switchOff()
        relay4.switchOff()
        #GPIO.cleanup()
        break
    if choice == '1':
        relay1.switch()
    if choice == '2':
        relay2.switch()
    if choice == '3':
        relay3.switch()
    if choice == '4':
        relay4.switch()

