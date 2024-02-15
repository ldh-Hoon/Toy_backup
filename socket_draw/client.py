## CLIENT ##

import socket
from _thread import *

import threading, json
import time

print("ip:\n")
HOST = input()
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("\nname:\n")
name = input()
print("\n")
total_data = []
user_data = dict()

mode = 0

def recv_data(client_socket):
    time.sleep(2)
    global user_data, total_data, app, title
    if mode == 0:
        title["text"] = "draw board"
    while True:
        try:
            data = client_socket.recv(1024)
            data = json.loads(data.decode().replace("'", "\""))
            if data["type"] == "draw":
                app.canvas.create_line(int(data["start"]["x"]),int(data["start"]["y"]),
                                    int(data["end"]["x"]),int(data["end"]["y"]))
            elif data["type"] == "total":
                for dd in range(len(data["data"])):
                    app.draw_line(int(data["data"][f"{dd}"]["start"]["x"]),int(data["data"][f"{dd}"]["start"]["y"]),
                                    int(data["data"][f"{dd}"]["end"]["x"]),int(data["data"][f"{dd}"]["end"]["y"]))
            elif data["type"] == "chat":
                chat_update(data['name'], data['data'])           

        except:
            continue
        

start_new_thread(recv_data, (client_socket,))
client_socket.send(str({"type":"init", "name":name}).encode())


import tkinter as tk
import tkinter.font
from tkinter import *
from tkinter import messagebox

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 그리기 영역 생성
        self.canvas = tk.Canvas(root, bg="white", width=1000, height=400)
        self.canvas.pack()

        # 도구 선택 영역 생성
        self.tool_frame = tk.Frame(root, bg="white")
        self.tool_frame.pack(pady=10)

        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 현재 그리기 정보
        self.past_x, self.past_y = None, None
        self.current_shape = None


    def draw_line(self, a, b, c, d):
        self.canvas.create_line(a, b, c, d)

    def start_draw(self, event):
        self.past_x, self.past_y = event.x, event.y

    def on_draw(self, event):
        if self.past_x and self.past_y:
            self.canvas.create_line(self.past_x, self.past_y, event.x, event.y)
            client_socket.send(str({"type":"draw", 
                                    "name":name,
                                    "start":{"x":self.past_x,"y":self.past_y},
                                    "end":{"x":event.x,"y":event.y}}).encode())
            self.past_x = event.x
            self.past_y = event.y
            time.sleep(0.01)

    def end_draw(self, event):
        self.start_x, self.start_y = None, None
chat_count = 0
def chat_update(name, text):
    global chat_count
    chat_list.insert(tkinter.END, f"{name} : {text}")            
    chat_list.see(tkinter.END)
    chat_count += 1
    if chat_count>9:
        chat_list.delete("0", "1") 
        chat_count -= 2

def ans():
    ans = lnk.get()
    lnk.delete("0", "end")
    client_socket.send(str({"type":"chat", "name":name,"data":ans}).encode())
    chat_update(name, ans)
root = tk.Tk()
title = tk.Label(root, text="chat and draw")
title.pack()

app = PaintApp(root)
font=tk.font.Font(family="맑은 고딕", size=16, slant="italic")

frame = tkinter.Frame(root)
scroll = tkinter.Scrollbar(frame)
scroll.pack(side = tkinter.RIGHT, fill=tkinter.Y)
chat_list = tkinter.Listbox(frame, height=15, width=60, yscrollcommand=scroll.set)
chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)
frame.pack()

lbl = tk.Label(root, text="정답 입력")
lbl.pack()

lnk = tk.Entry(root)
lnk.configure(font=font)
lnk.pack(fill="x")

btn = Button(root, text="확인",command=ans)
btn.pack(fill="x")

root.mainloop()


# 종료
client_socket.close()
quit(0)