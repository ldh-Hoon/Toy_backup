from flask import Flask, jsonify
import datetime
from pyngrok import ngrok 

user_data = dict()
live_user = dict()
chat_history = []

def clear_data():
    global chat_history
    chat_history = []
    return "ok"

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello"

@app.route("/live")
def get_live_user():
    s = ",".join(live_user.keys())
    return s

@app.route("/get/<string:user>")
def get_data(user):
    global live_user
    for u in live_user.keys():
        if u == user:
            live_user[u] = 20
        else:
            live_user[u] -= 1
            if live_user[u] < 0:
                del live_user[u]
    return chat_history

@app.route("/chat/<string:name>/<string:text>")
def chat(name, text):
    global chat_history
    t = datetime.datetime.now().strftime("Time: %H:%M:%S")
    if not name in user_data:
        return "no id"
    else:
        chat_history.append({"name": name, "text":text, "time":t})
        if len(chat_history) > 20:
            del chat_history[0]
    return "ok"

@app.route("/login/<string:id>/<string:pw>")
def login(id, pw):
    global live_user
    if not id in user_data:
        return "fail"
    else:
        if user_data[id] != pw:
            return "fail"
        else:
            live_user[id] = 20
            return "ok"

@app.route("/register/<string:id>/<string:pw>")
def register(id, pw):
    global user_data
    if not id in user_data:
        user_data[id] = pw
        return "ok"
    else:
        return "fail"

if __name__ == '__main__':
    app.debug = True
    app.run()
