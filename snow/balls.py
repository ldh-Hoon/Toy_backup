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
        global mx, my
        
        self.x += self.dx
        self.y += self.dy
        self.dx *= 0.8
        self.dy *= 0.8
        self.dy += 0.01
        d = math.sqrt((mx - self.x)**2 + (my  - self.y)**2)
        if d<500 and d!=0:
            self.dx -= 100*(mx - self.x)/((d)**2)
            self.dy -= 100*(my - self.y)/((d)**2)
        if self.x < 0:
            self.x = 0
            self.dx *= 0.8
        if self.x > screensize[0]:
            self.x = screensize[0]
            self.dx *= 0.8
        if self.y < 0:
            self.y = 0
            self.dy *= 0.8
        if self.y > screensize[1]:
            self.y = screensize[1]
            self.dy *= 0.8
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

for i in range(100):
    s = snow()
    s.x = random.randint(1, screensize[0])
    s.y = random.randint(1, screensize[1])

    s.z = random.random()
    s.size = random.randint(1, 5)

    s.r = 255 - random.randint(1, 100)
    s.g = 255 - random.randint(1, 100)
    s.b = 255 - random.randint(1, 100)

    particle.append(s)

def draw():
    for s in particle:
        s.update()
        pygame.draw.circle(screen, s.get_color(), (s.x, s.y), s.size)

def block():
    for i in range(len(particle)):
        for j in range(i, len(particle)):
            d = math.sqrt((particle[i].x - particle[j].x)**2 + (particle[i].y - particle[j].y)**2)
            if d!=0:
                if d<2*(particle[j].size+particle[i].size):
                    temp = particle[j].dx
                    particle[j].dx = particle[i].dx
                    particle[i].dx = temp

                    temp = particle[j].dy
                    particle[j].dy = particle[i].dy
                    particle[i].dy = temp

                    particle[j].dx -= 5*(particle[i].x - particle[j].x)/((d)**2)
                    particle[j].dy -= 5*(particle[i].y - particle[j].y)/((d)**2)

                    particle[i].dx -= 5*(particle[j].x - particle[i].x)/((d)**2)
                    particle[i].dy -= 5*(particle[j].y - particle[i].y)/((d)**2)


                else:
                    particle[j].dx += 1*(particle[i].x - particle[j].x)/((d)**2)
                    particle[j].dy += 1*(particle[i].y - particle[j].y)/((d)**2)

                    particle[i].dx += 1*(particle[j].x - particle[i].x)/((d)**2)
                    particle[i].dy += 1*(particle[j].y - particle[i].y)/((d)**2)

# loop
while True:
    screen.fill(fuchsia)
    screen.blit(sub_screen, (0, 0))
    mx, my = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if h.quit:
        break

            
    draw()
    block()

    time.sleep(0.01)
    pygame.display.update()    

