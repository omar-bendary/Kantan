from twilio.rest import Client
import random


def send_sms(number, OTP):

    # Your Account SID from twilio.com/console
    account_sid = "AC625ce292d44b2c21fa81bde1ae421d36"
    # Your Auth Token from twilio.com/console
    auth_token = "b0d7b6924a5f5b182dfa87380df4b5d2"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=number,
        from_="+1 662 767 6975",
        body=f"Your OTP number is : {OTP}")

    print(message.sid)
    return OTP


# send_sms('+201124250328', 132244)
