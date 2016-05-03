# -*- coding: utf-8 -*-

from Tkinter import *
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE
from subprocess import call
from tkFileDialog import askopenfilename
import os
import VirtualMachine as VM

fileName = "./default.txt"
data = ""

def delprof():
	Popen(["cmd.exe"], creationflags=CREATE_NEW_CONSOLE)
	call(['python', '-i', 'VirtualMachine.py'] )

def executeFile():
	global fileName
	#delprof()
	saveFile()

	VM.run(fileName)

def saveFile():
	global fileName

	data = T.get("1.0", 'end-1c')

	data_file = open(fileName, 'w')
	data_file.write(data)
	data_file.close()

def loadFile():
	global data
	global fileName

	#Tk().withdraw()
	data_file = open(askopenfilename())

	fileName = data_file.name
	#print(fileName)
	root.wm_title("CT - " + data_file.name)

	data = data_file.read()
	data_file.close()

	T.pack()
	T.insert("1.0", data)

root = Tk()
root.wm_title("CT")

S = Scrollbar(root)
T = Text(root, height = 30, width = 100)

executebutton = Button(root, text = 'Execute', width = 15, command = executeFile)
saveButton = Button(root, text = 'Save', width = 15, command = saveFile)
loadButton = Button(root, text = 'Load', width = 15, command = loadFile)

executebutton.pack()
saveButton.pack()
loadButton.pack()

S.pack(side = RIGHT, fill = Y)
T.pack(side = LEFT, fill = Y)
S.config(command = T.yview)
T.config(yscrollcommand = S.set)

root.mainloop()