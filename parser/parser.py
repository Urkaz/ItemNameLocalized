import math
import sys, os
from os import remove, close, path, name
import re
import datetime

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

	def Write(self, text):
		f = open(self.path,'w', encoding="utf8")
		f.write(text)
		f.close()

	def WriteAppend(self, text):
		f = open(self.path,'a', encoding="utf8")
		f.write(text)
		f.close()

	def ReadFile(self):
		f = open(self.path, "r", encoding="utf8")
		contents = f.readlines()
		f.close()
		return contents

	def WriteLines(self, linesArray):
		f = open(self.path,'w', encoding="utf8")
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
		with open(abs_path,'w', encoding="utf8") as new_file:
			with open(self.path, encoding="utf8") as old_file:
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
		with open(abs_path,'w', encoding="utf8") as new_file:
			with open(self.path, encoding="utf8") as old_file:
			
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
				#print('Access on file "' + self.path +'" is available!')
				return True
			except OSError as e:
				pass
				#print('Access-error on file "' + self.path + '"! \n' + str(e))
		return False

	def GetNumberOfLines(self):
		f = open(self.path, 'r', encoding="utf8")
		lines = 0
		for line in f:
			lines += 1
		f.close()
		self.lines = lines
		return lines

	def InsertInLine(self, index, value):
		f = open(self.path, "r", encoding="utf8")
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
		print("--------------------------")
		print(" \033[33mItemNameLocalized WoW Api Parser\033[0m")
		print("--------------------------")

		self.localesList = ["en_US","es_MX","pt_BR","de_DE","es_ES","fr_FR","it_IT","ru_RU","ko_KR","zh_TW","zh_CN"]
		self.eachLangcheck = []
		self.rangeStart = 25
		self.rangeEnd = 26

		self.processStarted = False
		self.lastItemID = 0
		self.minimumPrints = False
		self.baseUrl = 'https://eu.api.blizzard.com/data/wow/item/%d'
		self.files = []
		self.dbFile = File("parser_progress.txt")
		
		#Color flags
		self.ADDED = "32"
		self.REPLACED = "36"
		self.UNTOUCHED = "30;1"
		self.REMOVED = "31"
		self.NOT_FOUND = "33"

		#Create locale files if missing
		for i in range(len(self.localesList)):
			locale = self.localesList[i];
			path = 'ItemLocales/' + locale + '.lua'
			init = 'INL_Items.%s = {\n}' % (locale.replace("_", ""))

			self.files.append(File(path))
			if not self.files[i].Exists():
				self.files[i].Write(init);
			self.files[i].GetNumberOfLines();
			
			self.eachLangcheck.append(0);

		#Check dbFile file
		if not self.dbFile.Exists():
			self.PrintError("E", 'File "parser_progress.txt" does not exist.')
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

		#restart after error
		self.Command = ""
		self.Continue = True

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
		print(" \033[36m(i) HELP\033[0m: Arguments: parser.py [rangeStart][rangeEnd][DisablePrints]")
		print("    Example: parser.py 15649 150000 False")
		print("--------------------------")
		print(" Color codes displayed while parsing:")
		print("    \033[%smGreen\033[0m:  New item added" % self.ADDED)
		print("    \033[%smRed\033[0m:    Item deleted (The item was in the file, but not in the API)" % self.REMOVED)
		print("    \033[%smYellow\033[0m: Item not found (The item was not present in the file and the API)" % self.NOT_FOUND)
		print("    \033[%smBlue\033[0m:   Item replaced (A different version of the item was found in the API)" % self.REPLACED)
		print("    \033[%smBlack\033[0m:  Item not changed (The item in the file is the same as the found in the API)" % self.UNTOUCHED)
		print("--------------------------")

	def PrintConfig(self):
		print(" Config:")
		print("\tRange Start: \033[36m%i\033[0m" % (self.rangeStart))
		print("\tRange End: \033[36m%i\033[0m" % (self.rangeEnd))
		print("\tMinimum Prints: \033[36m%s\033[0m" % (self.minimumPrints))
		print("--------------------------")

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

	def Config(self, args):
		if len(args) >= 2:
			if args[1] is not None:
				self.rangeStart = int(args[1])

		if len(args) >= 3:
			if args[2] is not None:
				self.rangeEnd = int(args[2])
		
		if len(args) >= 4:
			if args[3] is not None:
				self.minimumPrints = args[3].lower() == 'true'

	def SaveIndexes(self):
		dbFilename = "parser";
		self.Command = "%s.py %i %i" % (dbFilename, self.lastItemID, self.rangeEnd)
		print(" \033[35m%s.py %i %i\033[0m" % (dbFilename, self.lastItemID, self.rangeEnd))
		self.dbFile.ReplacePattern("%s.py %i %i" % (dbFilename, self.rangeStart, self.rangeEnd), self.Command)

	def FindInFile(self, fileIndex, item):
		contents = self.files[fileIndex].ReadFile()
		return self.FindInContents(item, 2, self.files[fileIndex].lines -1, contents)

	def FindInContents(self, item, minI, maxI, contents):
		guess = int(math.floor(minI + (maxI - minI) / 2))
		#print ("guess: %d | min: %d | max: %d" % (guess, minI, maxI))
		if maxI >= minI:
			guessed_line = contents[guess-1]
			#print ("guess: %d | min: %d | max: %d | guessed_line: %s" % (guess, minI, maxI, guessed_line[:-1]))
			m = re.search('(\d{1,7})', guessed_line)
			if m is None:
				return [1, False]
			guessed_ID = int(m.group(0))
			#print("ID: %d" % guessed_ID)

			if guessed_ID == item:
				#print ("END | guess: %d | line: %s" % (guess-1, contents[guess-1]))
				return [guess-1, True]

			if guessed_ID < item:
				#print ("ID: %d < item: %s" % (guessed_ID, item))
				return self.FindInContents(item, guess + 1, maxI, contents)
			else:
				#print ("ID: %d > item: %s" % (guessed_ID, item))
				return self.FindInContents(item, minI, guess - 1, contents)
		else:
			#print ("END | %d NOT FOUND at pos %d" % (item, guess))
			return [guess-1, False]

	def GetNameFromLine(self, fileIndex, lineIndex):
		contents = self.files[fileIndex].ReadFile()
		m = re.search(r'"(.+?)(?<!\\)"', contents[lineIndex])
		if(m is not None):
			return m.group(0)
		return '""'

	def ReplaceNameFromLine(self, fileIndex, lineIndex, newText):
		contents = self.files[fileIndex].ReadFile()
		self.files[fileIndex].ReplacePattern(contents[lineIndex], newText)

	def PrintItem(self, itemID):
		now = datetime.datetime.now()
		time = now.strftime('%H:%M:%S')
		if not self.minimumPrints:
			data = "|"
			for localeIndex in range(len(self.localesList)):
				data = "%s\033[%sm%s\033[0m|" % (data, self.eachLangcheck[localeIndex], self.localesList[localeIndex])
			print(" %s - #%i - [%s]" % (time, itemID, data))
		else:
			if itemID % 50 == 0:
				print(" %s - \033[36m#%i\033[0m" % (time, itemID))

	def Run(self):
		import json

		reqs = Requests()
		reqs.GetToken()

		error = False
		addedItems = 0
		replacedItems = 0
		isReplaced = False

		try:
			import requests, datetime
			print(" \033[32mStarting\033[0m item parser")
			print("--------------------------")

			self.lastItemID = self.rangeStart

			params = dict(
				namespace="static-eu",
				access_token=reqs.token
			)

			self.processStarted = True
			while self.lastItemID < self.rangeEnd-1 and not error:
				try:
					#REQUEST AND PARSE ITEMS
					for itemID in range(self.lastItemID, self.rangeEnd):

						self.lastItemID = itemID
						url = self.baseUrl % (itemID)

						reqs.MakeRequest(url, params)
						req_status_code = reqs.GetRequestStatusCode()

						data = reqs.GetData()

						if data != "Downstream Error":
							data = json.loads(data)

							if req_status_code == 200:
								if 'name' not in data:
									print(data)
									self.PrintError("E", "No 'name' field in data")
									print("--------------------------")
									error = True
									break

								for localeIndex in range(len(self.localesList)):
									locale = self.localesList[localeIndex];
									nameDict = data["name"]
										
									if locale not in nameDict:
										self.eachLangcheck[localeIndex] = self.NOT_FOUND;
									else:
										name = nameDict[locale]
										name = name.replace('"', '\\"')
										name = name.replace('\r\n', '')
										name = name.replace('\n', '')

										luaString = '  {%i,"%s"},\n' % (itemID, name)
										
										result = self.FindInFile(localeIndex, itemID)
										exists = result[1]

										if not exists:
											self.files[localeIndex].InsertInLine(result[0]+1, luaString)
											self.files[localeIndex].lines += 1
											addedItems += 1
											self.eachLangcheck[localeIndex] = self.ADDED;
										else:
											current_name = self.GetNameFromLine(localeIndex, result[0])
											new_name = '"%s"' % (name)
											if current_name != new_name:
												isReplaced = True
												self.ReplaceNameFromLine(localeIndex, result[0], luaString)
												replacedItems += 1
												self.eachLangcheck[localeIndex] = self.REPLACED;
											else:
												isReplaced = False
												self.eachLangcheck[localeIndex] = self.UNTOUCHED;
											
								self.PrintItem(itemID)
							else:
								if req_status_code == 404:
									if 'detail' not in data:
										self.PrintError("E", "404 Error: No reason found")
										error = True
										break
									else:
										for localeIndex in range(len(self.localesList)):
											result = self.FindInFile(localeIndex, itemID)
											exists = result[1]
											if exists:
												self.files[localeIndex].DeleteLine(result[0]+1)
												self.eachLangcheck[localeIndex] = self.REMOVED;
											else:
												self.eachLangcheck[localeIndex] = self.NOT_FOUND;
										self.PrintItem(itemID)
										
								elif req_status_code == 504:
									self.PrintError("E", "504 Error: Gateway timeout")
									error = True
									break
								else:
									self.PrintError("E", "%i Error: Unknown error code" % (req_status_code)) #504
									error = True
									break
						else:
							print(" %s - \033[33m#%i\033[0m - %s" % (time, itemID, "Downstream Error"))
							
						#if itemID % 50 == 0:
							#print(" New indexes saved:")
							#self.SaveIndexes()
				except KeyboardInterrupt:
					error = True
					raise
				except requests.exceptions.ConnectionError:
					error = True
					raise
				except IOError:
					error = True
					raise
				except ValueError:
					error = True
					raise
				except:
					print("--------------------------")
					self.PrintError("E", "Unknown Error")
					error = True
					raise

			if not error:
				self.lastItemID += 1

			if self.lastItemID >= self.rangeEnd-1:
				self.Continue = False
				print("--------------------------")

		except KeyboardInterrupt:
			print("--------------------------")
			if self.processStarted:
				self.PrintError("W", "Process interrupted by the user")
			else:
				self.PrintError("W", "Process interrupted by the user before starting")
			self.Continue = False
		except requests.exceptions.ConnectionError:
			print("--------------------------")
			self.PrintError("E", "There was a problem with the Internet connection.")
		except IOError:
			print("--------------------------")
			self.PrintError("E", "There was a problem with the file access.")
		except ValueError:
			print("--------------------------")
			self.PrintError("E", "No JSON object could be decoded // ValueError")
		except:
			print("--------------------------")
			self.PrintError("E", "Unknown Error")
			raise
		finally:
			print(" New indexes saved:")
			self.SaveIndexes()
			print("--------------------------")
			print(" Stats:")
			print("\tItems parsed: \033[36m%i\033[0m" % (self.lastItemID - self.rangeStart))
			print("\tNew items added: \033[36m%i\033[0m" % (addedItems))
			print("\tReplaced items: \033[36m%i\033[0m" % (replacedItems))
			print("--------------------------")
			print(" \033[32mProcess Finished\033[0m")
			print("--------------------------")
			self.utils.PlaySound(2000, 250, 1)

