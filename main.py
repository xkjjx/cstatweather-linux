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
    setAccessToken("EAAQ0HFZAgp20BOZCUx5N8Eu6HfXGSln3kFZA2GSdkUmUwr2vq5rZB1xJ6eWJFO3IsbGZArjDwlrwlCWUqLqEY4l6h1w8ZClqW5ZAd3GZCfveGyNWK8avjiw9ifhPvpgfxAnyNwUQ1GOQn58ZBqW8AV84vz9wIqUGhxpEJiLSkaLMaert6YmWROZCZC8GEKwshL33tDoWOpd3W6qKkNG0AKQaZAzmZCpekuyLr")
    #renewToken()
    postOnIG()
    #postOnTwitter()
    # postOnIG()
    # renewToken()
    sendEmail("Success")
