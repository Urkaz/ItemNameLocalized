#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7
import json, requests, sys, datetime, os.path
from tempfile import mkstemp
from shutil import move
from os import remove, close
import math
import linecache
import re

def checkFileAccess(file_path):
	if os.path.exists(file_path):
		try:
			os.rename(file_path, file_path)
			#print 'Access on file "' + file_path +'" is available!'
			return True
		except OSError as e:
			pass
			#print 'Access-error on file "' + file_path + '"! \n' + str(e)
	return False

def replace(file_path, pattern, subst):
	while not checkFileAccess(file_path):
		pass

	#Create temp file
	fh, abs_path = mkstemp()
	with open(abs_path,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(pattern, subst))
	close(fh)
	#Remove original file
	remove(file_path)
	#Move new file
	move(abs_path, file_path)

def saveIndexes(locale, lastID, start, end):
	print "--------------------------"
	print "> wow_append.py %s %i %i" % (locale, lastID, end)
	replace("wowID.txt", "wow_append.py %s %i %i" % (locale, start, end), "wow_append.py %s %i %i" % (locale, lastID, end))
	
def findInFile(file_path, itemID, minI, maxI):
	guess = int(math.floor(minI + (maxI - minI) / 2))
	#print (guess, minI, maxI)
	if maxI >= minI:
		
		f = open(file_path, "r")
		contents = f.readlines()
		f.close()
		guessed_line = contents[guess-1]
		#print guessed_line[:-1]
		#print (guess, minI, maxI, guessed_line[:-1])
		m = re.search('(\d{1,7})', guessed_line)
		guessed_ID = int(m.group(0))
		
		if guessed_ID == itemID:
			return [guess, True]
		
		if guessed_ID < itemID:
			#print guessed_ID , "<",  itemID
			return findInFile(file_path, itemID, guess + 1, maxI)
		else:
			#print guessed_ID , ">",  itemID
			return findInFile(file_path, itemID, minI, guess - 1)
	else:
		#print itemID , "NOT FOUND at pos" , guess
		return [guess, False]
	
def removeExtraLua(file_path):	
	f = open(file_path, "r")
	contents = f.readlines()
	f.close()
	
	lua_lines = []
	lua_lines.append(contents[:1][0])
	lua_lines.append(contents[-1:][0])
	
	contents = contents[1:-1]
	
	f = open(file_path, "w")
	for line in contents:
		f.write(line)
	f.close()
	
	return lua_lines

def restoreExtraLua(file_path, lua_lines):
	f = open(file_path, "r")
	contents = f.readlines()
	f.close()

	contents.insert(0, lua_lines[0])
	contents.append(lua_lines[1])
	
	f = open(file_path, "w")
	for line in contents:
		f.write(line)
	f.close()

class File():
	def __init__(self, path_, init_text):
		self.path = path_
		self.lines = 0
		
		if not os.path.isfile(self.path):
			self.Write(init_text);
			
	def Write(self, text):
		f = open(self.path,'w')
		f.write(text)
		f.close()
	
	def WriteAppend(self, text):
		f = open(self.path,'a')
		f.write(text)
		f.close()
	
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
	def __init__(self):
		self.processStarted = False
		self.currLocale = ''
		self.lastItemID = 0
		self.rangeStart = 25
		self.rangeEnd = 153490
		self.strLen = 48
		self.baseUrl = 'https://eu.api.battle.net/wow/item/%d'
		self.apiKey = ""
		self.file = None
		self.removedLua = []
	
	def PrintArgs(self):
		print "--------------------------"
		print " /!\ ERROR: No arguments: wow.py  locale [rangeStart [rangeEnd]]"
		print "            Example:      wow.py  en_US     15649      150000"
		print "--------------------------"
	
	def PrintError(self, type, message):
		t = ""
		if type == "E":
			t = "ERROR"
		elif type == "W":
			t = "WARNING"
		print "--------------------------"
		print " /!\ " + t + ": " + message
	
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
		self.file = File(path, init)
	
	def Run(self, args):
		try:
			if len(args) <= 1:
				self.PrintArgs()
			else:
				self.Config(args)
			
				if self.rangeEnd <= self.rangeStart:
					self.PrintError("E", "rangeStart can't be less or equal than rangeEnd")
					print "--------------------------"
				else:
					print "--------------------------"
					print "> Start parsing %s locale" % (self.currLocale)
					print "--------------------------"

					self.lastItemID = self.rangeStart
					
					params = dict(
						locale=self.currLocale,
						apikey=self.apiKey
					)
					
					self.file.GetNumberOfLines()

					self.removedLua = removeExtraLua(self.file.path)
					self.file.GetNumberOfLines()
					
					self.processStarted = True
					while self.lastItemID < self.rangeEnd-1:
						try:
							#REQUEST AND PARSE ITEMS
							for itemID in xrange(self.lastItemID, self.rangeEnd):
							
								self.lastItemID = itemID
								url = self.baseUrl % (itemID)
								
								resp = requests.get(url=url, params=params)
								data = json.loads(resp.text)
								
								now = datetime.datetime.now()
								time = now.strftime('%H:%M:%S')
								
								if 'status' not in data:
									if 'name' not in data:
										print data
										self.PrintError("E", "No 'name' field in data")
										print "--------------------------"
										break
									
									name = data["name"]
									name = name.replace('"', '\\"')
									
									luaString = '  {%i,"%s"},\n' % (itemID, name)
									luaString = luaString.encode('utf-8')
									
									result = findInFile(self.file.path, itemID, 1, self.file.lines)
									if not result[1]:
										self.file.InsertInLine(result[0], luaString)
										self.file.lines += 1
									
									if len(name) > self.strLen+3:
										name = name[:self.strLen] + "..."
										
									print ("%s - #%i - [%s]" % (time, itemID, name)).encode('utf-8')
								else:
									print "%s - #%i - [---]" % (time, itemID)
						except KeyboardInterrupt:
							raise
						except:
							self.PrintError("E", "UNKNOWN ERROR")
							print "--------------------------"
							raise
						
					self.lastItemID += 1
					
					print "--------------------------"
					print "> Finished parsing %s locale" % (self.currLocale)
		except KeyboardInterrupt:
			if self.processStarted:
				self.PrintError("W", "Process interrupted by the user")
			else:
				self.PrintError("W", "Process interrupted by the user before starting")
		except:
			self.PrintError("E", "GLOBAL UNKNOWN ERROR")
		finally:
			restoreExtraLua(self.file.path, self.removedLua)
			saveIndexes(self.currLocale, self.lastItemID, self.rangeStart, self.rangeEnd)
			print "--------------------------"
''' ****************
	PROGRAM START
**************** '''
parser = Parser()
parser.Run(sys.argv)