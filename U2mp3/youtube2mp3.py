# call lib
import tkinter
import tkinter.font
from tkinter import *
from tkinter import messagebox
from pytube import YouTube
import glob
import os.path

import pytube
import inspect
print(inspect.getfile(pytube))

# set
root = Tk()
root.title("converter")
root.geometry("500x300")
root.resizable(False, False)
font=tkinter.font.Font(family="맑은 고딕", size=16, slant="italic")


#convert
def convert():
	#유튜브 전용 인스턴스 생성
	par = lnk.get()
	print(par)

	yt = YouTube(par)

	print("start!")
	yt.streams.filter(only_audio=True).first().download()

	files = glob.glob("*.mp4")
	for x in files:
		if not os.path.isdir(x):
			filename = os.path.splitext(x)
			try:
				os.rename(x,filename[0] + '.mp3')
			except:
				pass

	messagebox.showinfo("success","converted!")

def open_folder():
	path = os.path.realpath(os.getcwd())
	os.startfile(path)
	
#main
lbl = Label(root, text="YouTube Converter!", font=font)
lbl.pack()

lbl = Label(root, text="URL")
lbl.pack()

lnk = Entry(root)
lnk.configure(font=font)
lnk.pack(fill="x")

st = StringVar() 

place = Label(root, text="\n")
place.pack()

btn = Button(root, text="convert",command=convert)
btn.pack()

btn2 = Button(root, text="open folder",command=open_folder)
btn2.pack()
root.mainloop()