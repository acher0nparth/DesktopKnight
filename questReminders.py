from twilio.rest import Client

account_sid = "AC28db46872233b9069b4f9ca1f8c8500c"
auth_token = "d3882fe520ea898dd6148dcaa41752ed"
client = Client(account_sid, auth_token)

twiNum = '+17652759944'


def sendQuestTip(tip, number = '+13038812829'):
    message = client.messages.create(
        to=number,
        from_=twiNum,
        body=tip)
