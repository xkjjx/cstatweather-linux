from twitterBot import postOnTwitter
from instagramBot import postOnIG,renewToken,setAccessToken
from sendEmail import sendEmail


def postAll():


    messageContent = ""
    postOnTwitter()
    messageContent += "Post was successfully made on Twitter.\n"

    try:
        postOnIG()
        renewToken()
        messageContent += "Post was successfully made on Instagram and token was updated.\n"
    except:
        renewToken()
        postOnIG()
        messageContent += "Post was successfully made on Instagram after updating the token.\n"

    sendEmail(messageContent)



if __name__ == "__main__":
    postAll()
