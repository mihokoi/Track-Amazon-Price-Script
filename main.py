from bs4 import BeautifulSoup
import lxml
import requests
import os
import smtplib

PASS = os.environ['PASS']
SENDER = os.environ['SENDER']
RECEIVER = os.environ['RECEIVER']

BUY_PRICE = 100

url = "https://www.amazon.com/PlayStation-DualSense-Wireless-Controller-Galactic-5/dp/B09RBZ134K/ref=sr_1_1?crid=2L08RM9SD4D03&keywords=ps5&qid=1654266353&sprefix=ps%2Caps%2C434&sr=8-1"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
          'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'}

result = requests.get(url, headers=header).text


soup = BeautifulSoup(result, 'lxml')
price = float(soup.find(name='span', class_='a-offscreen').getText().replace("$", ""))
title = soup.find(id="productTitle").getText().strip()
print(title)

if price < BUY_PRICE:
    try:
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            result_ = connection.login(SENDER, PASS)
            message = f"{title} is now {price}"
            connection.sendmail(from_addr=SENDER, to_addrs=RECEIVER,
                                msg=f"Subject:Amazon Price Alert!\n\n {message}\n{url}".encode("utf-8"))

    except:
        print("Something went wrong while sending email!")

