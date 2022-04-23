import requests
import datetime as dt
import smtplib
import time
import os

mail = os.environ['mail']
password = os.environ['password']


lat_lon = {
    "lat": 41.000370,
    "lon": 28.862070,
    "formatted": 0
}

response_sun = requests.get(" https://api.sunrise-sunset.org/json", params=lat_lon)
response_sun.raise_for_status()

sun_data = response_sun.json()
sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

sun_times = (sunrise, sunset)

response = requests.get(url="http://api.open-notify.org/iss-now.json", params=lat_lon)
response.raise_for_status()

response_data = response.json()
print(response_data)

latitude = float(response_data["iss_position"]["latitude"])
longitude = float(response_data["iss_position"]["longitude"])
iss_position = (latitude, longitude)

now = dt.datetime.now()
now_hour = now.hour

while True:
    time.sleep(60)
    if abs(iss_position[0] - lat_lon["lat"]) < 10 and  abs(iss_position[1] - lat_lon["lon"]) < 10 and now.hour < sun_times[0] \
         and now.hour > sun_times[1]:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(mail, password)
            connection.sendmail(from_addr=mail, to_addrs="nuri.tass19@gmail.com", msg=f"Subject:ISS IS ABOVE YOU \n\n \
            position is {iss_position}.")


