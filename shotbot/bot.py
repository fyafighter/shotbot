from relay import Relay

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
            "up": Relay("up", 6, 30),
            "down": Relay("down", 13, 30),
            "left": Relay("left", 16, 90),
            "right": Relay("right",19 , 90),
            "pitch": Relay("pitch", 26, 90)
        }

    def get_name(self):
        return self.name
        
    def get_target(self):
        return [self.target_x, self.target_y]
    
    def set_target(self, target_x, target_y):
        move = [0,0]
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
        return [x_move, y_move]

    def get_relays(self):
        return self.relays