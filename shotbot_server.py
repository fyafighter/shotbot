#!/usr/bin/env python
# coding=utf-8
from flask import Flask, jsonify, request #import main Flask class and request object
import os, json, threading, time, random

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
      print("Get the status of the up relay. If it is on. Switch it off")
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

relays = {
  "pan": Relay("pan", 5, 90), 
  "up": Relay("up", 6, 30), 
  "down": Relay("down", 13, 30), 
  "pitch": Relay("pitch", 26, 90),
  "left": Relay("left", 16, 90),
  "right": Relay("right",19 , 90)
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
    if (command_param=='bouncers'): grounder_shots()
    elif (command_param=='edges'): edge_shots()
    elif (command_param=='random'): random_shots()
    elif (command_param=='level'): level()
    else: shutdown()
    return("Running "+ command_param)

def random_shots():
  print("Running random mode")
  # there are 18 times slots (90/5 - the ball shoots about every 5 seconds)
  ##transitions
  #also never do up/up or down/down
  #0 = up
  #1 = up+pan
  #2 = stop
  #3 = pan
  #4 = down+pan
  #5 = down

  last_vert = 0
  relays['pitch'].switchOn()
  for x in range(18):
    #transition!
    this_move = random.randint(0,5)
    
    while((this_move > 3) and (last_vert > 3)):
      print("Can't do 2 downs in a row "+ str(this_move))
      this_move = random.randint(0,5)
    while((this_move < 2) and (last_vert < 2)):
      print("Can't do 2 up in a row "+ str(this_move))
      this_move = random.randint(0,5)

    last_move = this_move
    stop_moving()
    if this_move==0:
      print("Random move is up next")
      relays['up'].switchOn()
      last_vert = 1
    elif this_move == 1:
      print("Random move is up/pan next")
      relays['up'].switchOn()
      relays['pan'].switchOn()
      last_vert = 1
    elif this_move == 2:
      print("Random move is stop next")
    elif this_move == 3:
      print("Random move is pan next")
      relays['pan'].switchOn() 
    elif this_move == 4:
      print("Random move is pan/down next")
      relays['pan'].switchOn()
      relays['down'].switchOn()
      last_vert = 4
    elif this_move == 5:
      print("Random move is down next")
      relays['down'].switchOn()
      last_vert = 4
    time.sleep(5)

def edge_shots():
  print("Edge shots don't currently work; going random.")
  random_shots()

def grounder_shots():
  shutdown()
  print("Running grounder mode")
  relays['pan'].switchOn()
  relays['pitch'].switchOn()
  relays['down'].switchOn()
  time.sleep(5)
  relays['down'].switchOff()
  time.sleep(85)
  relays['up'].switchOn()
  time.sleep(5)
  relays['up'].switchOff()
  relays['pitch'].switchOff()

def level():
  shutdown()
  print("Leveling")
  relays['up'].switchOn()
  time.sleep(30)
  relays['up'].switchOff()
  relays['down'].switchOn()
  time.sleep(14)
  relays['down'].switchOff()

def shutdown():
  relays['up'].switchOff()
  relays['pan'].switchOff()
  relays['down'].switchOff()
  relays['pitch'].switchOff()
  relays['left'].switchOff()
  relays['right'].switchOff()
  print("Shutting down")

def stop_moving():
  relays['up'].switchOff()
  relays['pan'].switchOff()
  relays['down'].switchOff()
  relays['left'].switchOff()
  relays['right'].switchOff()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)