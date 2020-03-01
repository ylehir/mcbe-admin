
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

class Gui(object):

	def __init__(self):
		self.root = Tk()
		self.worldDir = None
		self.scanSpawn = IntVar()
		self.scanHSA   = IntVar()
		self.worldPath = StringVar()
		self.worldButton = Button(text="Select World", command=self.browseButton)
		self.worldButton.grid(row=0, column=0)
		self.worldLabel = Label(master=self.root,textvariable=self.worldPath)
		self.worldLabel.grid(row=0, column=1)
		self.spawnerButton = Checkbutton(self.root, text="Scan spawners", variable = self.scanSpawn)
		self.spawnerButton.grid(row=1,column=0)
		self.hsaButton = Checkbutton(self.root, text="Scan HSA", variable=self.scanHSA)
		self.hsaButton.grid(row=1,column=1)
		self.scanButton = Button(text="Scan", command=self.scan)
		self.scanButton.grid(row=2,column=0, columnspan=2, sticky=N+S+E+W)

	def scan(self):
		print("Starting scan : spawner :%s hsa : %s"%(self.scanSpawn.get(), self.scanHSA.get()) )

	def browseButton(self):
		self.worldDir = filedialog.askdirectory(title="Select World", initialdir=r"%s\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds"%(os.environ['LOCALAPPDATA']))
		self.worldPath.set(self.worldDir)

def mainGui():
	g = Gui()
	mainloop()

#	print(filepath)



if __name__ == '__main__' :
	setLdb()
	mainGui()
