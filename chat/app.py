from flask import Flask, render_template, request, redirect

#Flask 객체 인스턴스 생성
app = Flask(__name__)

history = ""

@app.route('/') # 접속하는 url
def index(text = None):
    return render_template("page.html", text=history.replace('\n', '<br>'))

@app.route('/chat', methods=['GET'])
def chat(text = None):
    global history
    temp = request.args.get('input_text')
    history += f"{temp}\n"

    return redirect('/')

if __name__=="__main__":
  app.run()

