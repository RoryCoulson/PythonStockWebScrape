from schedule import *
import schedule
from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # think this is his weird way of getting his info..
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Market Summary > Coca-Cola Co'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS  # or another email..

page = requests.get('https://finance.yahoo.com/quote/KO/')
soup = BeautifulSoup(page.content, 'html.parser')  # web scrape tools

# times of notifications

closeTime = '17:02PM'  # roughly


def getStockPriceInfo():
    currentDateTime = datetime.datetime.now()
    currentDay = currentDateTime.isoweekday()

    stock_containers = soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    stock_price = stock_containers[0].find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')

    stock_stats_positive = stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    stock_stats_negative = stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($negativeColor)')
    td = soup.find_all('td')
    day_range = td[9]
    currentTime = currentDateTime.strftime("%H:%M")

    if not stock_stats_negative:        # checks if positive or negative as the class changes depending on which one
        stock_stats = stock_stats_positive
    else:
        stock_stats = stock_stats_negative

    print(stock_containers)
    print("Current time:", currentTime)  # current time
    print("Market Summary > Coca-Cola Co")
    print("-----------------------------------")
    print("Current stock price: ", stock_price.get_text(), stock_stats.get_text())
    print("Day's Range: ", day_range.get_text())
    stockMarket = "open"

    if currentTime > closeTime or currentDay >= 6:
        stockMarket = "closed"
        print("Stock Market: ", stockMarket)
    else:
        print("Stock Market: ", stockMarket)

    print("-----------------------------------")

    msg.add_alternative("""\
            <!DOCTYPE html>
            <html>
                <body>
                    <h1>Coca Cola Stocks:</h1>
                    <h2>Current stock price: {stock_price}, {stock_stats}</h2>
                    <p>Stock Market: {stockMarket}</p>
                    <p>{day_range}</p>

                </body>
            </html>
            """.format(stockMarket=stockMarket, stock_price=stock_price, stock_stats=stock_stats, day_range=day_range),
                        subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("sending stock info email")


def getStockPriceChangeInfo():
    stock_containers = soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    stock_price = stock_containers[0].find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')
    stock_stats = stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    td = soup.find_all('td')
    day_range = td[9]
    original_stock_priceFloat = 48  # ??just set this for the start..?
    stock_priceFloat = float(stock_price.get_text())  # the number that we can now use for maths comparisons..
    stock_update_difference = original_stock_priceFloat - stock_priceFloat
    stock_price_alert_difference = 3  # !!
    stock_price_change = round(stock_update_difference, 2)
    stockMarket = "open"

    print("Checking for change in stock market")

    if abs(stock_update_difference) > stock_price_alert_difference:
        print("Stock price has changed:")
        print("-----------------------------------")
        print("Stock price change: ", stock_price_change)
        print("Current stock price: ", stock_price.get_text(), stock_stats.get_text())
        print("Day's Range: ", day_range.get_text())
        print("-----------------------------------")
        msg.add_alternative("""\
                <!DOCTYPE html>
                <html>
                    <body>
                        <h1>Coca Cola Stocks: </h1>
                        <h2>*Stock price change: {stock_price_change}*</h2>
                        <h2>Current stock price: {stock_price}, {stock_stats}</h2>
                        <p>Stock Market: {stockMarket}</p>
                        <p>{day_range}</p>

                    </body>
                </html>
                """.format(stock_price_change=stock_price_change, stockMarket=stockMarket, stock_price=stock_price,
                           stock_stats=stock_stats,
                           day_range=day_range), subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("sending email stocks have changed")


print("Welcome to Coca Cola Stocks python program")
print("Time is: ", datetime.datetime.now())  # date time stamp
morning = "08:00"
mid_day = "12:30"
# sends email at morning, mid day and 4, about the stock status
schedule.every().day.at(morning).do(getStockPriceInfo)
schedule.every().day.at(mid_day).do(getStockPriceInfo)
schedule.every().day.at("17:24").do(getStockPriceInfo)

# this will check if the change in price is significant and then send an email if so
schedule.every(30).seconds.do(getStockPriceChangeInfo)

while True:
    currentDateTimee = datetime.datetime.now()
    currentDayy = currentDateTimee.isoweekday()

    if currentDayy < 6:  # not a weekend
        schedule.run_pending()

    time.sleep(1)
