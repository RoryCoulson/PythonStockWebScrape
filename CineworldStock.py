from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import os
from email.message import EmailMessage


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # think this is his weird way of getting his info..
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Market Summary > Cineworld'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS  # or another email..

cineworld_page = requests.get('https://finance.yahoo.com/quote/CINE.L?p=CINE.L&.tsrc=fin-srch')
cineworld_soup = BeautifulSoup(cineworld_page.content, 'html.parser')  # web scrape tools

# times of notifications

closeTime = '16:00PM'  # roughly


def getCineworldStockPriceInfo():
    currentDateTime = datetime.datetime.now()
    currentDay = currentDateTime.isoweekday()

    cineworld_stock_containers = cineworld_soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    cineworld_stock_price = cineworld_stock_containers[0].find(
        class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')

    cineworld_stock_stats_positive = cineworld_stock_containers[0].find(
        class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    cineworld_stock_stats_negative = cineworld_stock_containers[0].find(
        class_='Trsdu(0.3s) Fw(500) Fz(14px) C($negativeColor)')
    cineworld_td = cineworld_soup.find_all('td')
    day_range = cineworld_td[9]
    currentTime = currentDateTime.strftime("%H:%M")

    if not cineworld_stock_stats_negative:  # checks if positive or negative as the class changes depending on which one
        cineworld_stock_stats = cineworld_stock_stats_positive
    else:
        cineworld_stock_stats = cineworld_stock_stats_negative

    print(cineworld_stock_containers)
    print("Current time:", currentTime)  # current time
    print("Market Summary > Cineworld")
    print("-----------------------------------")
    print("Current stock price: ", cineworld_stock_price.get_text(), cineworld_stock_stats.get_text())
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
                    <h1>Cineworld Stocks:</h1>
                    <h2>Current stock price: {cineworld_stock_price}, {cineworld_stock_stats} <h4>GBX</h4></h2>
                    <p>Stock Market: {stockMarket}</p>
                    <p>{day_range}</p>

                </body>
            </html>
            """.format(stockMarket=stockMarket, cineworld_stock_price=cineworld_stock_price,
                       cineworld_stock_stats=cineworld_stock_stats,
                       day_range=day_range),
                        subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("sending stock info email")


def getCineworldStockPriceChangeInfo():
    stock_containers = cineworld_soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    stock_price = stock_containers[0].find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')
    cineworld_stock_stats_positive = stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    cineworld_stock_stats_negative = stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($negativeColor)')

    if not cineworld_stock_stats_negative:  # checks if positive or negative as the class changes depending on which one
        stock_stats = cineworld_stock_stats_positive
    else:
        stock_stats = cineworld_stock_stats_negative

    td = cineworld_soup.find_all('td')
    day_range = td[9]
    original_stock_priceFloat = 60  # !!!!TEST this??just set this for the start..?
    stock_priceFloat = float(stock_price.get_text())  # the number that we can now use for maths comparisons..
    stock_update_difference = original_stock_priceFloat - stock_priceFloat  # TEST this
    stock_price_alert_difference_for_cineworld = 5  # !!Can change this!!
    stock_price_change = round(stock_update_difference, 2)
    stockMarket = "open"

    print("Checking for change in stock market")

    if abs(stock_update_difference) > stock_price_alert_difference_for_cineworld:
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
                        <h1>Cineworld Stocks: </h1>
                        <h2>*Stock price change: {stock_price_change}*</h2>
                        <h2>Current stock price: {stock_price}, {stock_stats}<h4>GBX</h4></h2>
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


getCineworldStockPriceChangeInfo()
getCineworldStockPriceInfo()
