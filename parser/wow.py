#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7
import json, requests, sys, datetime, os.path
from tempfile import mkstemp
from shutil import move
from os import remove, close

def checkFileAccess(file):
	if os.path.exists(file):
		try:
			os.rename(file, file)
			#print 'Access on file "' + file +'" is available!'
			return True
		except OSError as e:
			pass
			#print 'Access-error on file "' + file+ '"! \n' + str(e)
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
	print "> wow.py %s %i %i" % (locale, lastID, end)
	replace("wowID.txt", "wow.py %s %i %i" % (locale, start, end), "wow.py %s %i %i" % (locale, lastID, end))

def printError(type, message):
	t = ""
	if type == "E":
		t = "ERROR"
	elif type == "W":
		t = "WARNING"
	print "--------------------------"
	print " /!\ " + t + ": " + message

processStarted = False
currLocale = ''
rangeStart = 25
rangeEnd = 150000
lastItemID = 0

try:
	#CONFIG
	if len(sys.argv) <= 1:
		print "--------------------------"
		print " /!\ ERROR: No arguments: wow.py [locale [rangeStart [rangeEnd]]]"
		print "            Example:      wow.py  en_US     15649      150000"
		print "--------------------------"
	else:
		strLen = 48

		if len(sys.argv) >= 2:
			if sys.argv[1] is not None:
				currLocale = sys.argv[1]

		if len(sys.argv) >= 3:
			if sys.argv[2] is not None:
				rangeStart = int(sys.argv[2])

		if len(sys.argv) >= 4:
			if sys.argv[3] is not None:
				rangeEnd = int(sys.argv[3])

		if rangeEnd <= rangeStart:
			printError("E", "rangeStart can't be less or equal than rangeEnd")
			print "--------------------------"
		else:
			baseUrl = 'https://eu.api.battle.net/wow/item/%d'
			if currLocale == "ko_KR":
				strLen = 28
				baseUrl = 'https://kr.api.battle.net/wow/item/%d'
			if currLocale == "zh_TW":
				baseUrl = 'https://tw.api.battle.net/wow/item/%d'
			if currLocale == "ru_RU":
				strLen = 28

			processStarted = True
			print "--------------------------"
			print "> Start parsing %s locale" % (currLocale)
			print "--------------------------"

			#INIT FILE
			fileName = 'ItemLocales/' + currLocale + '.lua'

			if not os.path.isfile(fileName):
				f = open(fileName,'w')
				f.write('INL_Items.%s = {\n' % (currLocale.replace("_", "")))
				f.close()

			lastItemID = rangeStart

			while rangeStart < rangeEnd - 1:
				try:
					#REQUEST AND PARSE ITEMS
					for itemID in xrange(lastItemID, rangeEnd):

						lastItemID = itemID

						url = baseUrl % (itemID)

						params = dict(
							locale=currLocale,
							apikey='cmjcr3qatwxfezg2ugruszjvhd69mnmr'
						)

						resp = requests.get(url=url, params=params)
						data = json.loads(resp.text)

						now = datetime.datetime.now()
						time = now.strftime('%H:%M:%S')

						if 'status' not in data:
							if 'name' not in data:
								print data
								printError("E", "No 'name' field in data")
								print "--------------------------"
								break

							name = data["name"]
							name = name.replace('"', '\\"')

							nln = '  {%i,"%s"},\n' % (itemID, name)
							nln = nln.encode('utf-8')

							f = open(fileName,'a')
							f.write(nln)
							f.close()

							if len(name) > strLen+3:
								name = name[:strLen] + "..."

							print ("%s - #%i - [%s]" % (time, itemID, name)).encode('utf-8')
						else:
							print "%s - #%i - [---]" % (time, itemID)
				except KeyboardInterrupt:
					raise
				except:
					printError("E", "UNKNOWN ERROR")
					print "--------------------------"

			#END FILE
			f = open(fileName,'a')
			f.write('}')
			f.close()

			print "--------------------------"
			print "> Finished parsing %s locale" % (currLocale)

except KeyboardInterrupt:
	if processStarted:
		printError("W", "Process interrupted by the user")
	else:
		printError("W", "Process interrupted by the user before starting")
except:
	printError("E", "GLOBAL UNKNOWN ERROR")
finally:
	saveIndexes(currLocale, lastItemID, rangeStart, rangeEnd)
	print "--------------------------"