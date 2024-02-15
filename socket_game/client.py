## CLIENT ##

import socket
from _thread import *

import pygame, time, json, os
import win32api
import win32con
import win32gui
import ctypes
import requests
from io import BytesIO
from PIL import Image
import threading
import keyboard

print("ip:\n")
HOST = input()
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("\nname:\n")
name = input()
print("\n")
user_data = dict()
past_data = dict()
nowx = 100
nowy = 100
user_chat = dict()
livemax = 70


class Hook(threading.Thread):
    def __init__(self):
        super(Hook, self).__init__()
        self.daemon = True
        self.quit = False
        
        keyboard.unhook_all()

        
    def run(self):
        global mode, message
        while True:
            key = keyboard.read_hotkey(suppress=False)
            if key == 'esc':
                self.quit = True

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

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

url = "https://raw.githubusercontent.com/ldh-Hoon/ScreenPet/main/penguin.png"

# request.get 요청
res = requests.get(url)

img_p = Image.open(BytesIO(res.content)).convert('RGBA')
#image = Image.open("image/penguin.png").convert('RGBA')
img_p = img_p.resize((img_p.width//2, img_p.height//2))
        
img1 = pilImageToSurface(img_p.crop((0, 0, 64, 64)))
img2 = pilImageToSurface(img_p.crop((64, 0, 128, 64)))

h = Hook()
h.start()

myFont = pygame.font.SysFont("malgungothic", 14)



def recv_data(client_socket):
    global user_data, livemax
    while True:
        data = client_socket.recv(1024)
        if data.decode().split("###")[0] == "chat":
            user_chat[data.decode().split("###")[1]] = {"text":data.decode().split("###")[2], "live":livemax}
        else:
            user_data = json.loads(data.decode().replace("'", "\""))
            
start_new_thread(recv_data, (client_socket,))
client_socket.send((f"init###{name}").encode())

def draw():
    global user_data, past_data
    for u in user_data:
        screen.blit(img1, (user_data[u][0], user_data[u][1]))
             
message = ""

count = 0


def chat():
    global livemax
    while True:
        text = input()
        client_socket.send(f"chat###{name}###{text}".encode())
        user_chat[name] = {"text":text, "live":livemax}

thread = threading.Thread(target=chat)
thread.daemon = True
thread.start()

def update():
    for name in user_chat.keys():
        user_chat[name]['live'] -= 1
        if user_chat[name]['live'] < 0:
            del user_chat[name]
            break
        l = len(name+user_chat[name]['text'])*15
        pygame.draw.rect(screen, (255, 255, 255), (user_data[name][0]-15, user_data[name][1]-20, l+25, 18))
        text_Title= myFont.render(f"{name} : {user_chat[name]['text']}", True, (25, 0, 0))
        screen.blit(text_Title, (user_data[name][0], user_data[name][1]-20))

while not done:
    screen.fill(fuchsia)
    if keyboard.is_pressed('left'):
        nowx -= 10
        if nowx < 20:
            nowx = 20
    if keyboard.is_pressed('right'):
        nowx += 10
        if nowx > 1000:
            nowx = 1000
    if keyboard.is_pressed('up'):
        nowy -= 10
        if nowy < 20:
            nowy = 20
    if keyboard.is_pressed('down'):
        nowy += 10
        if nowy > 1000:
            nowy = 1000
        
    if h.quit == True:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if message == 'quit':
        close_data = message
        break

    
    # 화면 업데이트
    
    if len(user_data)!=0:
        draw()
        update()

    pygame.display.update()    
    time.sleep(0.05)
    count += 1
    if count > 20:
        client_socket.send("none".encode())
        count = 0
    client_socket.send(f"move###{name}###{nowx}###{nowy}".encode())

client_socket.close()
quit(0)