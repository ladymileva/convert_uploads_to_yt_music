import base
from time import sleep
import os, re, json, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import selenium.webdriver.common.by as By
from time import sleep

start_time = datetime.datetime.now()    #log inicial time


def get_uploads_list(uploads_file):
	song_list = []
	time_list = []
	m = False
	with open(uploads_file, encoding='utf-8', errors='ignore') as f:
		all_lines = f.readlines()
		f.close()
		ctr = 2
		for line in all_lines:
			if ctr == 2 :
				song_string = str.rstrip(line)
			elif ctr == 3 :
				song_string = str.rstrip(song_string + " " + line)
				song_list.append(song_string)
			else : 
				m = re.match("^([0-5]?[0-9]):([0-5]?[0-9])$", line)
				
				if m:
					time_list.append(line)
					ctr = 0  
					
			ctr += 1	
	
	
	return song_list, time_list			
	
	
			


#reads the config.json    
json_file = open('./config.json')
config = json.load(json_file)
uploads_file = config["filename"]
song_list, time_list = get_uploads_list(uploads_file)

searches = base.Searches() 	#sets Searches class from base.py file
#searches.login()
searches.search_init()

i = 0 #can change value from 0 if you want to start farther down the list
got_song = []

for song in song_list[i:]:   
	print('Working with song #' + str(i))
	searches.search_song(song)
	ind = searches.match_time(time_list[i])
	gs = searches.library_add(ind)
	got_song.append(gs)
	
	with open('matches_file.txt', 'a', encoding='utf-8') as f:	
		f.write('i = ' + str(i) + ':' + song + ' --> ' + gs + '\n')
		f.close()
	i += 1
	

	
