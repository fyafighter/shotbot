from flask import Flask, jsonify, request #import main Flask class and request object
import os, json, threading, time

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
      GPIO.output(6, GPIO.LOW)
    elif (self.name=='down') and GPIO.input(22):
      print("Get the status of the up relay. If it is on. Switch it off")
      GPIO.output(22, GPIO.LOW)
    GPIO.output(self.pin, GPIO.HIGH)

  def switchOff(self):
    self.state = 0
    print("Turn off " + self.name + " on pin " +str(self.pin) + " and resetting timer.")
    GPIO.output(self.pin, GPIO.LOW)
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

relays = {
  "pan": Relay("pan", 4, 90), 
  "up": Relay("up", 22, 30), 
  "down": Relay("down", 6, 30), 
  "pitch": Relay("pitch", 26, 90)
}

transition_queue = []
engaged=False

app = Flask(__name__) #create the Flask app

@app.route('/')
def index():
  return 'Shotbot is online.'

def processRelayState(relay_list):
  for r in relay_list:
    print(r)

@app.route('/relay', methods=['POST', 'GET'])
def relay():
    if (request.method=='POST'):
        for r in request.json['relays']:
          relays[r['name']].setState(r['state'])
    return jsonify(relays=[r.serialize() for r in relays.values()])

@app.route('/command', methods=['POST'])
def command():
  command_param = request.args.get("switch")
  print(command_param)
  if (command_param in relays):
    relays[command_param].switch()
    return jsonify(relays[command_param].state)
  else:
    print("A macro command! Do cool stuff!")
    if (command_param=='grounders'): grounder_shots()
    elif (command_param=='edges'): edge_shots()
    elif (command_param=='random'): random_shots()
    elif (command_param=='level'): level()
    else: shutdown()
    return("Running "+ command_param)

def random_shots():
  print("Running random mode")

def edge_shots():
  print("Running random mode")

def grounder_shots():
  print("Running grounder mode")

def level():
  print("Leveling")

def shutdown():
  print("Shutting down")

#state
#transitions
#up/pan
#down/pan
#up
#down
#stop


def engage():
  relays['pan'].switchOn()
  #For 90 seconds go up and down at random intervals of no more than 10 seconds in each direction. 
  #Do a level motion at the end
  total = 0
  engaged=True
  relays['pan'].switchOn()
  relays['up'].switchOn()
  time.sleep(5)
  relays['down'].switchOn()
  time.sleep(5)
  relays['up'].switchOn()
  time.sleep(5)
  relays['down'].switchOn()
  time.sleep(5)
  relays['up'].switchOn()
  time.sleep(5)
  relays['down'].switchOn()
  time.sleep(5)
  relays['up'].switchOn()
  time.sleep(5)
  relays['pan'].switchOff()
  
  engaged=False
  #while(total<90):
  return jsonify(relays=[r.serialize() for r in relays.values()])

if __name__ == '__main__':
    app.run(port=5000, debug=True)