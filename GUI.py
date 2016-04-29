# -*- coding: utf-8 -*-

from Tkinter import * 
from Tkinter import Tk
from sys import executable
# from subprocess import Popen, CREATE_NEW_CONSOLE
from subprocess import call
from tkFileDialog import askopenfilename
import os
import VirtualMachine as VM

fileName = ""
data = ""

# def delprof(): Popen(["cmd.exe"], creationflags=CREATE_NEW_CONSOLE)

def executeFile():
	global fileName

	saveFile()

	VM.run(fileName)

def saveFile():
	global fileName

	data = T.get('1.0', END)

	data_file = open(fileName, 'w')
	data_file.write(data)
	data_file.close()

def loadFile():
	global data
	global fileName

	Tk().withdraw()
	data_file = open(askopenfilename())
	fileName = data_file.name

	root.wm_title("CT - " + data_file.name)

	data = data_file.read()
	data_file.close()

	T.delete('1.0', END)
	T.insert(END, data)

root = Tk()
root.wm_title("CT")

S = Scrollbar(root)
T = Text(root, height = 30, width = 100)

button = Button(root, text = 'Execute', width = 25, command = executeFile)
button2 = Button(root, text = 'Save', width = 25, command = saveFile)
button3 = Button(root, text = 'Load', width = 25, command = loadFile)
button.pack()
button2.pack()
button3.pack()

S.pack(side = RIGHT, fill = Y)
T.pack(side = LEFT, fill = Y)
S.config(command = T.yview)
T.config(yscrollcommand = S.set)

root.mainloop()
