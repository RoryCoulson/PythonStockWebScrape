from schedule import *
import schedule
import datetime
import BarclaysStock
import CineworldStock
import CokeStock

print("Welcome to Rory's tracking Stocks python program")
print("Time is: ", datetime.datetime.now())  # date time stamp
morning = "08:00"
mid_day = "12:30"
# sends email at morning, mid day and 4, about the stock status
# coke
schedule.every().day.at(morning).do(CokeStock.getCokeStockPriceInfo)
schedule.every().day.at(mid_day).do(CokeStock.getCokeStockPriceInfo)
schedule.every().day.at("17:24").do(CokeStock.getCokeStockPriceInfo)
# barclays
schedule.every().day.at(morning).do(BarclaysStock.getBarclaysStockPriceInfo)
schedule.every().day.at(mid_day).do(BarclaysStock.getBarclaysStockPriceInfo)
schedule.every().day.at("17:24").do(BarclaysStock.getBarclaysStockPriceInfo)
# cineworld
schedule.every().day.at(morning).do(CineworldStock.getCineworldStockPriceInfo)
schedule.every().day.at(mid_day).do(CineworldStock.getCineworldStockPriceInfo)
schedule.every().day.at("17:24").do(CineworldStock.getCineworldStockPriceInfo)

# this will check if the change in price is significant and then send an email if so
schedule.every(30).seconds.do(CokeStock.getCokeStockPriceChangeInfo)
schedule.every(30).seconds.do(BarclaysStock.getBarclaysStockPriceChangeInfo)
schedule.every(30).seconds.do(CineworldStock.getCineworldStockPriceChangeInfo)

while True:
    currentDateTimee = datetime.datetime.now()
    currentDayy = currentDateTimee.isoweekday()

    if currentDayy < 6:  # not a weekend
        schedule.run_pending()

    time.sleep(1)
