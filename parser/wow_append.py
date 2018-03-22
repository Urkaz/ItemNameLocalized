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
		print " \033[33mItemNameLocalized WoW Api Parser\033[0m"
		print "--------------------------"
		
		self.currLocale = ''
		self.rangeStart = 25
		self.rangeEnd = 153490
		self.compactMode = False
		
		self.processStarted = False
		self.lastItemID = 0
		self.strLen = 48
		self.baseUrl = 'https://eu.api.battle.net/wow/item/%d'
		self.apiKey = ""
		self.file = None
		self.removedLua = []
		self.dbFile = File("wowID.txt")
		self.error = False
		
		#Check dbFile file
		if not self.dbFile.Exists():
			self.PrintError("E", 'File "wowID.txt" does not exist.')
			self.Exit()
		
		#Config
		if len(args) <= 1: 
			self.PrintArgs()
			self.Exit()
		else:
			self.Config(args)
			if self.rangeEnd <= self.rangeStart:
				self.PrintError("E", "rangeStart can't be less or equal than rangeEnd")
				self.Exit()
	
		#Utils
		self.utils = Utils()
		self.utils.PlaySound(2000, 250, 1)
		
	def Exit(self):
		if self.osSleep:
			self.osSleep.Uninhibit()
		sys.exit()
	
	def PrintArgs(self):
		print " \033[31m/!\ ERROR\033[0m: No arguments: wow.py  locale [rangeStart [rangeEnd]]"
		print "            Example:      wow.py  en_US    15649      150000"
		print "--------------------------"
		
	def PrintConfig(self):
		print " Config:"
		print "\tLanguage: \033[36m%s\033[0m" % (self.currLocale)
		print "\tRange Start: \033[36m%i\033[0m" % (self.rangeStart)
		print "\tRange End: \033[36m%i\033[0m" % (self.rangeEnd)
		print "--------------------------"
	
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
		
	def ReadAPIKey(self, apiKeyFile):
		if os.path.isfile(apiKeyFile):
			fa = open(apiKeyFile,'r')
			self.apiKey = fa.readline()
			fa.close()
	
	def Config(self, args):
		if len(args) >= 2:
			if args[1] is not None:
				self.currLocale = args[1]

		if len(args) >= 3:
			if args[2] is not None:
				self.rangeStart = int(args[2])

		if len(args) >= 4:
			if args[3] is not None:
				self.rangeEnd = int(args[3])

		if self.currLocale == "ko_KR":
			self.strLen = 28
			self.baseUrl = 'https://kr.api.battle.net/wow/item/%d'
		if self.currLocale == "zh_TW":
			self.baseUrl = 'https://tw.api.battle.net/wow/item/%d'
		if self.currLocale == "ru_RU":
			self.strLen = 28
		
		self.ReadAPIKey("apikey.key");
		
		path = 'ItemLocales/' + self.currLocale + '_APPEND.lua'
		init = 'INL_Items.%s = {\n}' % (self.currLocale.replace("_", ""))
		self.file = File(path)
		if not self.file.Exists():
			self.file.Write(init);
	
	def RemoveExtraLua(self):	
		contents = self.file.ReadFile()
		
		self.removedLua = []
		self.removedLua.append(contents[:1][0])
		self.removedLua.append(contents[-1:][0])
		
		contents = contents[1:-1]
		
		self.file.WriteLines(contents)

	def RestoreExtraLua(self):
		contents = self.file.ReadFile()

		contents.insert(0, self.removedLua[0])
		contents.append(self.removedLua[1])
		
		self.file.WriteLines(contents)
	
	def SaveIndexes(self):
		print " \033[35mwow_append.py %s %i %i\033[0m" % (self.currLocale, self.lastItemID, self.rangeEnd)
		self.dbFile.ReplacePattern("wow_append.py %s %i %i" % (self.currLocale, self.rangeStart, self.rangeEnd), "wow_append.py %s %i %i" % (self.currLocale, self.lastItemID, self.rangeEnd))
	
	def FindInFile(self, itemID, minI, maxI):
		contents = self.file.ReadFile()
		return self.FindInFile_Contents(itemID, minI, maxI, contents)
	
	def FindInFile_Contents(self, itemID, minI, maxI, contents):
		guess = int(math.floor(minI + (maxI - minI) / 2))
		#print (guess, minI, maxI)
		if maxI >= minI:			
			guessed_line = contents[guess-1]
			#print guessed_line[:-1]
			#print (guess, minI, maxI, guessed_line[:-1])
			m = re.search('(\d{1,7})', guessed_line)
			guessed_ID = int(m.group(0))
			
			if guessed_ID == itemID:
				return [guess, True]
			
			if guessed_ID < itemID:
				#print guessed_ID , "<",  itemID
				return self.FindInFile_Contents(itemID, guess + 1, maxI, contents)
			else:
				#print guessed_ID , ">",  itemID
				return self.FindInFile_Contents(itemID, minI, guess - 1, contents)
		else:
			#print itemID , "NOT FOUND at pos" , guess
			return [guess, False]
	
	def Run(self):
		import requests, json, datetime
		
		self.error = False
		
		try:
			print " \033[32mStarting\033[0m item parser"
			print "--------------------------"

			self.lastItemID = self.rangeStart
			
			params = dict(
				locale=self.currLocale,
				apikey=self.apiKey
			)
			
			self.file.GetNumberOfLines()

			self.RemoveExtraLua()
			self.file.GetNumberOfLines()
			
			self.processStarted = True
			while self.lastItemID < self.rangeEnd-1 and not self.error:
				try:
					#REQUEST AND PARSE ITEMS
					for itemID in xrange(self.lastItemID, self.rangeEnd):
					
						self.lastItemID = itemID
						url = self.baseUrl % (itemID)
						
						resp = requests.get(url=url, params=params)
						data = json.loads(resp.text)
						
						now = datetime.datetime.now()
						time = now.strftime('%H:%M:%S')
						
						if resp.status_code == 200:
							if 'name' not in data:
								print data
								self.PrintError("E", "No 'name' field in data")
								print "--------------------------"
								self.error = True
								break
							
							name = data["name"]
							name = name.replace('"', '\\"')
							
							luaString = '  {%i,"%s"},\n' % (itemID, name)
							luaString = luaString.encode('utf-8')
							
							exists = False
							result = self.FindInFile(itemID, 1, self.file.lines)
							if not result[1]:
								self.file.InsertInLine(result[0], luaString)
								self.file.lines += 1
								exists = True
							
							if len(name) > self.strLen+3:
								name = name[:self.strLen] + "..."
							
							if exists:
								print (" %s - \033[31m#%i\033[0m - [%s]" % (time, itemID, name)).encode('utf-8')
							else:
								print (" %s - \033[32m#%i\033[0m - [%s]" % (time, itemID, name)).encode('utf-8')
						else:
							if resp.status_code == 404:
								if 'reason' not in data:
									self.PrintError("E", "404 Error: No reason found")
									self.error = True
									break
								else:
									print " %s - \033[33m#%i\033[0m - /!\ %s" % (time, itemID, data["reason"].encode('utf-8'))
							else:
								self.PrintError("E", "%i Error: Unknown error code" % (resp.status_code))
								self.error = True
								break
				except KeyboardInterrupt:
					self.error = True
					raise
				except:
					self.PrintError("E", "Unknown Error")
					self.error = True
					raise
			
			if not self.error:
				self.lastItemID += 1
			
			print " \033[32mFinished\033[0m parsing \033[36m%s\033[0m" % (self.currLocale)
			print "--------------------------"
			self.utils.PlaySound(2000, 250, 1)
		except KeyboardInterrupt:
			print "--------------------------"
			if self.processStarted:
				self.PrintError("W", "Process interrupted by the user")
			else:
				self.PrintError("W", "Process interrupted by the user before starting")
		except:
			self.PrintError("E", "Unknown Error")
			raise
		finally:
			self.RestoreExtraLua()
			print " New indexes saved:"
			self.SaveIndexes()
			print "--------------------------"
			self.rangeStart = self.lastItemID

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
parser.PrintConfig()
parser.Run()
parser.Exit()