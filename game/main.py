import pygame, os, time, random
import win32api
import win32con
import win32gui
import ctypes
import requests
from io import BytesIO
from PIL import Image
import time, threading
import keyboard
import pyautogui

import enemy
import player
import item
import bullet


import math


score = 0
level = 1
gameover = False

def get_rad(a, t):
    angle = math.atan2(t.y-a.y, t.x-a.x)
    return angle
def get_dist(ax, ay, tx, ty):
    d = math.sqrt((ty-(ay))**2+ (tx-(ax))**2)
    return d

class Hook(threading.Thread):
    def __init__(self):
        super(Hook, self).__init__()
        self.daemon = True
        self.quit = False
        
        keyboard.unhook_all()

        
    def run(self):
        global p
        while True:
            key = keyboard.read_hotkey(suppress=False)
            if key == 'f4':
                self.quit = True
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

url = "https://raw.githubusercontent.com/ldh-Hoon/ScreenPet/main/p.png"

# request.get 요청
res = requests.get(url)

img_p = Image.open(BytesIO(res.content)).convert('RGBA')
#image = Image.open("image/penguin.png").convert('RGBA')
img_p = img_p.resize((img_p.width//20, img_p.height//20))
img_p = pilImageToSurface(img_p)


url = "https://raw.githubusercontent.com/ldh-Hoon/ScreenPet/main/e.png"

# request.get 요청
res = requests.get(url)

img_e = Image.open(BytesIO(res.content)).convert('RGBA')
#image = Image.open("image/penguin.png").convert('RGBA')
img_e = img_e.resize((img_e.width//3, img_e.height//3))
img_e = pilImageToSurface(img_e)

myFont = pygame.font.Font(None, 30)





object_list = []

p = player.player()
p.x = screensize[0]//2
p.y = screensize[1]//2
p.level = 1
p.atkspeed = 20
p.speed = 20
p.skill = "red"
object_list.append(p)
## init



h = Hook()
h.start()


## defs
def draw(screen, object_list):
    BLACK = ( 0, 0, 0 )

    text_Title= myFont.render(f"SCORE:{score}, LEVEL:{level}", True, BLACK)
    screen.blit(text_Title, (0, 0))


    for o in object_list:
        screen.blit(img_p, (o.x, o.y))
        text_hp= myFont.render(f"{p.hp}/{p.maxhp}", True, (90, 255, 100))
        screen.blit(text_hp, (p.x-10, p.y+40))
    for b in bullet_list:
        b.update()
        if b.kind == "player_b":
            if p.skill == "red":
                pygame.draw.circle(screen,(255, 100, 120), (b.x, b.y), 2)
            if p.skill == "blue":
                pygame.draw.circle(screen,(70, 70, 255), (b.x, b.y), 3)
            if p.skill == "purple":
                pygame.draw.circle(screen,(255, 20, 255), (b.x, b.y), 1)
                d = 1000
                if len(enemy_list)!=0:
                    for idx in range(len(enemy_list)):
                        td = get_dist(b.x, b.y, enemy_list[idx].x, enemy_list[idx].y)
                        if d>td:
                            d = td
                            b.target = idx
                if b.lost == False:
                    b.angle += ((180*math.atan2(enemy_list[b.target].y-b.y, enemy_list[b.target].x-b.x))/math.pi - b.angle)/3

                    

        elif b.kind == "enemy_b":
            pygame.draw.circle(screen,(255, 20, 20), (b.x, b.y), 4)
    for i in item_list:
        text_item= myFont.render(f"{i.kind}", True, (90, 255, 100))
        screen.blit(text_item, (i.x-20, i.y+40))
        if i.kind == "blue":
            pygame.draw.circle(screen, (0, 0, 255), (i.x, i.y), 20) 
        if i.kind == "red":
            pygame.draw.circle(screen, (255, 0, 5), (i.x, i.y), 20) 
        if i.kind == "purple":
            pygame.draw.circle(screen, (222, 0, 225), (i.x, i.y), 20) 
        if i.kind == "atkspeed":
            pygame.draw.circle(screen, (100, 200, 100), (i.x, i.y), 20) 
        if i.kind == "hp":
            pygame.draw.circle(screen, (200, 100, 100), (i.x, i.y), 20) 
        if i.kind == "speed":
            pygame.draw.circle(screen, (100, 100, 200), (i.x, i.y), 20) 
        if i.kind == "damage":
            pygame.draw.circle(screen, (155, 155, 155), (i.x, i.y), 20) 
        i.update()
    for e in enemy_list:
        screen.blit(img_e, (e.x, e.y))
        text_hp= myFont.render(f"{e.hp}", True, (255, 100, 100))
        screen.blit(text_hp, (e.x+35, e.y-10))
        e.update()
        e.attackcount -= 1 + level//10
        if e.attackcount<=0:
            enemy_atk(e.kind, e.x+20, e.y)
            if e.kind == "enemy1":
                e.attackcount = 100
            if e.kind == "enemy2":
                e.attackcount = 200 - level
            if e.kind == "enemy3":
                e.attackcount = max(50 - level, 30)
            if e.kind == "enemy4":
                e.attackcount = 200 - level
            if e.kind == "enemy5":
                e.attackcount = 200 - level
            if e.kind == "enemy6":
                e.attackcount = 30
        if e.kind == "enemy_follow" or e.kind == "enemy_follow2":
            if e.y < p.y:
                e.angle += ((180*math.atan2(p.y-e.y, p.x-e.x))/math.pi-e.angle)/5
            else:
                e.angle += (90 - e.angle)/10
        if e.y > screensize[1]:
            e.y = 0

item_list = []
def drop_item(x, y):
    print("make")
    i = item.item()
    i.x = x
    i.y = y
    kind = ["hp", "red", "blue", "purple", "speed", "damage", "atkspeed"]
    i.kind = random.choice(kind)
    item_list.append(i)




bullet_list = []
count = 0
max_num = 600
def counting():
    global count
    count += 1
    if count >= max_num:
        count = 0
for _ in range(max_num):
    b = bullet.bullet()
    bullet_list.append(b)
def make_bullet(name, x, y, angle, speed, kind):
    global count

    b = bullet_list[count]
    b.lost = False
    b.x = x
    b.y = y
    b.angle = angle
    b.speed = speed
    b.kind = kind
    counting()


enemy_list = []

def init_bullet(b):
    b.x = -10
    b.y = -10
    b.speed = 0


def make_enemy():
    m = enemy.enemy()
    m.y = 0
    m.x = random.randint(200, screensize[0]-200)
    m.hp = 10+level*10
    m.speed = level*1 + 1
    
    if random.random()>(0.8 - level/100):
        if random.random()>(0.5) and level>3:
            if random.random()>(0.5) and level>5:
                if random.random()>(0.5) and level>10:
                    if random.random()>(0.6) and level>15:
                        m.kind = "enemy6"
                        m.hp += 1000 + 500*level
                        m.speed = 1
                    else:
                        m.kind = "enemy5"
                        m.hp += 500 + 300*level
                        m.speed = 5
                else:
                    m.kind = "enemy4"
                    m.hp += 300 + 100*level
            else:
                m.kind = "enemy3"
                m.hp += 100 + 10*level
                if random.random()>0.9:
                    m.kind = "enemy_follow2"
                    m.speed = m.speed*2
        else:
            m.kind = "enemy2"
            m.hp += 5  + 20*level
            m.speed = 3
    else:
        m.kind = "enemy1"
        m.speed = 2
        if random.random()>0.8:
            m.kind = "enemy_follow"
            m.speed = 10
        

    enemy_list.append(m)

def enemy_atk(kind, x, y):
    if kind == "enemy1":
        make_bullet(kind, x + 20, y, 90, level*2+10, "enemy_b")
    if kind == "enemy2":
        make_bullet(kind, x + 20, y, 90, level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, 70, level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, 110, level*2+10, "enemy_b")

    if kind == "enemy3":
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi), 20, "enemy_b")
    if kind == "enemy4":
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)+10, level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi), level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)-10, level*2+10, "enemy_b")

    if kind == "enemy5":
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)+10, 20, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi), 20, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)+30, 20, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)-10, 20, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)-30, 20, "enemy_b")

    if kind == "enemy6":
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)+10,level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi), level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)+30, level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)-10, level*2+10, "enemy_b")
        make_bullet(kind, x + 20, y, ((180*math.atan2(p.y-y, p.x-x))/math.pi)-30, level*2+10, "enemy_b")

    
