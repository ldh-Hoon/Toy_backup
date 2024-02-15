import math

class bullet:
    def __init__(self):
        self.x = -10
        self.y = -10
        self.angle = 0
        self.speed = 0
        self.size = 0
        self.kind = ""
        self.lost = False
        self.target = 0

    def update(self):
        self.x += math.cos(self.angle*(math.pi/180.0))*self.speed
        self.y += math.sin(self.angle*(math.pi/180.0))*self.speed
