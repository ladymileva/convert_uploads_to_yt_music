# convert_uploads_to_yt_music
Adds contents of "Uploads" library to "Youtube music" library for customers who migrated from Google Play. Requires Google chrome browser and python 3 with selenium WebDriver for chrome browser (https://chromedriver.chromium.org/downloads).  Tested in Windows 10.    

acknowledgement to github user ath67 (whose code this was adapted from)

Users must have a valid Youtube music account.

This python script automates addition of songs from Uploads library to Youtube library.  It performs a search for song title and artist, and from the top five song results will add the song to Youtube library which has the closest duration.  It is not failsafe but records a file with all the matches so that manual corrections can be done if necessary.    

1) Create a text file with all songs in "Uploads" library. <br />  
  a) Navigate to Uploads page <br />
  b) Scroll manually to the bottom of the Uploads page or enter the following command in chrome Developer Tools:  <br />

var i = 0; <br />
(function scroll () { <br />
  if (i > 50) { <br />
    return <br />
  } <br />
  i++ <br />
  window.scrollTo(0, 9999999) <br />
  console.log('scrolled ' + i) <br />
  setTimeout(scroll, 900) <br />
  })() <br />
  
  c) Ctrl-A to select all songs on the page.  Paste output into plain text file and save file, for example, as "youtube_music_uploads.txt"  <br />
  
2) Create a file called config.json in the same folder as main.py and base.py.  Its contents should be as follows: <br />
{ <br />
    "filename" : "C:\\\path\\\to\\\uploads\\\file\\\youtube_music_uploads.txt" <br />
} <br />

3) Start an instance of the Google Chrome debugger on port 1111: <br />
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=1111 --user-data-dir="C:\selenium\AutomationProfile"
Ensure that if you navigate to music.youtube.com you are logged in automatically.  This debugger step is necessary because Youtube music rejects login attempts by selenium.  

4) Navigate to locate of main.py in terminal and execute the python script: python main.py
5) Progress will be recorded in "matches_file.txt", listing the song title and artist from the Uploads library, and the corresponding song title and artist that was added to your youtube library.  

Troubleshooting: 
Occasionally the program crashes due to unexpected organization of the search results page.  In this case, manually add the song which caused the error to youtube library, then restart the python script after changing the starting value of "i" in main.py to the next in value the list so that you don't have to start over from 0.  
