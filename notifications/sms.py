import africastalking
import os

username = "sandbox"  # your AT username
api_key = os.getenv("AFRICASTALKING_API_KEY")  # store this safely

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print(response)
    except Exception as e:
        print("SMS error:", e)
# Example usage
# from notifications.sms import send_sms

# send_sms("+254712345678", "Your rent payment was received successfully.")