def hit_test():
    global gameover, score

    del_list = []
    n = 0
    for idx in range(len(enemy_list)):
        if abs(enemy_list[idx].x+40 - (p.x + 20))<30 and abs(enemy_list[idx].y+30 - (p.y+20))<30:
            if p.hitted<=0:
                p.hp -= 10
                p.hitted = 30

        for b in bullet_list:  
            if b.kind == "player_b":
                if abs(enemy_list[idx].x+40 - b.x)<40 and abs(enemy_list[idx].y+30 - b.y)<40:
                    init_bullet(b)
                    if p.skill == "purple":
                        enemy_list[idx].hp -= int(p.damage/10)+1
                    else:
                        enemy_list[idx].hp -= p.damage
                    if enemy_list[idx].hp <= 0:
                        for b in bullet_list:
                            if idx == b.target:
                                b.lost = True
                        del_list.append(idx)
                        score += level
                        if random.random()>0.6:
                            drop_item(enemy_list[idx].x, enemy_list[idx].y)
                        break
    del_list.sort()
    for idx in del_list:
        del enemy_list[idx-n]
        n += 1

    del_list = []
    for idx in range(len(item_list)):
        if abs(p.x+20 - item_list[idx].x)<20 and abs(p.y+20 - item_list[idx].y)<20:
            del_list.append(idx)
            if item_list[idx].kind == "red":
                if p.skill == "red":
                    p.level = min(p.level+1, 9)
                else:
                    p.skill = "red"
                    p.level = max(p.level - 2, 1)
            if item_list[idx].kind == "blue":
                if p.skill == "blue":
                    p.level = min(p.level+1, 9)
                else:
                    p.skill = "blue"
                    p.level = max(p.level - 2, 1)
            if item_list[idx].kind == "purple":
                if p.skill == "purple":
                    p.level = min(p.level+1, 9)
                else:
                    p.skill = "purple"
                    p.level = max(p.level - 2, 1)
            if item_list[idx].kind == "speed":
                p.speed = min(p.speed+5, 50)
            if item_list[idx].kind == "atkspeed":
                p.atkspeed = min(p.atkspeed+10, 500)
            if item_list[idx].kind == "damage":
                p.damage += 2
            if item_list[idx].kind == "hp":
                p.maxhp += 20
                p.hp = p.maxhp            

    del_list.sort()
    for idx in del_list:
        del item_list[idx-n]
        n += 1

    for b in bullet_list:
        if b.y<0 or b.y>screensize[1]:
            init_bullet(b)
        if b.kind == "enemy_b":
            if abs(p.x+20 - b.x)<30 and abs(p.y+20 - b.y)<30:
                init_bullet(b)
                p.hp -= 10
                if p.hp <= 0:
                    gameover = True
                    break

