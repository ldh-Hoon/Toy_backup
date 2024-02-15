import math

class player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 100
        self.sp = 100
        self.maxhp = 100
        self.naxsp = 100
        self.atkspeed = 10
        self.speed = 5
        self.skill = "red"
        self.level = 1
        self.subskill = "none"
        self.kind = "player"
        self.angle = 0
        self.damage = 10
        self.hitted = 0

    def update(self):
        self.x += math.cos(self.angle*(math.pi/180.0))*self.speed
        self.y += math.sin(self.angle*(math.pi/180.0))*self.speed




