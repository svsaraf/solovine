import requests
from .secrets import *

def send_registration_email(to_email):
    link = "https://api.mailgun.net/v3/mg.solovine.com/messages"
    auth = ("api", mailgun_api)
    data = {"from": "Solovine Robot robot@solovine.com",
              "to": [to_email],
              "subject": "Welcome to Solovine!",
              "text": "Welcome to Solovine! My hope is that this will be the place you can have intelligent discussions with your contacts. Feel free to send a note to founder@solovine.com with any feedback.\n\nThanks!\nSanjay"}
    requests.post(link, auth=auth, data=data)

def send_password_reset(to_email, newpassword):
    link = "https://api.mailgun.net/v3/mg.solovine.com/messages"
    auth = ("api", mailgun_api)
    text = "Forgetful eh? Your new password is %s. Feel free to log in to solovine with your email and password!" % (newpassword,)
    data = {"from": "Solovine Robot robot@solovine.com",
              "to": [to_email],
              "subject": "Solovine Password Reset",
              "text": text}
    requests.post(link, auth=auth, data=data)
