from relay import Relay
from markdown import markdown

class Shotbot:
  def __init__(self, name):
    self.name = name
    self.state = 0
    self.target = [1,1]
    self.relays = {
        "pan": Relay("pan", 5, 90), 
        "up": Relay("up", 6, 30), 
        "down": Relay("down", 13, 30), 
        "pitch": Relay("pitch", 26, 90),
        "left": Relay("left", 16, 90),
        "right": Relay("right",19 , 90)
        }
        
    def get_target():
        return self.target

    def set_target(target):
        self.target = target