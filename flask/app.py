
from __future__ import unicode_literals
from flask import Flask, flash, request, redirect, url_for, render_template
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
from pprint import pprint
import pyap
import os
import youtube_dl
import random
from google.oauth2 import service_account
from google.cloud import vision
import io
import base64

app = Flask(__name__)

# index
@app.route('/')
def index():
    return render_template('index.html')


#return render_template('index.html', )

#@app.route('/callFunction')
#def callFunction():
"""
ButtonPressed = 0
@app.route('/button', methods=["GET", "POST"])
def button():
    if request.method == "POST":
        return render_template("index.html", ButtonPressed = ButtonPressed)
        # I think you want to increment, that case ButtonPressed will be plus 1.
    return render_template("index.html", ButtonPressed = ButtonPressed)
"""

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = "TEST"
      return render_template("result.html",result = result)

def getSpotify(userINPUT, passwINPUT):
    op = Options()
    #op.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    link = "https://developer.spotify.com/console/get-users-currently-playing-track/"
    driver.get(link)
    getTokenButton = "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div/form/div[3]/div/span/button"
    checkBox = "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div/div[1]/div/div/div[2]/form/div[1]/div/div/div/div/label/span"
    checkBoxPosition = "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div/div[1]/div/div/div[2]/form/div[2]/div/div[1]/div/label/span"
    finalButton = "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div/div[1]/div/div/div[2]/form/input"
    user = "/html/body/div[1]/div[2]/div/form/div[1]/div/input"
    passw = "/html/body/div[1]/div[2]/div/form/div[2]/div/input"
    login = "/html/body/div[1]/div[2]/div/form/div[4]/div[2]/button"
    agree = "/html/body/div/div[2]/div/div/div[4]/div/form/button"
    token = "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div/form/div[3]/div/input"
    driver.find_element_by_xpath(getTokenButton).click()
    time.sleep(0.5)
    try:
        driver.find_element_by_xpath(".//*[contains(text(), 'user-read-currently-playing')]").click()
    except:
        driver.find_element_by_xpath(checkBox).click()
    try:
        driver.find_element_by_xpath(".//*[contains(text(), 'user-read-playback-position')]").click()
    except:
        driver.find_element_by_xpath(checkBoxPosition).click()
    driver.find_element_by_xpath(finalButton).click()
    driver.find_element_by_xpath(user).send_keys(userINPUT)
    driver.find_element_by_xpath(passw).send_keys(passwINPUT)
    driver.find_element_by_xpath(login).click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath(agree).click()
    except:
        pass
    tokenTEXT = driver.find_element_by_xpath(token).get_attribute('value')
    #tokenTEXTOther = driver.find_element_by_xpath(token).text
    driver.quit()
    return tokenTEXT
def getCurrentPlayingInfo(token, printOut = False):
    #https://developer.spotify.com/console/get-users-currently-playing-track/
    SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
    ACCESS_TOKEN = token
    response = requests.get(SPOTIFY_GET_CURRENT_TRACK_URL,headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    #callSpotifyData = datetime.datetime.now()
    resp = response.json()
    playing = resp['is_playing'],
    albumName = resp['item']['album']['name']
    artistName = resp['item']['album']['artists'][0]['name']
    duration = resp['item']['duration_ms']
    progress = resp['progress_ms']
    songName = resp['item']['name']
    if printOut:
        print("Song: {} by {} in {}\nPlaying: {}\nTotal Time:\t\t{} mins and {} seconds\nCurrent Progress:\t{} mins and {} seconds".\
              format(resp['item']['name'], resp['item']['album']['artists'][0]['name'], resp['item']['album']['name'], resp['is_playing'],
                    int((resp['item']['duration_ms']/(1000*60))%60), int((resp['item']['duration_ms']/1000)%60),
                    int((resp['progress_ms']/(1000*60))%60), int((resp['progress_ms']/1000)%60)))
    return playing, albumName,artistName, duration, progress, songName
def generateYTLink(songName, artistName, albumName):
    titleName = (songName + " by " +  artistName +  " - " + albumName).strip().replace(" ", "+")
    print(titleName)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.youtube.com/results?search_query=" + titleName)
    firstSong = "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a"
    driver.find_element_by_xpath(firstSong).click()
    songLink = driver.current_url
    driver.quit()
    return songLink
def downloadSong(songLink, containFolder, songName, artistName):
    os.chdir()
    songNameDir = songName+"_"+artistName+"_"+str(random.randint(1,100))
    os.mkdir(songNameDir)
    os.chdir(songNameDir)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songLink])
    fileName = ""
    for i in os.listdir("."):
        if i.endswith(".wav"):
            fileName = i
    orgTotalFile = containFolder + songNameDir + "/" + fileName
    renamed = containFolder + songNameDir + "/" + songName + ".wav"
    os.rename(orgTotalFile,renamed)
    musicFilePath = renamed
    return musicFilePath
def getTextFromPic(imgPath):
    keyDIR = "/Users/kunal/Documents/AAPersonalAIPROJECT/MUSICBEAT/KEYS/ruhacks-312105-8c743209e4a6.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    # [START vision_python_migration_document_text_detection]
    with io.open(imgPath, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    extractText = response.text_annotations[0].description
    #extractText = "GEORGIA\nUSA\nGA\nDL\nDRIVER\'S LICENSE\nDL INSTRUCTIONAL PERMIT\nGovernor:\nBilh\nUNDER 21\n4d DL NO.061914281\n07/10/2004\n3 DOB\npuncak R. More\n9 CLASS CP\n4b EXP\n15 SEX\n06/25/2022\nMT\nBRO\n5-07\"\n18 EYES\nCommissioner\n16 HGT\n17 WGT\n145 lb\nFrunzel Ave\n2 KUNAL\n1 ANEJA\n84202 BLUEHOUSE LN\nALPHARETTA, GA 30022-1459\nFULTON\n12 REST A\n9a END\nNONE\nUS\n4a ISS\n06/25/2020\n07/10/2004\n5 DD 420913097520079585\n"
    extractText = extractText.replace("\n"," ")
    return extractText
def getAddress(txt):
    addresses = pyap.parse(txt, country='US')
    return addresses[0] if len(addresses) > 0 else []





if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)