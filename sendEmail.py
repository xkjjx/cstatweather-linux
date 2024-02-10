import smtplib
import json
from email.message import EmailMessage


def sendEmail(text):
    serverName = "smtp.gmail.com"
    port = 465
    server = smtplib.SMTP_SSL(serverName, port)
    with open("keys.json") as file:
        data = json.load(file)
        email, password = data["email"], data["emailPassword"]

    message = EmailMessage()
    message["From"], message["To"] = email, email
    message["Subject"] = "Twitter and Instagram Bot Update"
    message.set_content(text)
    server.login(email, password)
    server.send_message(message)
