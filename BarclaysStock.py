from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # think this is his weird way of getting his info..
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Market Summary > BARC barclays'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS  # or another email..

barclays_page = requests.get('https://finance.yahoo.com/quote/BARC.L?p=BARC.L&.tsrc=fin-srch')
barclays_soup = BeautifulSoup(barclays_page.content, 'html.parser')  # web scrape tools

# times of notifications

closeTime = '16:00PM'  # roughly


def getBarclaysStockPriceInfo():
    currentDateTime = datetime.datetime.now()
    currentDay = currentDateTime.isoweekday()

    barclays_stock_containers = barclays_soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    barclays_stock_price = barclays_stock_containers[0].find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')

    barclays_stock_stats_positive = barclays_stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    barclays_stock_stats_negative = barclays_stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($negativeColor)')
    barclays_td = barclays_soup.find_all('td')
    day_range = barclays_td[9]
    currentTime = currentDateTime.strftime("%H:%M")

    if not barclays_stock_stats_negative:  # checks if positive or negative as the class changes depending on which one
        barclays_stock_stats = barclays_stock_stats_positive
    else:
        barclays_stock_stats = barclays_stock_stats_negative

    # print("Current time:", currentTime)  # current time
    print("Market Summary > BARC barclays")
    print("-----------------------------------")
    print("Current stock price: ", barclays_stock_price.get_text(), barclays_stock_stats.get_text())
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
                        <h1>Barclays stock:</h1>
                        <h2>Current stock price: {barclays_stock_price}, {barclays_stock_stats}, <h4>Pence sterling (GBX)</h4></h2>
                        <p>Stock Market: {stockMarket}</p>
                        <p>{day_range}</p>

                    </body>
                </html>
                """.format(stockMarket=stockMarket, barclays_stock_price=barclays_stock_price,
                           barclays_stock_stats=barclays_stock_stats, day_range=day_range),
                        subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("sending stock info email")


def getBarclaysStockPriceChangeInfo():
    barclays_stock_containers = barclays_soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')
    barclays_stock_price = barclays_stock_containers[0].find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)')
    barclays_stock_stats = barclays_stock_containers[0].find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)')
    barclays_td = barclays_soup.find_all('td')
    barclays_day_range = barclays_td[9]
    barclays_original_stock_priceFloat = 90     # ??just set this for the start..?
    barclays_stock_priceFloat = float(barclays_stock_price.get_text())  # the number that we can now use for maths comparisons..
    barclays_stock_update_difference = barclays_original_stock_priceFloat - barclays_stock_priceFloat
    barclays_stock_price_alert_difference_for_barclays = 5  # !!Can change this!!
    barclays_stock_price_change = round(barclays_stock_update_difference, 2)
    stockMarket = "open"

    print("Checking for change in stock market")

    if abs(barclays_stock_update_difference) > barclays_stock_price_alert_difference_for_barclays:
        print("Stock price has changed:")
        print("-----------------------------------")
        print("Stock price change: ", barclays_stock_price_change)
        print("Current stock price: ", barclays_stock_price.get_text(), barclays_stock_stats.get_text())
        print("Day's Range: ", barclays_day_range.get_text())
        print("-----------------------------------")
        msg.add_alternative("""\
                    <!DOCTYPE html>
                    <html>
                        <body>
                            <h1>Barclays Stock: </h1>
                            <h2>*Stock price change: {stock_price_change}*</h2>
                            <h2>Current stock price: {stock_price}, {stock_stats}, <h4>Pence sterling (GBX)</h4></h2>
                            <p>Stock Market: {stockMarket}</p>
                            <p>{day_range}</p>

                        </body>
                    </html>
                    """.format(stock_price_change=barclays_stock_price_change, stockMarket=stockMarket, stock_price=barclays_stock_price,
                               stock_stats=barclays_stock_stats,
                               day_range=barclays_day_range), subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)
            print("sending email stocks have changed")
