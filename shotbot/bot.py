from relay import Relay
import redis, time
from rq import Queue, Connection
from flask import current_app

class Bot:
    def __init__(self, name):
        self.name = name
        self.state = 0
        #The target system, is 9 squares using x,y coordinates
        # It makes more sense for the bottom right to be 1,1 rather than 0,0 
        # (as we are targeting inside the square rather than at a specific position)
        #[1,3] [2,3] [3,3]
        #[1,2] [2,2] [3,2]
        #[1,1] [2,1] [3,1]
        self.target_x = 2
        self.target_y = 2
        self.v_rate = 3
        self.h_rate = 3
        self.relays = {
            "pan": Relay("pan", 5, 90),
            "up": Relay("up", 6, 15),
            "down": Relay("down", 13, 15),
            "left": Relay("left", 16, 15),
            "right": Relay("right",19 , 15),
            "pitch": Relay("pitch", 26, 90)
        }
        print("Initializing bot and ensuring relays are off")
        for relay in self.relays:
            self.relays[relay].switchOff() 

    def get_name(self):
        return self.name
        
    def get_target(self):
        return [self.target_x, self.target_y]

    def calibrate_center(self):
        self.target_x = 2
        self.target_y = 2
        return self.get_target()

    def enqueue_manual_move(self, relay):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(self.manual_move, relay)

    def manual_move(self, relay, timeout=15):
        if relay=='up':
            self.relays['down'].switchOff()
        if relay=='down':
            self.relays['up'].switchOff()
        if relay=='left':
            self.relays['right'].switchOff()
        if relay=='right':
            self.relays['left'].switchOff()
        self.relays[relay].switch()
        

    def execute_manual_move(self, relay, timeout):
        self.relays[relay].switchOn(timeout)
        time.sleep(timeout)

    def all_stop(self):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            print("Emptying worker queue. Current Size: " + str(q.count))
            q.empty()
        for relay in self.relays:
            self.relays[relay].switchOff()

    def execute_move(self, x_move, y_move):
        #Stop all movements before beginning a move command
        #This is done to prevent potentially sending "left and right"
        # or "up AND down" at the same time.
        self.relays['right'].switchOff()
        self.relays['left'].switchOff()
        self.relays['up'].switchOff()
        self.relays['down'].switchOff()
        self.relays['pan'].switchOff()
        total_move_seconds = 0
        if (x_move>0):
            total_move_seconds += x_move * self.h_rate
            self.relays['right'].switchOn(x_move * self.h_rate)
            print("Moving right " + str(total_move_seconds))
        elif (x_move<0):
            total_move_seconds += abs(x_move) * self.h_rate
            self.relays['left'].switchOn(abs(x_move) * self.h_rate)
            print("Moving left " + str(total_move_seconds))

        if (y_move>0):
            print("Moving up")
            if (abs(y_move) * self.h_rate>total_move_seconds): 
                total_move_seconds += abs(y_move) * self.h_rate
            self.relays['up'].switchOn(abs(y_move) * self.h_rate)
            print("Moving up " + str(total_move_seconds))
        elif (y_move<0):
            if (abs(y_move) * self.h_rate>total_move_seconds): 
                total_move_seconds += abs(y_move) * self.h_rate
            self.relays['down'].switchOn(abs(y_move) * self.h_rate)
            print("Moving down " + str(total_move_seconds))
        time.sleep(total_move_seconds)
        return total_move_seconds
    
    def set_target(self, target_x, target_y):
        x_move = 0
        y_move = 0
        if ((target_x>3) or (target_y>3) or (target_x<1) or (target_y<1)):
            raise ValueError("The target was out of bounds")
        
        if ((self.target_x != target_x) or (self.target_y != target_y)):
            #calucluate the x movement
            if (self.target_x > target_x):
                #it is smaller, move to the left
                x_move = 0-(self.target_x - target_x)
            elif (self.target_x < target_x):
                #it is larger, move to the left
                x_move = target_x - self.target_x

            if (self.target_y > target_y):
                #it is smaller, move down
                y_move = 0-(self.target_y - target_y)
            elif (self.target_y < target_y):
                #it is larger, move up
                y_move = target_y - self.target_y
            self.target_x = target_x
            self.target_y = target_y
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            #print("Queue size: " + str(q.count))
            task = q.enqueue(self.execute_move, x_move, y_move)
        #return [x_move, y_move, task]

    def level(self):
        self.relays['up'].switchOn(30)
        time.sleep(30)
        self.relays['down'].switchOn(15)
        time.sleep(15)

    def get_relays(self):
        return self.relays