def atk():
    if p.skill == "purple":
        if p.level >= 1:
            make_bullet(p.kind, p.x + 20, p.y, -90, 20, "player_b")
        if p.level >= 2:
            make_bullet(p.kind, p.x + 20, p.y-5, -90, 20, "player_b")
        if p.level >= 3:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 25, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 25, "player_b")
        if p.level >= 4:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 26, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 26, "player_b")
        if p.level >= 5:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 27, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 27, "player_b")
        if p.level >= 6:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 28, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 28, "player_b")
        if p.level >= 7:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 29, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 29, "player_b")
        if p.level >= 8:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 30, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 30, "player_b")
        if p.level >= 9:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 31, "player_b")
                make_bullet(p.kind, p.x + 20, p.y-10, -90, 31, "player_b")

    if p.skill == "red":
        if p.level >= 1:
            make_bullet(p.kind, p.x + 20, p.y, -90, 50, "player_b")
        if p.level >= 2:
            make_bullet(p.kind, p.x + 10, p.y, -90, 50, "player_b")
            make_bullet(p.kind, p.x + 30, p.y, -90, 50, "player_b")
        if p.level >= 3:
            make_bullet(p.kind, p.x + 0, p.y, -91, 50, "player_b")
            make_bullet(p.kind, p.x + 40, p.y, -89, 50, "player_b")
        if p.level >= 4:
            make_bullet(p.kind, p.x - 10, p.y + 2, -95, 50, "player_b")
            make_bullet(p.kind, p.x + 50, p.y + 2, -85, 50, "player_b")
        if p.level >= 5:
            make_bullet(p.kind, p.x - 20, p.y+5, -100, 50, "player_b")
            make_bullet(p.kind, p.x + 60, p.y+5, -80, 50, "player_b")

            make_bullet(p.kind, p.x + 10, p.y + 30, -90, 50, "player_b")
            make_bullet(p.kind, p.x + 30, p.y + 30, -90, 50, "player_b")
        if p.level >= 6:
            make_bullet(p.kind, p.x - 30, p.y + 9, -110, 50, "player_b")
            make_bullet(p.kind, p.x + 70, p.y + 9, -70, 50, "player_b")

            make_bullet(p.kind, p.x + 0, p.y + 30, -91, 50, "player_b")
            make_bullet(p.kind, p.x + 40, p.y + 30, -89, 50, "player_b")
        if p.level >= 7:
            make_bullet(p.kind, p.x - 40, p.y+15, -120, 50, "player_b")
            make_bullet(p.kind, p.x + 80, p.y+15, -60, 50, "player_b")
        if p.level >= 8:
            make_bullet(p.kind, p.x - 50, p.y+24, -120, 50, "player_b")
            make_bullet(p.kind, p.x + 90, p.y+24, -60, 50, "player_b")
        if p.level >= 9:
            make_bullet(p.kind, p.x - 20, p.y+35, -100, 50, "player_b")
            make_bullet(p.kind, p.x + 60, p.y+35, -80, 50, "player_b")

            make_bullet(p.kind, p.x - 30, p.y + 37, -110, 50, "player_b")
            make_bullet(p.kind, p.x + 70, p.y + 37, -70, 50, "player_b")
    if p.skill == "blue":
        if p.level == 1:
            for i in range(2):
                make_bullet(p.kind, p.x + 20, p.y + i*5, -90, 50, "player_b")
        elif p.level == 2:
            for i in range(3):
                make_bullet(p.kind, p.x + 20, p.y + i*5, -90, 50, "player_b")
        elif p.level == 3:
            for i in range(4):
                make_bullet(p.kind, p.x + 0, p.y + i*6, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y + i*6, -90, 50, "player_b")
        elif p.level == 4:
            for i in range(5):
                make_bullet(p.kind, p.x + 0, p.y + -5+ i*7, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y + -5+ i*7, -90, 50, "player_b")
        elif p.level == 5:
            for i in range(6):
                make_bullet(p.kind, p.x + 40, p.y -10+ i*8, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 20, p.y -10+ i*8, -90, 50, "player_b")
        elif p.level == 6:
            for i in range(7):
                make_bullet(p.kind, p.x + 0, p.y -20+ i*8, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y -20+ i*8, -90, 50, "player_b")

                make_bullet(p.kind, p.x - 20, p.y -20+ i*8, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 60, p.y -20+ i*8, -90, 50, "player_b")
        elif p.level == 7:
            for i in range(8):
                make_bullet(p.kind, p.x + 0, p.y -20+ i*8, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y -20+ i*8, -90, 50, "player_b")

                make_bullet(p.kind, p.x - 20, p.y -20+ i*8, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 60, p.y -20+ i*8, -90, 50, "player_b")
        elif p.level == 8:
            for i in range(9):
                make_bullet(p.kind, p.x + 0, p.y -20+ i*9, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y -20+ i*9, -90, 50, "player_b")

                make_bullet(p.kind, p.x - 20, p.y -20+ i*9, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 60, p.y -20+ i*9, -90, 50, "player_b")
        elif p.level == 9:
            for i in range(11):
                make_bullet(p.kind, p.x + 0, p.y -20+ i*10, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 40, p.y -20+ i*10, -90, 50, "player_b")

                make_bullet(p.kind, p.x - 20, p.y -20+ i*10, -90, 50, "player_b")
                make_bullet(p.kind, p.x + 60, p.y -20+ i*10, -90, 50, "player_b")

## loop
atk_count = 0
while True:
    if score>(level*level)*10:
        level += 1
    p.hitted -= 1
    if p.hitted <= 0:
        p.hitted = 0
    atk_count += 1
    if atk_count > 1000/(50 + p.atkspeed):
        atk()
        atk_count = 0
        if p.skill == "blue":
            atk_count = -1000/(50 + p.atkspeed)
        if p.skill == "purple":
            atk_count = 1000/(50 + p.atkspeed) - 6
    if random.random()>(0.99 - level/500):
        make_enemy()
    if len(enemy_list)<5:
        if random.random()>(0.5):
            make_enemy()

    if h.quit:
        break
    if keyboard.is_pressed('left'):
        p.x -= p.speed
    if keyboard.is_pressed('right'):
        p.x += p.speed
    if keyboard.is_pressed('up'):
        p.y -= p.speed
    if keyboard.is_pressed('down'):
        p.y += p.speed

    screen.fill(fuchsia)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    draw(screen, object_list)
    hit_test()


    pygame.display.update()    
    time.sleep(0.05)