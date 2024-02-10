import cloudinary
from cloudinary.uploader import upload
import json

with open("keys.json") as file:
    keyData = json.load(file)

key = keyData["cloud_key"]
keySecret = keyData["cloud_keySecret"]
cloudName = keyData["cloudName"]

def cloudinaryImageUpload(name,localName):
    cloudinary.config(cloud_name = cloudName, api_key = key, api_secret = keySecret, secure = True)
    url = upload(localName, public_id=name)["url"]

def cloudinaryVideoUpload(name,localName):
    cloudinary.config(cloud_name=cloudName, api_key=key, api_secret=keySecret, secure=True)
    url = upload(localName, public_id=name, resource_type="video")["url"]


if __name__ == "__main__":
    cloudinaryVideoUpload("test","fileDump/portraitVid.mp4")

