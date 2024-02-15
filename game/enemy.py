import math


class enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 100
        self.angle = 90
        self.speed = 10
        self.kind = ""
        self.attackcount = 100

        self.debuff = ""

    def update(self):
        self.x += math.cos(self.angle*(math.pi/180.0))*self.speed
        self.y += math.sin(self.angle*(math.pi/180.0))*self.speed


