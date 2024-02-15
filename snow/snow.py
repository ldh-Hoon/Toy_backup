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

wind = 0.0
mx, my = pyautogui.position()
level = 4
size = 1

pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
screen = pygame.display.set_mode(screensize, pygame.NOFRAME)
done = False
fuchsia = (100, 100, 100)  # Transparency color
dark_red = (139, 0, 0)

sub_screen = pygame.Surface(screensize)
sub_screen.fill(fuchsia)

win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

class snow:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.size = 2
        
        self.dx = 0.0
        self.dy = 0.0
        self.r = 255
        self.g = 255
        self.b = 255

        self.respone = 100
        self.stack = False

    def get_color(self):
        return (self.r, self.g, self.b)
    
    def update(self):
        global mx, my, line, size
        
        if self.stack == False:
            self.dx += random.random() - 0.5 + wind/(self.z*1.0)
            self.dy += random.random() - 0.5 

            self.dy = max(min(self.dy, 5), 1)
            self.dx = max(min(self.dx, 3), -3)
            
            self.x += self.dx + (screensize[0]//2-mx)/(200.0)
            self.y += self.dy + (my-300)/500.0

            if self.x < 0:
                self.x = screensize[0]
            if self.x > screensize[0]:
                self.x = 0
            if self.y > screensize[1]-level:
                self.stack = True
                self.respone = random.randint(300, 800)
                self.dx = 0
                self.dy = 0
                self.size = random.randint(5,30)
            
        if self.stack == True:
            self.respone -= 1
            if self.respone < 0:
                self.stack = False
                self.y = 0
                self.size = random.randint(1, 2)
            self.x += self.dx
            self.y += self.dy
            self.dx *= 0.95
            self.dy *= 0.95
            self.dy += (screensize[1]-10 - self.y)/1000.0 + 0.01
            d = math.sqrt((mx - self.x)**2 + (my  - self.y)**2)
            if d<100 and d!=0:
                self.dx -= 20*(mx - self.x)/((d)**2)
                self.dy -= 20*(my - self.y)/((d)**2)
            if d<10 and d!=0:
                self.stack = False
                self.y = 0
                self.size = random.randint(1, 2)
                size = min(size+0.01, 50)
            if self.x < 0:
                self.x = 0
            if self.x > screensize[0]:
                self.x = screensize[0]
            if self.y > screensize[1]-level:
                self.y = random.randint(screensize[1]-level-10, screensize[1]-level)
                self.dy *= -0.7
# hooking
        
class Hook(threading.Thread):
    def __init__(self):
        super(Hook, self).__init__()
        self.daemon = True
        self.quit = False
        
        keyboard.unhook_all()
        
    def run(self):
        while True:
            key = keyboard.read_hotkey(suppress=False)
            if key == 'f4':
                self.quit = True
            if key == 'esc':
                self.quit = True

h = Hook()
h.start()


# init
particle = []

for i in range(2000):
    s = snow()
    s.x = random.randint(1, screensize[0])
    s.y = random.randint(1, screensize[1])

    s.z = random.random()
    s.size = random.randint(1, 2)

    s.r = 255 - random.randint(1, 10)
    s.g = 255 - random.randint(1, 10)
    s.b = 255 - random.randint(1, 10)

    particle.append(s)
col = 1

def make_snow():
    global level
    if random.random()>0.9 and len(particle)<8000:
        s = snow()
        s.x = random.randint(1, screensize[0])
        s.y = 0

        s.z = random.random()
        s.size = random.randint(1, 2)

        if col == 1:
            s.r = 255 - random.randint(1, 10)
            s.g = 255 - random.randint(1, 10)
            s.b = 255 - random.randint(1, 10)
        else:
            s.r = random.randint(1, 10)
            s.g = random.randint(1, 10)
            s.b = random.randint(1, 10)

        particle.append(s)
    if random.random()>0.999:
        level += 1

def draw():
    for s in particle:
        s.update()
        pygame.draw.circle(screen, s.get_color(), (s.x, s.y), s.size)
        if s.stack==True and s.y>screensize[1]-level-3:
            pygame.draw.circle(sub_screen, s.get_color(), (s.x, s.y), s.size)
        pygame.draw.circle(screen, (255,255,255), (mx, my), size)
# loop
reverse = False
while True:
    screen.fill(fuchsia)
    screen.blit(sub_screen, (0, 0))
    mx, my = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if h.quit:
        break

    if level > screensize[1]-100:
        level = 2
        reverse = True
    
    if reverse == True:
        reverse = False
        if col == 0:
            col = 1
            for p in particle:
                p.r = 255
                p.g = 255
                p.b = 255
        else:
            col = 0
            for p in particle:
                p.r = 0
                p.g = 0
                p.b = 0
            
    draw()

    make_snow()
    pygame.display.update()    

