import requests, sys, os
import tkinter
import json, datetime
import threading
import aiohttp
import asyncio
import time as tm

#pip install aiohttp 

add = dict()
add['chat'] = ""
add['register'] = "_2"
add["login"] = "_1"
add["get"] = "_3"
add["live"] = "_4"

url = "https://ldhldh-rest-api.hf.space/run/predict"
#url = input()

win_connect = tkinter.Tk()
win_connect.title("name")


name = ""
pw = 1234

def window_input_close(event=None):
    print("윈도우 종료")
    win_connect.destroy()
    sys.exit(1)

def connect(event=None):
    global name
    name = input_addr_string.get()
    win_connect.destroy()

tkinter.Label(win_connect, text="name").grid(row=0, column=0)
input_addr_string = tkinter.StringVar(value="user1")
input_addr = tkinter.Entry(win_connect, textvariable=input_addr_string, width=20)
input_addr.grid(row=0, column=1, padx=5, pady=5)
connect_button = tkinter.Button(win_connect, text="접속하기",  command=connect)
connect_button.grid(row=0, column=2, padx=5, pady=5)

width = 280
height = 40

screen_width = win_connect.winfo_screenwidth()
screen_height = win_connect.winfo_screenheight()

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))
win_connect.geometry('%dx%d+%d+%d' % (width, height, x, y))
input_addr.focus()


win_connect.protocol("WM_DELETE_WINDOW", window_input_close)

win_connect.mainloop()

try:
    response = requests.post(url+add['register'], json={
    "data": [
        f"{name}",
        f"{pw}",
    ]}).json()
    data = response["data"][0]

    response = requests.post(url+add['login'], json={
    "data": [
        f"{name}",
        f"{pw}",
    ]}).json()

    data = response["data"][0]
    if data == "fail":
        print("login error")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print("Error occurred: ", e)
    sys.exit(1)

live_users = ""


async def fetch(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200: # 요청 성공
                print('결과:', await response.text()) # await 주의
            else: # 요청 실패
                print('실패 상태 코드:', response.status)
async def live_call():
    global live_users
    async with aiohttp.ClientSession() as session:
        async with session.post(url+add['live'], json={"data": [f"{name}"]}, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200: # 요청 성공
                text = await response.text()
                live_data = json.loads(text)["data"][0]
                live_users = live_data.replace("dict_keys", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("(", "").replace("[", "").replace("]", "").replace("\"", "").replace("\'", "")
            else: # 요청 실패
                print('live 실패 상태 코드:', response.status)

async def get_message():
    async with aiohttp.ClientSession() as session:
        async with session.post(url+add['get'], json={"data": [f"{name}"]}, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200: # 요청 성공
                text = await response.text()
                data = json.loads(text)["data"][0]
                chat_list.delete(0, tkinter.END)
                chat_list.insert(tkinter.END, "live users : " + live_users)
                chat_list.insert(tkinter.END, "_________________________")
                data = json.loads(data.replace("'", "\""))
                for d in data:
                    msg = f"[{d['time'].split(':', 1)[1]}]{d['name']} : {d['text']}"
                    chat_list.insert(tkinter.END, msg)
                
                chat_list.see(tkinter.END)
            
            else: # 요청 실패
                print('get 실패 상태 코드:', response.status)

def send_message(text):
    asyncio.run(send(text))

async def send(text):
    t = datetime.datetime.now().strftime("Time: %H:%M:%S")
    text = inputbox.get()
    inputbox.delete(0, tkinter.END)
    async with aiohttp.ClientSession() as session:
        async with session.post(url+add['chat'], json={"data": [name, text, t]}, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200: # 요청 성공
                text = await response.text()
                data = json.loads(text)["data"][0]
            else: # 요청 실패
                print('get 실패 상태 코드:', response.status)

window = tkinter.Tk()
window.title("채팅 클라이언트")
frame = tkinter.Frame(window)
scroll = tkinter.Scrollbar(frame)
scroll.pack(side = tkinter.RIGHT, fill=tkinter.Y)
chat_list = tkinter.Listbox(frame, height=15, width=100, yscrollcommand=scroll.set)
chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)
frame.pack()

input_msg = tkinter.StringVar()
inputbox = tkinter.Entry(window, textvariable=input_msg)
inputbox.bind("<Return>", send_message)
inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)
send_button = tkinter.Button(window, text="전송", command=send_message)
send_button.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)

width = 500
height = 300

x = int((2000 / 2) - (width / 2))
y = int((1000 / 2) - (height / 2))

window.geometry('%dx%d+%d+%d' % (width, height, x, y))

lab = tkinter.Label(window)
lab.pack()
def clock():
    while True:

        t = datetime.datetime.now().strftime("Time: %H:%M:%S")
        asyncio.run(get_message())
        asyncio.run(live_call())
        lab.config(text=t)
        tm.sleep(0.1)
    #lab['text'] = time    
# run first time

def startThread(d):
    thread = threading.Thread(target=d)
    thread.daemon = True
    thread.start()

startThread(clock)
startThread(window.mainloop())

