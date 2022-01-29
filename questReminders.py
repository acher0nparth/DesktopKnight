from twilio.rest import Client
from configparser import ConfigParser

smsInfo = ConfigParser()
smsInfo.read("config.cfg")

accountInfo = smsInfo["TWILIOINFO"]
account_sid = accountInfo["account_sid"]
auth_token = accountInfo["auth_token"]

client = Client(account_sid, auth_token)

def sendQuestTip(tip):
    print(account_sid)
    message = client.messages.create(
        to=accountInfo["to"],
        from_=accountInfo["from"],
        body=tip)
