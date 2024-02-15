#https://337e6bd92485654abd.gradio.live

from gradio_client import Client

client = Client("https://337e6bd92485654abd.gradio.live/")
def chat(x):
    result = client.predict(
            f"{x}",	# str  in 'User input' Textbox component
            0.9,	# float (numeric value between 0.05 and 1.0) in 'Top-p (nucleus sampling)' Slider component
            30,	# float (numeric value between 5 and 100) in 'Top-k (nucleus sampling)' Slider component
            0.7,	# float (numeric value between 0.1 and 2.0) in 'Temperature' Slider component
            200,	# float (numeric value between 1 and 200) in 'Max New Tokens' Slider component
            1.1,	# float (numeric value between 1.0 and 3.0) in 'repetition_penalty' Slider component
            api_name="/gen"
    )
    return result

history = []

def make_form(history):
    out = ""
    for d in history:
        if out != "":
            out += "\n\n"
        if d['role']=="user":
            out += f"### 친구: {d['text']}"
        else:
            out += f"### 너: {d['text']}"
    return out

text = ""
text = input()
while text != "-1":
    history.append({"role":"user", "text":text})

    out = chat(make_form(history) + "\n\n### 너: ")
    history.append({"role":"bot", "text": out})
    print(out)
    text = input()