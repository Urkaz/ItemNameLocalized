#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7
import math
import sys, os
from os import remove, close, path, name
import re

# check dependent modules
import imp
try:
	imp.find_module('requests')
except:
	print '"requests" module not found, install using the command "pip install requests"'
	sys.exit()

try:
	imp.find_module('colorama')
except:
	print '"colorama" module not found, install using the command "pip install colorama"'
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
	
	def Write(self, text):
		f = open(self.path,'w')
		f.write(text)
		f.close()
	
	def WriteAppend(self, text):
		f = open(self.path,'a')
		f.write(text)
		f.close()
		
	def ReadFile(self):
		f = open(self.path, "r")
		contents = f.readlines()
		f.close()
		return contents
	
	def WriteLines(self, linesArray):
		f = open(self.path,'w')
		for line in linesArray:
			f.write(line)
		f.close()
		
	def ReplacePattern(self, pattern, subst):
		from tempfile import mkstemp
		from shutil import move
	
		while not self.CheckFileAccess():
			pass

		#Create temp file
		fh, abs_path = mkstemp()
		with open(abs_path,'w') as new_file:
			with open(self.path) as old_file:
				for line in old_file:
					new_file.write(line.replace(pattern, subst))
		close(fh)
		#Remove original file
		remove(self.path)
		#Move new file
		move(abs_path, self.path)
		
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
		
	def InsertInLine(self, index, value):
		f = open(self.path, "r")
		contents = f.readlines()
		f.close()

		contents.insert(index, value)
		
		contents = "".join(contents)
		self.Write(contents)
	
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
		print "--------------------------"
		print " \033[33mItemNameLocalized Locales Fixer\033[0m"
		print "--------------------------"
		
		#self.localesList = ["en_US","es_ES","es_MX","de_DE","fr_FR","it_IT","pt_BR","ru_RU","ko_KR","zh_TW"]
		self.localesList = ["en_US","es_ES"]
		self.currLocaleFile = None
		
		self.dbFile = File("IDs_list.txt")
		self.dbFile.GetNumberOfLines()
		
		self.removedLua = []
		self.createDB = False
		self.processDuplicates = False
		self.findMissing = False
		
		#Check files
		if not self.dbFile.Exists():
			self.PrintError("E", 'File "IDs_list.txt" does not exist.')
			self.Exit()
		
		#Config
		if len(args) <= 2: 
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
				print (self.Command)
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
		print " \033[31m/!\ ERROR\033[0m: No arguments: PLACEHOLDER"
		print "            PLACEHOLDER"
		print "--------------------------"
		
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
		print "\t\t\t\t\t\t\t\t\t\t\t\t\r",
		print " %s: %s" % (t, message)
		print "--------------------------"
	
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
		
		if len(args) >= 3:
			if args[2] is not None:
				self.createDB = args[2] == 'True'
		
		if len(args) >= 4:
			if args[3] is not None:
				self.findMissing = args[3] == 'True'
	
	def RemoveExtraLua(self):	
		contents = self.currLocaleFile.ReadFile()
		
		self.removedLua = []
		self.removedLua.append(contents[:1][0])
		self.removedLua.append(contents[-1:][0])
		
		contents = contents[1:-1]
		
		self.currLocaleFile.WriteLines(contents)
		
	def RestoreExtraLua(self):
		contents = self.currLocaleFile.ReadFile()

		contents.insert(0, self.removedLua[0])
		contents.append(self.removedLua[1])
		
		self.currLocaleFile.WriteLines(contents)
	
	''' def SaveIndexes(self):
		self.Command = "wow_append.py %s %i %i" % (self.currLocale, self.lastItemID, self.rangeEnd)
		print " \033[35mwow_append.py %s %i %i\033[0m" % (self.currLocale, self.lastItemID, self.rangeEnd)
		self.dbFile.ReplacePattern("wow_append.py %s %i %i" % (self.currLocale, self.rangeStart, self.rangeEnd), "wow_append.py %s %i %i" % (self.currLocale, self.lastItemID, self.rangeEnd))
	'''
	
	def FindInFile(self, item, minI, maxI, file):
		contents = file.ReadFile()
		return self.FindInContents(item, minI, maxI, contents)
	
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
		
		if self.createDB:
			self.CreateIDDatabase()
		
		if self.findMissing:
			self.FindMissing()

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
				print "\r %f %%" % (index * 100 / size),
			print ""
			print "Duplicates:", duplicates
	
	def CreateIDDatabase(self):
		print("Creating list of IDs")
	
		for locale in self.localesList:
			addedIndexes = 0	
			path = 'ItemLocales/' + locale + '.lua'
			self.currLocaleFile = File(path)
			if not self.currLocaleFile.Exists():
				continue
		
			print("Processing " + locale)
			contents = self.currLocaleFile.ReadFile()
			
			index = 0
			size = float(len(contents))
			
			for line in contents:
				ids = re.search(r'(\d{1,7})', line)
				if not ids == None:
					itemId = ids.group(0)
					#print("-"+itemId+"-")
					result = self.FindInFile(int(itemId), 1, self.dbFile.lines, self.dbFile)
					#print(result)
					exists = result[1]
					if not exists:
						self.dbFile.InsertInLine(result[0], itemId+"\n")
						self.dbFile.lines += 1
						addedIndexes += 1
				index += 1
				print "\r %f %%" % (index * 100 / size),
			print ""
			print "Added %i" % (addedIndexes)
	
	def FindMissing(self):
		print("Checking missing items")
		
		dbContent = self.dbFile.ReadFile()
		
		for locale in self.localesList:
			path = 'ItemLocales/' + locale + '.lua'
			self.currLocaleFile = File(path)
			self.currLocaleFile.GetNumberOfLines()
			if not self.currLocaleFile.Exists():
				continue
			
			self.RemoveExtraLua()
			
			print("Processing " + locale)
			
			index = 0
			size = float(len(dbContent))
			
			for item in dbContent:
				ids = re.search(r'(\d{1,7})', item)
				if not ids == None:
					itemId = ids.group(0)
					result = self.FindInFile(int(itemId), 1, self.currLocaleFile.lines, self.currLocaleFile)
					exists = result[1]
					if not exists:
						command = "parser.py %s %i %i" % (locale, int(itemId)-1, int(itemId)+2)
						self.RestoreExtraLua()
						os.system(command)
						self.RemoveExtraLua()
				index += 1
				print "\r %f %%" % (index * 100 / size),
			self.RestoreExtraLua()
	
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