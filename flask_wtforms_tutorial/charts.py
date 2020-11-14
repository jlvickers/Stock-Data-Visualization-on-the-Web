'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests as rq
import json
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()
apiKey = "B82J6IGU3OII6QCA"
apiURL = "https://www.alphavantage.co/query"
def StockModel(self, data):
    self.open = float(data['1. open'])
    self.high = float(data['2. high'])
    self.low = float(data['3. low'])
    self.close = float(data['4. close'])
    self.volume = data['5. volume']
def queryStockData(symbol, chartType, timeSeries, startDate, endDate):
    ts = {
        "1": "INTRADAY",
        "2": "DAILY",
        "3": "WEEKLY",
        "4": "MONTHLY"
    }
    #API Query paramters
    series = "TIME_SERIES_" + ts[timeSeries]
    data = {
        "function": series,
        "symbol": symbol,
        "outputsize":"full",
        "interval":"60min",
        "apikey": apiKey
    }

    #Sending our request to the API using the information we put in the data collection.
    apiCall = rq.get(apiURL, params=data)

        #Stores the json-enconded content in the retrieved data.
    response = apiCall.json()
        
        # If statements to change key depending on the Time Serires selected. 
    if series == "TIME_SERIES_DAILY":
        timeSeries = "Time Series (Daily)"
    elif series == "TIME_SERIES_INTRADAY":
        timeSeries = "Time Series (60min)"
    elif series == "TIME_SERIES_WEEKLY":
        timeSeries = "Weekly Time Series"
    elif series == "TIME_SERIES_MONTHLY":
        timeSeries = "Monthly Time Series"
        
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    #Parsing the dates from the user input
    #startDate = datetime.fromisoformat(startDate)
    #endDate = datetime.fromisoformat(endDate)
    for d, nums in response[timeSeries].items():
        #Parsing the date from the api record.
        if timeSeries == "Time Series (60min)":
            entryDate = datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date()
        else:
            entryDate = datetime.strptime(d, '%Y-%m-%d').date()
        #entryDate = date.fromisoformat(d)
        #entryDate = date
        #Populating lists with data, within the given date range, from API 
        if (entryDate >= startDate and entryDate <= endDate):
            opens.append(float(nums["1. open"]))
            highs.append(float(nums["2. high"]))
            lows.append(float(nums["3. low"]))
            closes.append(float(nums["4. close"]))
            dates.append(d)
    dates.reverse()
    opens.reverse()
    highs.reverse()
    lows.reverse()
    closes.reverse()
        #If true, prints line chart. Else prints the bar chart.
    if chartType == "2":
        chart = pygal.Line(x_label_rotation=45)
        chart.x_labels = dates
        chart.title = "Stock Date for " + symbol + ": " + str(startDate) + " to " + str(endDate)
        chart.add("Open",opens)
        chart.add("High",highs)
        chart.add("Low", lows)
        chart.add("Close",closes)
        #chart.render_in_browser()
        return chart.render()
    else:
        chart = pygal.Bar(x_label_rotation=45)
        chart.title = "Stock Date for " + symbol + ": " + str(startDate) + " to " + str(endDate)
        chart.x_labels = dates
        chart.add("Open",opens)
        chart.add("High",highs)
        chart.add("Low", lows)
        chart.add("Close",closes)
        #chart.render_in_browser()
        return chart.render()