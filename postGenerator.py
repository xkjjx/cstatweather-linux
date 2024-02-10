from PIL import ImageDraw,ImageFont,Image
import pyowm
import random
import os
from math import ceil
from cloudinaryUpload import *
from moviepy.editor import ImageClip, AudioFileClip
import time


with open("keys.json") as file:
    keyData = json.load(file)

weatherKey = keyData["weatherKey"]

timeDict = {0: "morning", 1: "morning", 2: "morning", 3: "evening", 4: "night"}
statusDict = {"few clouds": "cloudy", "broken clouds": "cloudy", "overcast clouds": "cloudy",
              "scattered clouds": "cloudy"
    , "clear sky": "clear", "light snow": "clear", "snow": "clear", "light rain": "rain", "moderate rain": "rain"
    , "heavy intensity rain": "heavy_rain",
              "mist":"cloudy"}

def getFileCount(filePath,fileExtension):
    count = 0
    for file in os.listdir(filePath):
        #print(- len(fileExtension),file[- len(fileExtension) - 1:])
        if file[- len(fileExtension) - 1:] == "." + fileExtension:
            count += 1
    return count


def makeVideo(audioFileName,imageFileName="fileDump/portraitpic.jpeg",videoFileName="fileDump/portraitVideo.mp4"):
    audio = AudioFileClip(audioFileName)
    imageClip = ImageClip(imageFileName).set_duration(30)
    video = imageClip.set_audio(audio)
    if video.size[0] > 1080:
        video = video.resize(width=1080,height=1440)
    print(video.size)
    video.write_videofile(videoFileName, fps=30,
                          audio_codec="aac",
                          preset="ultrafast", threads=8)


class FileRotatedIncorrectly(Exception):
    def __init__(self,fileName):
        self.message = "The file " + fileName + " has invalid rotation metadata"
        super().__init__(self.message)


