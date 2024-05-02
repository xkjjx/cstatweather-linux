from postGenerator import createPostText
import time
import requests
import json

cstatPlaceID = 4682464

with open("/app/src/keys.json") as file:
    keyData = json.load(file)


appID = keyData["IG_appID"]
appSecret = keyData["IG_appSecret"]
accessToken = keyData["IG_accessToken"]
pageID = keyData["IG_pageID"]
igAccountID = keyData["IG_igAccountID"]
accessURL = keyData["IG_accessURL"]
graphURL = keyData["IG_graphURL"]

def IGImageURL(ctime):
    year, month, day, hour, minute, sec, wday, tday, dst = ctime
    if day < 9:
        day = "0" + str(day)
    else:
        day = str(day)

    if month < 9:
        month = "0" + str(month)
    else:
        month = str(month)

    return "https://res.cloudinary.com/dzygv07en/image/upload/" + str(3600*hour + 60*minute + sec) + month + "/" + day + "/" + str(year)


def IGVideoURL(ctime):
    year, month, day, hour, minute, sec, wday, tday, dst = ctime
    if day < 9:
        day = "0" + str(day)
    else:
        day = str(day)

    if month < 9:
        month = "0" + str(month)
    else:
        month = str(month)

    return "https://res.cloudinary.com/dzygv07en/video/upload/" + str(3600*hour + 60*minute + sec) + month + "/" + day + "/" + str(year)

def cstatTime():
    return time.localtime()


def renewToken():
    url = graphURL + "oauth/access_token"
    param = {"grant_type":"fb_exchange_token","client_id":appID,"client_secret":appSecret,"fb_exchange_token":accessToken}
    response = requests.get(url=url,params=param).json()
    print("Instagram access token renewed!")
    with open("/app/src/keys.json") as file:
        keyData = json.load(file)
    keyData["accessToken"] = response["access_token"]
    with open("/app/src/keys.json","w") as file:
        json.dump(keyData,file)



def uploadImage(imageURL,caption):
    try:
        url = graphURL + igAccountID + "/media"
        param = {"access_token":accessToken,"caption":caption,"image_url":imageURL
                #,"media_type":"STORIES"
                }
        response = requests.post(url,params=param)
        response = response.json()
    except:
        print("Error in uploading image to Instagram")
        response = None
    
    return response

def uploadVideo(videoURL,caption):
    try:
        url = graphURL + igAccountID + "/media"
        print(url)
        param = {"access_token":accessToken,"caption":caption,"video_url":videoURL,"media_type":"REELS"}
        response = requests.post(url,params=param)
        response = response.json()
    except:
        print("Error in uploading video to Instagram")
        response = None
    return response


def postOnIG():
    ctime = cstatTime()
    caption,imageSaved = createPostText(cstatPlaceID,ctime,False)
    if imageSaved:
        try:
            picURL = IGVideoURL(ctime)
            response = uploadVideo(picURL,caption)
            time.sleep(20)
            #print(response)
            print("Instagram Image URL:\n" + picURL)
            print("Instagram Post Text:\n" + caption)
            print(response)
            containerID = response['id']
            url = graphURL + igAccountID + "/media_publish"
            param = {"access_token":accessToken,"creation_id":containerID}
            response = requests.post(url,params=param)
            print("Succesfully posted on Instagram\n")
        except:
            print("Error in posting on Instagram\n")
    else:
        print("No image found - Instagram post not completed\n")

def setAccessToken(token):
    with open("/app/src/keys.json") as file:
        info = json.load(file)
        info["IG_accessToken"] = token
    with open("/app/src/keys.json","w") as file:
        json.dump(info,file)


