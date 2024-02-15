import requests
import pygame, os
import win32api
import win32con
import win32gui
import ctypes

from io import BytesIO
from PIL import Image
import time, threading, random
import keyboard
import pyautogui
import numpy as np
import math

mx, my = pyautogui.position()
delta = 2
mode = 0
class dot():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        self.r = 0
        self.g = 0
        self.b = 0
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0
        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0

    def update(self):
        global mode, mx, my

        if mode!=4:
            self.x += self.dx
            self.y += self.dy
            self.z += self.dz

        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)

        self.rx *= 0.9
        self.ry *= 0.9
        self.rz *= 0.9
        
        if abs(self.tx-self.x)<0.5:
            self.x = self.tx
        if abs(self.ty-self.y)<0.5:
            self.y = self.ty
        if abs(self.tz-self.z)<0.5:
            self.z = self.tz

        if mode == 0:
            self.dx *= 0.95
            self.dy *= 0.95
            self.dz *= 0.95

            self.dx += random.random() - 0.5
            self.dy += random.random() - 0.5
        elif mode == 1:
            self.dx *= 0.99
            self.dy *= 0.99
            self.dz *= 0.99

        elif mode == 2:
            self.dx *= 0.95
            self.dy *= 0.95
            self.dz *= 0.95

            self.dx += (self.tx - self.x)/200.0
            self.dy += (self.ty - self.y)/200.0
            self.dz += (self.tz - self.z)/200.0

            d = math.sqrt((mx - screensize[0]//2 - self.x)**2 + (my - screensize[1]//2 - self.y)**2)
            if d<3000:
                self.dx -= 20*(mx - screensize[0]//2- self.x)/((d+0.1)**2)
                self.dy -= 20*(my - screensize[1]//2- self.y)/((d+0.1)**2)
        elif mode == 3:
            self.dx *= 0.95
            self.dy *= 0.95
            self.dz *= 0.95

            d = math.sqrt((mx - screensize[0]//2 - self.x)**2 + (my - screensize[1]//2 - self.y)**2)
            if d<100 and d!=0:
                self.dx -= 100*(mx- screensize[0]//2 - self.x)/((d)**2)
                self.dy -= 100*(my- screensize[1]//2 - self.y)/((d)**2)
        elif mode == 4:
            self.dx *= 0.99
            self.dy *= 0.99
            self.dz *= 0.99
            
            self.ry = -(10*(screensize[0]//2 - mx)/screensize[0] - self.rx)/5.0
            self.rx = (10*(screensize[1]//2 - my)/screensize[1] - self.ry)/5.0
            self.rz = 0

    def get_color(self):
        return (self.r, self.g, self.b)
    def get_pos(self):
        tempx  = self.x*math.cos(self.ry)*math.cos(self.rz) - self.y*math.cos(self.ry)*math.sin(self.rz)+ self.z*math.sin(self.ry)
        tempy = self.x*(math.cos(self.rx)*math.sin(self.rz) + math.sin(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + self.y*(math.cos(self.rx)*math.cos(self.rz)- math.sin(self.rx)*math.sin(self.ry)*math.sin(self.rz)) - self.z*math.sin(self.rx)*math.cos(self.ry)
        tempz = self.x*(math.sin(self.rx)*math.sin(self.rz)-math.cos(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + self.y*(math.sin(self.rx)*math.cos(self.rz) + math.cos(self.rx)*math.sin(self.ry)*math.sin(self.rz)) + self.z*math.cos(self.rx)*math.cos(self.ry)
        
        tempx = tempx / (1 + (129 + tempz)/1000)
        tempy = tempy / (1 + (129 + tempz)/1000)
        return (tempx, tempy, tempz)
    def get_pos_2d(self):
        tempx  = self.x*math.cos(self.ry)*math.cos(self.rz) - self.y*math.cos(self.ry)*math.sin(self.rz)+ self.z*math.sin(self.ry)
        tempy = self.x*(math.cos(self.rx)*math.sin(self.rz) + math.sin(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + self.y*(math.cos(self.rx)*math.cos(self.rz)- math.sin(self.rx)*math.sin(self.ry)*math.sin(self.rz)) - self.z*math.sin(self.rx)*math.cos(self.ry)
        tempz = self.x*(math.sin(self.rx)*math.sin(self.rz)-math.cos(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + self.y*(math.sin(self.rx)*math.cos(self.rz) + math.cos(self.rx)*math.sin(self.ry)*math.sin(self.rz)) + self.z*math.cos(self.rx)*math.cos(self.ry)
        
        tempx = tempx / (1 + (129 + tempz)/1200)
        tempy = tempy / (1 + (129 + tempz)/1200)
        xx = tempx + screensize[0]//2
        yy = tempy + screensize[1]//2
        return int(xx), int(yy)
class Hook(threading.Thread):
    def __init__(self):
        super(Hook, self).__init__()
        self.daemon = True
        self.add = False
        
        keyboard.unhook_all()
        keyboard.add_hotkey('f4', print, args=['\nf4 was pressed'])
        
    def run(self):
        global mode
        while True:
            key = keyboard.read_hotkey(suppress=False)
            if key == 'f4':
                mode += 1
                if mode >4:
                    mode = 0
                self.add = True

h = Hook()
h.start()


pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
screen = pygame.display.set_mode(screensize, pygame.NOFRAME)
done = False
fuchsia = (100, 100, 100)  # Transparency color
dark_red = (139, 0, 0)


win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

url = "https://www.adobe.com/content/dam/cc/us/en/creative-cloud/photography/discover/landscape-photography/CODERED_B1_landscape_P2d_714x348.jpg.img.jpg"

# request.get 요청
res = requests.get(url)

base = Image.open(BytesIO(res.content)).convert('RGB')
#image = Image.open("image/penguin.png").convert('RGBA')
base = base.resize((base.width//4, base.height//4))

pixels = base.load() # this is not a list, nor is it list()'able
width, height = base.size

dots = []
for x in range(width):
    for y in range(height):
        new_dot = dot()
        new_dot.x = random.randint(0, screensize[0])-screensize[0]//2
        new_dot.y = random.randint(0, screensize[1])-screensize[1]//2
        new_dot.z = 2*(new_dot.b-128)
        new_dot.tx = (x-width//2)*delta
        new_dot.ty = (y-height//2)*delta
        new_dot.tz = 3.0*(new_dot.b-128)

        new_dot.dx = random.random()*2-1
        new_dot.dy = random.random()*2-1
        new_dot.dz = random.random()*2-1

        new_dot.r, new_dot.g, new_dot.b = pixels[x, y]
        dots.append(new_dot)


while not done:
    screen.fill(fuchsia)
    mx, my = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    for d in dots:
        pygame.draw.circle(screen, d.get_color(), d.get_pos_2d(), delta//2)
        d.update()
    # 화면 업데이트
    pygame.display.update()    
    time.sleep(0.01)
    print("\r", end="")
