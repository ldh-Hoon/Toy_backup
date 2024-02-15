import pygame
import win32api
import win32con
import win32gui
import ctypes

from PIL import Image
import threading
import keyboard


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

# PIL 이미지 pygame이미지로 변환
def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

#글씨용 폰트
myFont = pygame.font.SysFont("malgungothic", 14)



# 키보드 후킹
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
h = Hook()
h.start()

while not done:
    screen.fill(fuchsia) # 투명 칠하기
        
    if h.quit == True:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    
    # 화면 업데이트
    

    pygame.display.update()    
    #time.sleep(0.05)

quit(0)