def makeImage(originalImage,temp,timeStr,dateStr):
    #function that draws white text with black border on an image
    def textWithBorder(x,y,size,text):
        border = int(ceil(size / 50))
        textOnImage.text((x- border, y- border), text, font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",size), fill="#000")
        textOnImage.text((x+ border, y- border), text, font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",size), fill="#000")
        textOnImage.text((x- border, y+ border), text, font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",size), fill="#000")
        textOnImage.text((x+ border, y+ border), text, font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",size), fill="#000")
        textOnImage.text((x,y),text=text,fill="#fff",font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",size))

    #opens background image from file name and creates size variables for temperature, time, and tag texts
    background = Image.open(originalImage)
    width,height = background.width,background.height

    #checks to make sure the file is rotated correctly - essential for correct operations
    if (274 in background.getexif().keys()) and (background.getexif()[274] == 6):
        raise FileRotatedIncorrectly(originalImage)
    
    textOnImage = ImageDraw.Draw(background)

    if width > height:
        sizeTemp = int(ceil(width / 4.5))
        xTemp = width / 30
        yTemp = height - sizeTemp

        sizeTag = int(ceil(width / 50))
        xTag = width - 7 * sizeTag
        yTag = height - sizeTag * 4 / 3

        sizeTime = int(ceil(width / 20))
        if len(timeStr)==6:
            xTime = width - 3.75 * sizeTime
        else:
            xTime = width - 4.25 * sizeTime
        yTime = height / 60

        sizeDate = int(ceil(width / 40))
        xDate = width - len(dateStr) * 0.55 * sizeDate
        yDate = height / 12
    else:
        sizeTemp = int(ceil(height / 5))
        xTemp = width / 22.5
        yTemp = height - sizeTemp

        sizeTag = int(ceil(height / 50))
        xTag = width - 7 * sizeTag
        yTag = height - sizeTag * 4 / 3

        sizeTime = int(ceil(height / 20))
        if len(timeStr) == 6:
            xTime = width - 3.75 * sizeTime
        else:
            xTime = width - 4.25 * sizeTime
        yTime = height / 80

        sizeDate = int(ceil(height / 40))
        xDate = width - len(dateStr) * 0.55 * sizeDate
        yDate = height / 16


    #temperature, 176 is ascii for the degree symbol
    text = str(temp) + chr(176)

    #calls the border drawing function to draw temperature, time, and tag
    textWithBorder(xTemp,yTemp,sizeTemp,text)
    textWithBorder(xTag, yTag, sizeTag, "@cstatweather")
    textWithBorder(xTime, yTime, sizeTime,timeStr)
    textWithBorder(xDate,yDate,sizeDate,dateStr)

    #saves picture and closes file
    if width > height:
        background.save("fileDump/landscapePic.jpeg",format="jpeg")
    else:
        background.save("fileDump/portraitpic.jpeg",format="jpeg")
    background.close()


def createPostText(placeID,time,landscape):
    #get weather information from the open weather API
    weather = pyowm.OWM(weatherKey).weather_manager().weather_at_id(placeID)
    #get temperature and round it
    temp = weather.weather.temperature("fahrenheit")["temp"]
    temp = round(temp)
    #get humidity
    humidity = weather.weather.humidity
    #get detailed status of weather
    skies = weather.weather.detailed_status
    #turn detailed status message into a more descriptive sentence
    skyStatusMessage = ""
    if skies == "few clouds":
        skyStatusMessage = "It is slightly cloudy."
    elif skies == "broken clouds":
        skyStatusMessage = "There are a few broken clouds."
    elif skies == "overcast clouds":
        skyStatusMessage = "There are a few rainy clouds."
    elif skies == "scattered clouds":
        skyStatusMessage = "There are a few scattered clouds."
    elif skies == "clear sky":
        skyStatusMessage = "The sky is clear!"
    elif skies == "light snow":
        skyStatusMessage = "There's a bit of snow?!?!"
    elif skies == "snow":
        skyStatusMessage = "It's snowing!!!"
    elif skies == "light rain":
        skyStatusMessage = "It's slightly drizzling."
    elif skies == "moderate rain":
        skyStatusMessage = "It's raining."
    elif skies == "heavy intensity hard":
        skyStatusMessage = "It's raining hard!"
    #space for spacing and gramatical purposes
    skyStatusMessage = " " + skyStatusMessage

    #get data and time from time module
    year, month, day, hour, minute, sec, wday, tday, dst = time
    if day < 9:
        dayStr = "0" + str(day)
    else:
        dayStr = str(day)

    if month < 9:
        monthStr = "0" + str(month)
    else:
        monthStr = str(month)

    dateStr = monthStr + "/" + dayStr + "/" + str(year)
    code = str(hour*3600 + minute*60 + sec) + dateStr

    #set random seed and get a random number to intorduce randomness in the message
    random.seed(year + month + day + hour + minute + sec)
    r = random.randint(0, 100000)

    #get name of the month from its numerical information
    monthDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                 9: "September", 10: "October", 11: "November", 12: "December"}
    month = monthDict[month]

    #add suffix to day
    if day == 1:
        day = str(day) + "st"
    elif day == 2:
        day = str(day) + "nd"
    elif day == 3:
        day = str(day) + "rd"
    else:
        day = str(day) + "th"

    #variable to categorize time into human categorizations
    # 0 is morning, 1 is noon, 2 is afternoon, 3 is evening, 4 is night
    timeSimple = 0

    #add the correct AM/PM suffix while categorizing time by setting the timeSimple variable
    if hour == 0:
        timeSimple = 4
        hour = 12
        sec = str(sec) + "AM"
    elif hour == 12:
        timeSimple = 1
        sec = str(sec) + "PM"
    elif hour > 12:
        if hour > 19:
            timeSimple = 4
        elif hour > 16:
            timeSimple = 3
        else:
            timeSimple = 2
        hour = hour % 12
        sec = str(sec) + "PM"
    else:
        if hour < 6:
            timeSimple = 4
        else:
            timeSimple = 0
        sec = str(sec) + "AM"

    #have "0" precede single digit numbers for clearer consistent time formatting
    if len(sec) == 3:
        sec = "0" + sec
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    hour = str(hour)

    #making the main message
    text = "In College Station, Texas, it is currently {}:{}:{} on {} {}, {} - the weather is {} degrees with a humidity of {}%.{}".format(
        hour, minute, sec, month, day, year, temp, humidity, skyStatusMessage)

    #adding special additions if it's morning with the help of the random number
    if timeSimple == 0:
        if r % 7 == 0:
            text = "Good morning Ags!! " + text + " Hope you have an amazing day!"
        else:
            text = "Good morning Ags! " + text + " Hope you have an amazing day!"

    #adding special additions if it's night with the help of the random number
    elif timeSimple == 4:
        if r % 11 == 0:
            text = text + " Good night:)"
        else:
            text = text + " Good night."

    #adding more special messages with the random variable
    if r % 5 == 0:
        text = text + "\nGig 'em!"

    #adding hashtags and returning the created text
    text = text + "\n#cstat #texasam #tamu #bryan #northgate #collegestation"

    #gets file name of image
    imageFile = timeDict[timeSimple] + os.sep + statusDict[skies]
    audioFile = "music" + os.sep + timeDict[timeSimple]
    audioFile += os.sep + str(r % getFileCount(audioFile,"mp3") + 1) + ".mp3"

    if landscape:
        imageFile = "images" + os.sep + "landscape" + os.sep + imageFile

        # checks if there are any images in the folder - if there is none, returns with imageSaved=False
        # else saves a new image then returns with imageSaved=True
        l = getFileCount(imageFile,"jpeg")

        if l == 0:
            return text, False
        else:
            imageFile = imageFile + os.sep + str(r % l + 1) + ".jpeg"

        # adds temperature information to a background image to create image that will be posted
        makeImage(imageFile, temp, hour + ":" + minute + sec[-2:],dateStr)
        makeVideo(audioFile,"fileDump/landscapePic.jpeg","fileDump/landscapeVid.mp4")
    else:
        imageFile = "images" + os.sep + "portrait" + os.sep + imageFile
        l = getFileCount(imageFile,"jpeg")
        #a = getFileCount()
        if l == 0:
            return text, False
        else:
            imageFile = imageFile + os.sep + str(r % l + 1) + ".jpeg"
        print(imageFile,audioFile)
        makeImage(imageFile,temp,hour + ":" + minute + sec[-2:],dateStr)
        makeVideo(audioFile,"fileDump/portraitpic.jpeg","fileDump/portraitVid.mp4")
        cloudinaryVideoUpload(code,"fileDump/portraitVid.mp4")


    return text,True


if __name__ == "__main__":
    createPostText(4682464,time.localtime(),landscape=True)
    createPostText(4682464,time.localtime(),landscape=False)
