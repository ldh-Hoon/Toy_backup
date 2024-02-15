## SERVER ##

import socket
import json
from _thread import *
import time

client_sockets = []

## Server IP and Port ##

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

########## processing in thread ##
## new client, new thread ##

total_data = []
# {"start":{"x":1, "y":1},"end":{"x":2,"y":2}}

user_data = dict()

name_ip = dict()

def threaded(client_socket, addr):
    global user_data, client_sockets
    print('>> Connected by :', addr[0], ':', addr[1])
    ## process until client disconnect ##
    while True:
        try:
            time.sleep(0.01)
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by (not data)' + addr[0], ':', addr[1])
                del user_data[name_ip[addr[0]+str(addr[1])]]
                break

            else:
                json_data = json.loads(data.decode().replace("'", "\""))
                if json_data["type"] == "draw":
                    name = json_data["name"]
                    
                    px = json_data["start"]["x"]
                    py = json_data["start"]["y"]
                    tx = json_data["end"]["x"]
                    ty = json_data["end"]["y"]
                    total_data.append({"start":{"x":px, "y":py}, "end":{"x":tx, "y":ty}})
                    user_data[name] = {"x":tx, "y":ty}
                    for client in client_sockets:
                        if client != client_socket:
                            client.send(data)
                    continue
                elif json_data["type"] == "chat":
                    name = json_data["name"]
                    px = json_data["data"]
                    for client in client_sockets:
                        if client != client_socket:
                            client.send(data)
                    continue
                elif json_data["type"] == "init":
                    name = json_data["name"]
                    user_data[name] = {"x":0, "y":0}
                    name_ip[addr[0]+str(addr[1])] = name
                    if not len(total_data)==0:
                        temp = dict()
                        temp["type"] = "total"
                        temp["data"] = dict()
                        i = 0
                        for d in total_data:
                            temp["data"][f"{i}"] = d
                            i += 1
                            if i > 5:
                                client_socket.send(str(temp).encode())
                                time.sleep(0.1)
                                temp = dict()
                                temp["type"] = "total"
                                temp["data"] = dict()
                                i = 0
                        client_socket.send(str(temp).encode())
                    print(f">> {addr[0]} : {name} has init")
                elif json_data["type"] == "move":
                    name = json_data["name"]
                    tx = json_data["end"]["x"]
                    ty = json_data["end"]["y"]
                    user_data[name] = {"x":tx, "y":ty}
                    client_socket.send(str(user_data).encode())
                
        
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            if name_ip[addr[0]+str(addr[1])] in user_data:
                del user_data[name_ip[addr[0]+str(addr[1])]]
            if addr[0]+str(addr[1]) in name_ip:
                del name_ip[addr[0]+str(addr[1])]
            break
    
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))
    client_socket.close()

############# Create Socket and Bind ##

print('>> Server Start with ip :', HOST)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

############# Client Socket Accept ##

try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))

        
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()



