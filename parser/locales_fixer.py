#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7
import math
import sys, os
from os import remove, close, path, name
import re

# check dependent modules
from importlib import util

req_spec = util.find_spec("requests")
req_found = req_spec is not None
if (not req_found):
	print('"requests" module not found, install using the command "pip install requests"')
	sys.exit()

col_spec = util.find_spec("colorama")
col_found = col_spec is not None
if (not col_found):
	print('"colorama" module not found, install using the command "pip install colorama"')
	sys.exit()
# end check modules

class WindowsInhibitor:
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def Inhibit(self):
        import ctypes
        #print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def Uninhibit(self):
        import ctypes
        #print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)
	
class File():
	def __init__(self, path_):
		self.path = path_
		self.lines = 0
	
	def Exists(self):
		return os.path.isfile(self.path)

	def ReadFile(self):
		f = open(self.path, "r")
		contents = f.readlines()
		f.close()
		return contents

	def DeleteLine(self, lineNum):
		from tempfile import mkstemp
		from shutil import move
	
		while not self.CheckFileAccess():
			pass

		#Create temp file
		fh, abs_path = mkstemp()
		with open(abs_path,'w') as new_file:
			with open(self.path) as old_file:
			
				for lineno, line in enumerate(old_file, 1):
					if lineno != lineNum:
						new_file.write(line)
		close(fh)
		#Remove original file
		remove(self.path)
		#Move new file
		move(abs_path, self.path)
		
	def CheckFileAccess(self):
		if os.path.exists(self.path):
			try:
				os.rename(self.path, self.path)
				#print 'Access on file "' + self.path +'" is available!'
				return True
			except OSError as e:
				pass
				#print 'Access-error on file "' + self.path + '"! \n' + str(e)
		return False
	
	def GetNumberOfLines(self):
		f = open(self.path, 'r')
		lines = 0
		for line in f:
			lines += 1
		f.close()
		self.lines = lines
		return lines
	
class Parser():
	def __init__(self, args):
		from colorama import init
		init()
		
		#If Windows then prevent sleep
		self.osSleep = None
		if os.name == 'nt':
			self.osSleep = WindowsInhibitor()
			self.osSleep.Inhibit()
		
		# INIT
		print("--------------------------")
		print(" \033[33mItemNameLocalized Locales Fixer\033[0m")
		print("--------------------------")
		
		self.localesList = ["en_US","es_ES","es_MX","de_DE","fr_FR","it_IT","pt_BR","ru_RU","ko_KR","zh_TW"]
		self.currLocaleFile = None
		
		self.dbFile = File("IDs_list.txt")
		self.dbFile.GetNumberOfLines()
		
		self.removedLua = []
		self.processDuplicates = False
		
		#Check files
		if not self.dbFile.Exists():
			self.PrintError("E", 'File "IDs_list.txt" does not exist.')
			self.Exit()
		
		#Config
		if len(args) <= 1: 
			self.PrintArgs()
			self.Exit()
		else:
			self.Config(args)
	
		#Utils
		self.utils = Utils()
		self.utils.PlaySound(2000, 250, 1)
		
		#set cmd code page
		try:
			os.system("chcp 65001 > nul")
		except:
			pass

	def Exit(self):
		try:
			if self.osSleep:
				self.osSleep.Uninhibit()
			if self.Continue:
				print(self.Command)
				if self.Command != "":
					os.system(self.Command)
			else:
				sys.exit()
		except KeyboardInterrupt:
			sys.exit()
		except:
			sys.exit()
			raise
	
	def PrintArgs(self):
		print(" \033[31m/!\ ERROR\033[0m: No arguments: PLACEHOLDER")
		print("            PLACEHOLDER")
		print("--------------------------")
		
	''' def PrintConfig(self):
		print " Config:"
		print "\tLanguage: \033[36m%s\033[0m" % (self.currLocale)
		print "\tRange Start: \033[36m%i\033[0m" % (self.rangeStart)
		print "\tRange End: \033[36m%i\033[0m" % (self.rangeEnd)
		print "--------------------------"
	'''
	
	def PrintError(self, type, message):
		t = ""
		if type == "E":
			t = "\033[31m/!\\ ERROR\033[0m"
			self.utils.PlaySound(200, 200, 3)
		elif type == "W":
			t = "\033[33m/!\\ WARNING\033[0m"
			self.utils.PlaySound(200, 200, 2)
		print(" %s: %s" % (t, message))
		print("--------------------------")
	
	'''	def ReadAPIKey(self, apiKeyFile):
		if os.path.isfile(apiKeyFile):
			fa = open(apiKeyFile,'r')
			self.apiKey = fa.readline()
			fa.close()
	'''
	
	def Config(self, args):
		if len(args) >= 2:
			if args[1] is not None:
				self.processDuplicates = args[1] == 'True'

	def FindInContents(self, item, minI, maxI, contents):
		guess = int(math.floor(minI + (maxI - minI) / 2))
		#print (guess, minI, maxI)
		if maxI >= minI:			
			guessed_line = contents[guess-1]
			#print guessed_line[:-1]
			#print (guess, minI, maxI, guessed_line[:-1])
			m = re.search('(\d{1,7})', guessed_line)
			guessed_ID = int(m.group(0))
			#print(guessed_ID)
			
			if guessed_ID == item:
				return [guess, True]
			
			if guessed_ID < item:
				#print guessed_ID , "<",  item
				return self.FindInContents(item, guess + 1, maxI, contents)
			else:
				#print guessed_ID , ">",  item
				return self.FindInContents(item, minI, guess - 1, contents)
		else:
			#print item , "NOT FOUND at pos" , guess
			return [guess, False]
	
	def Run(self):
		import datetime
		
		if self.processDuplicates:
			self.FixDuplicates()

	def FixDuplicates(self):
		for locale in self.localesList:
			duplicates = []
			itemsList = []
			path = 'ItemLocales/' + locale + '.lua'
			self.currLocaleFile = File(path)
			if not self.currLocaleFile.Exists():
				return
			
			print("Processing duplicates of " + locale)
			contents = self.currLocaleFile.ReadFile()
			
			index = 0
			size = float(len(contents))
				
			for line in contents:
				ids = re.search(r'(\d{1,7})', line)
				if not ids == None:
					itemId = ids.group(0)
					
					exists = False
					if len(itemsList) > 0:
						result = self.FindInContents(int(itemId), 1, len(itemsList), itemsList)
						exists = result[1]
						
					if not exists:
						itemsList.append(itemId)
					else:
						duplicates.append(itemId)
						self.currLocaleFile.DeleteLine(result[0]+1)
						
				index += 1
				print("\r %f %%" % (index * 100 / size))
			print("")
			print("Duplicates:", duplicates)

class Utils():
	def __init__(self):
		pass

	def PlaySound(self, frequency, duration, repetitions):
		try:
			import winsound
			for x in range(1, repetitions+1):
				winsound.Beep(frequency, duration)
		except:
			pass
	
''' ****************
	PROGRAM START
**************** '''
parser = Parser(sys.argv)
#parser.PrintConfig()
parser.Run()
parser.Exit()