class Utils():
	def __init__(self):
		self.Mute = False
		pass

	def PlaySound(self, frequency, duration, repetitions):
		if not self.Mute:
			try:
				import winsound
				for x in range(1, repetitions+1):
					winsound.Beep(frequency, duration)
			except:
				pass

class Requests():
	def __init__(self):
		self.client_id_file = "client_id.key"
		self.client_secret_file = "client_secret.key"
		self.token = ""

	def GetToken(self):
		try:
			import requests, json
			url = "https://eu.battle.net/oauth/token"

			params = dict(
				grant_type="client_credentials",
				client_id=self.ReadClientID(),
				client_secret=self.ReadClientSecret()
			)

			resp = requests.get(url=url, params=params)
			data = json.loads(resp.text)

			if resp.status_code == 200:
				if 'access_token' not in data:
					print(data)
					self.PrintError("E", "No 'name' field in data")
					print("--------------------------")
				self.token = data["access_token"]
		except ValueError:
			print("--------------------------")
			self.PrintError("E", "No JSON TOKEN object could be decoded")
		except requests.exceptions.ConnectionError:
			print("--------------------------")
			self.PrintError("E", "There was a problem with the Internet connection.")

	def ReadClientID(self):
		if os.path.isfile(self.client_id_file):
			fa = open(self.client_id_file,'r', encoding="utf8")
			client_id = fa.readline()
			fa.close()
			return client_id

	def ReadClientSecret(self):
		if os.path.isfile(self.client_secret_file):
			fa = open(self.client_secret_file,'r', encoding="utf8")
			client_secret = fa.readline()
			fa.close()
			return client_secret

	def MakeRequest(self, url, params):
		import requests
		self.resp = requests.get(url=url, params=params)

	def GetRequestStatusCode(self):
		return self.resp.status_code

	def GetData(self):
		return self.resp.text

	def PrintError(self, type, message):
		t = ""
		if type == "E":
			t = "\033[31m/!\\ ERROR\033[0m"
			# self.utils.PlaySound(200, 200, 3)
		elif type == "W":
			t = "\033[33m/!\\ WARNING\033[0m"
			# self.utils.PlaySound(200, 200, 2)
		print(" %s: %s" % (t, message))
		print("--------------------------")

''' ****************
	PROGRAM START
**************** '''
parser = Parser(sys.argv)
parser.PrintConfig()
parser.Run()
parser.Exit()