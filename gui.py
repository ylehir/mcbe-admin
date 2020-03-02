
import leveldb
import argparse
from leveldb import Row, setLdb, Key
from collections import namedtuple, defaultdict
from enum import Enum
from hsa import HSA,Position,HSAType
from spawner import findSpawners
import nbt
import io
import os
import sys
import datetime
from tkinter.filedialog import *
from tkinter import *
import multiprocessing
import threading

class StdoutRedirector(object):
	def __init__(self,textWidget):
		self.textSpace = textWidget
	
	def flush(self):
		return

	def write(self,string):
		self.textSpace.insert('end', string)
		self.textSpace.see('end')

class Gui(object):

	def __init__(self):
		self.root = Tk()
		self.root.grid_rowconfigure(0,weight=1)
		self.root.grid_columnconfigure(2,weight=1)
		self.worldDir = None
		self.scanSpawn = IntVar()
		self.scanHSA   = IntVar()
		self.nbProcess = IntVar()
		self.worldPath = StringVar()
		self.worldButton = Button(text="Select World", command=self.browseButton)
		self.worldButton.grid(row=0, column=0)
		self.worldLabel = Label(master=self.root,textvariable=self.worldPath)
		self.worldLabel.grid(row=0, column=1)
		self.spawnerButton = Checkbutton(self.root, text="Scan spawners", variable = self.scanSpawn)
		self.spawnerButton.grid(row=1,column=0)
		self.hsaButton = Checkbutton(self.root, text="Scan HSA", variable=self.scanHSA)
		self.hsaButton.grid(row=1,column=1)
		self.nbProcess = Scale(self.root, orient="horizontal", from_=1, to=multiprocessing.cpu_count(), resolution=1, label="Nb process", variable = self.nbProcess)
		self.nbProcess.set(multiprocessing.cpu_count())
		self.nbProcess.grid(row=2, column=0, columnspan=2, sticky=N+S+E+W)
		self.scanButton = Button(text="Scan", command=self.scan)
		self.scanButton.grid(row=3,column=0, columnspan=2, sticky=N+S+E+W)

		self.textBox = Text(self.root, wrap='word')
		self.textBox.grid(column=2, row=0, rowspan = 3, sticky='NSWE')
		sys.stdout = StdoutRedirector(self.textBox)

	def scan(self):
		import mcbeAdmin
		if not self.scanSpawn.get() and not  self.scanHSA.get() :
			return
		params = argparse.Namespace()
		params.worldBorders = None
		params.removeEntities = False
		params.pendingTicks = False
		params.compact = False
		params.world = self.worldDir
		params.dumpHSA = bool(self.scanHSA.get())
		params.findSpawners = bool(self.scanSpawn.get())
		params.nbProcess = self.nbProcess.get()
		scanner = threading.Thread(target=mcbeAdmin.main, args=(params,))
		scanner.start()

	def browseButton(self):
		self.worldDir = filedialog.askdirectory(title="Select World", initialdir=r"%s\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds"%(os.environ['LOCALAPPDATA']))
		worldName = self.worldDir
		with open(os.path.join(self.worldDir, "levelname.txt"), 'r') as worldNameFd :
			worldName = worldNameFd.read().strip()
		self.worldPath.set(worldName)

def mainGui():
	g = Gui()
	mainloop()

if __name__ == '__main__' :
	setLdb()
	mainGui()
