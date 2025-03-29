import requests
from fastapi import HTTPException
import variabless
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def weather(city_name : str, api_key:str): 
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    print(city_name)
    try:
        response = requests.get(api_url)
        data = response.json()
        if data["cod"] == 200:
            coord = data["coord"]
            content = f"Latitude = {coord['lat']}\n"
            content+= f"Longitude = {coord['lon']}\n"
            main = data["main"]
            content+= f"Temperature = {main['temp']} °C\n"
            content+= f"Feels Like = {main['feels_like']} °C\n"
            sys = data["sys"]
            content+= f"Country = {sys['country']}\n"
            desc = data["weather"]
            content+= f"Weather = {desc[0]['description']}"
            print(content)
            status = send_email(
                sender_email=variabless.get_sender(),
                sender_password=variabless.get_passkey(),
                recipient_email=variabless.get_recipient(),
                subject=f"{city_name} weather updates",
                body=content
            )
            if(status==1):
                return response.json()
            else:
                 raise HTTPException(status_code=500, detail="Email sending failed")
        else:
            raise HTTPException(status_code=int(data["cod"]), detail=data["message"])
    except Exception:
        raise


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Set up the email details
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    status =0
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server (e.g., Gmail's server)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in
        server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email
        print("Email sent successfully!")
        status=1
    except Exception as e:
        print(f"Failed to send email: {e}")
        status=0
    finally:
        server.quit()  # Disconnect from the server
        return status