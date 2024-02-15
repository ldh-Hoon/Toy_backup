## SERVER ##

import socket
from _thread import *

client_sockets = []

## Server IP and Port ##

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

########## processing in thread ##
## new client, new thread ##

user_data = dict()
name_ip = dict()

def threaded(client_socket, addr):
    global user_data, client_sockets
    print('>> Connected by :', addr[0], ':', addr[1])

    ## process until client disconnect ##
    while True:
        try:
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by (not data)' + addr[0], ':', addr[1])
                del user_data[name_ip[addr[0]]]
                break

            else:
                if data.decode().split("###", 1)[0] == "chat":
                    print('>> Received from ' + addr[0], ':', addr[1], data.decode())
                    ## chat to client connecting client ##
                    ## chat to client connecting client except person sending message ##
                    for client in client_sockets:
                        if client != client_socket:
                            client.send(data)
                    continue
                elif data.decode().split("###", 1)[0] == "move":
                    name = data.decode().split("###")[1]
                    if len(data.decode().split("###"))>=4:
                        tx = int(data.decode().split("###")[2])
                        ty = int(data.decode().split("###")[3])
                        user_data[name] = [tx, ty]
                elif data.decode().split("###", 1)[0] == "init":
                    name = data.decode().split("###")[1]
                    user_data[name] = [100, 100]
                    name_ip[addr[0]] = name
                    print(f">> {addr[0]} : {name} has init")

                client_socket.send(str(user_data).encode())
                
        
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            if name_ip[addr[0]] in user_data:
                del user_data[name_ip[addr[0]]]
            if addr[0] in name_ip:
                del name_ip[addr[0]]
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
