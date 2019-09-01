import requests

def getQuote(func, symbol):
    """
    Gets JSON string for desired quote. Below is documentation for Alpha Vantage requests:
    Available function:
        INTRADAY
        DAILY
        DAILY_ADJUSTED
        WEEKLY
        WEEKLY_ADJUSTED
        MONTHLY
        MONTHLY_ADJUSTED
    symbol -> Quote
    """
    key = "JMHNDOFOZTWO5N9G"
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_{}&symbol={}.SA&apikey={}".format(func.upper(), symbol.upper(), key)

    response = requests.get(url)
    return response