from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import selenium.webdriver.common.by as By
from selenium.webdriver.common.keys import Keys

from datetime import datetime

from time import sleep
import os, shutil, re
from fpdf import FPDF
from PIL import Image




class Searches: 
	
	
		
	
	def search_init(self):
		read_url = 'music.youtube.com'
		chrome_options = Options()
		chrome_options.add_argument("user-data-dir=selenium") 
		chrome_options.add_argument("--start-fullscreen")
		#chrome_options.add_argument("--incognito")
		chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:1111")
		
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.wait = WebDriverWait(self.driver,100)
		options = {
			'page-width' : '211',
			'page-height': '298',
			'enable-local-file-access':''
			}
    
		#go to youtube music
		self.driver.get('https://music.youtube.com/')
		
		
		sleep(5)
		

	def search_song(self, song):
		self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]').click()
		sleep(5)
		#song_search_element.send_keys(Keys.Home)
		self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').clear()
		self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').send_keys(song)
		self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').send_keys(Keys.RETURN)
		#song_search_element.send_keys(song)
		sleep(10)
		print('I entered the search term: ' + song)
		#Click on "Songs" 
		self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[1]/ytmusic-chip-cloud-renderer/div/ytmusic-chip-cloud-chip-renderer[1]/a/yt-formatted-string').click()
		sleep(10)
		
		
	
	def match_time(self, time_string) :	
		print(*(time_string.split(" ")), sep = ",")
		dur_song = datetime.strptime(time_string.rstrip(), "%M:%S")	
		
		dur_dif = []
		for i in range(5) :
			
			
			for j in range(1,5) :
				element_string = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[2]/ytmusic-responsive-list-item-renderer[' + str(i+1) + ']/div[2]/div[3]/yt-formatted-string/span[' + str(j) + ']'
				#print('The element string is: ' + element_string)
				try :
					dur_string = self.driver.find_element_by_xpath(element_string).text
					#print('The string of the searched song duration is: ' + dur_string) 
					try : 
						dur_yt = datetime.strptime(dur_string, "%M:%S")
						dur_dif.append(abs((dur_yt - dur_song).total_seconds()))
						#print('The datetime of the searched song duration is: ' + str(dur_yt))
						#print((dur_yt - dur_song).total_seconds())
						break
					except :
						#print('Need to have something in except block')
						continue
				except :
					#print('Not working') 
					continue
					
						
			
			
			
		#sleep(100000)
		#find the one that is closest to 0, return the index.  
		return dur_dif.index(min(dur_dif))
		
	def library_add(self, ind) :
		got_song_title_xpath = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[2]/ytmusic-responsive-list-item-renderer[' + str(ind+1) + ']/div[2]/div[1]/yt-formatted-string'
		got_song_artist_xpath = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[2]/ytmusic-responsive-list-item-renderer[' + str(ind+1) + ']/div[2]/div[3]/yt-formatted-string/a[1]'
		got_song_title = self.driver.find_element_by_xpath(got_song_title_xpath).text
		got_song_artist = self.driver.find_element_by_xpath(got_song_artist_xpath).text
		
		got_song = got_song_title + " " + got_song_artist
		print('I matched: ' + got_song)
		
		
		
		#right click anywhere within the song
		song_area = self.driver.find_element_by_xpath(got_song_title_xpath)
		sleep(5)
		ActionChains(self.driver).context_click(song_area).perform()
				
		
		add_to_library_option = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-toggle-menu-service-item-renderer[1]'
		
		add_to_library_item = self.driver.find_element_by_xpath(add_to_library_option)
		
		add_to_library_item_text = add_to_library_item.text
		while not add_to_library_item_text :
			print('.', end='')
			sleep(5)  #increase this sleep if add_to_library_item.text is coming back blank
			add_to_library_item_text = add_to_library_item.text
		print('.')
		print('The option is:' + add_to_library_item_text)	
		
		
		if 'Add' in add_to_library_item.text :
			self.driver.find_element_by_xpath(add_to_library_option).click()
			
			print('I added the song to the library.')
			#else :
			#	print('The song was not added to the library.')
		elif 'Remove' in add_to_library_item.text : 
			print('This song is already in your library!')
		else :
			print('Something went wrong.. increase sleep timers')
				
		return got_song
		
		
		

