#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, requests, os.path, sys

from tempfile import mkstemp
from shutil import move
from os import remove, close

def replace(file_path, pattern, subst):
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

#CONFIG
if len(sys.argv) <= 1:
	print "--------------------------"
	print " /!\ ERROR: No arguments: wow.py [locale [rangeStart [rangeEnd]]]"
	print "            Example:      wow.py  en_US     15649      150000"
	print "--------------------------"
else:
	currLocale = ''
	rangeStart = 25
	rangeEnd = 150000

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
		print "--------------------------"
		print " /!\ ERROR: rangeStart can't be less or equal than rangeEnd"
		print "--------------------------"
	else:
		baseUrl = 'https://eu.api.battle.net/wow/item/%d'

		print "--------------------------"
		print "> Start parsing %s locale" % (currLocale)
		print "--------------------------"

		#INIT FILE
		fileName = 'ItemLocales/' + currLocale + '.lua'

		if not os.path.isfile(fileName):
			f = open(fileName,'w')
			f.write(currLocale + 'INL_Items. = {\n')
			f.close()

		lastItemID = 0
			
		try:
			#REQUEST AND PARSE ITEMS
			for itemID in xrange(rangeStart, rangeEnd):
				
				lastItemID = itemID
				
				url = baseUrl % (itemID)
					
				params = dict(
					locale=currLocale,
					apikey='cmjcr3qatwxfezg2ugruszjvhd69mnmr'
				)

				resp = requests.get(url=url, params=params)
				data = json.loads(resp.text)

				if 'status' not in data:
					name = data["name"]
					name = name.replace('"', '\\"')
						
					nln = '  {%i,"%s"},\n' % (itemID, name)
					nln = nln.encode('utf-8')
						
					f = open(fileName,'a')
					f.write(nln)
					f.close()
						
					print ("#%i [%s]" % (itemID, name)).encode('utf-8')
				else:
					print "#%i [---]" % (itemID)

			#END FILE
			f = open(fileName,'a')
			f.write('}')
			f.close()
		
		except KeyboardInterrupt:
			print "--------------------------"
			print "> wow.py %s %i %i" % (currLocale, lastItemID, rangeEnd)
			replace("wowID.txt", "wow.py %s %i %i" % (currLocale, rangeStart, rangeEnd), "wow.py %s %i %i" % (currLocale, lastItemID, rangeEnd))
		except:
			print "--------------------------"
			print "> wow.py %s %i %i" % (currLocale, lastItemID, rangeEnd)
			print "--------------------------"
			print " /!\ AN ERROR HAS OCCURRED"
			print "--------------------------"
			replace("wowID.txt", "wow.py %s %i %i" % (currLocale, rangeStart, rangeEnd), "wow.py %s %i %i" % (currLocale, lastItemID, rangeEnd))
			raise
		
		print "--------------------------"
		print "> Finished parsing %s locale" % (currLocale)
		print "--------------------------"