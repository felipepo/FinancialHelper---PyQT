from ..Stock import data
import json

def run_test():
    response = data.getQuote("daily", "petr4")
    loaded = json.loads(response.content)
    pr = 1