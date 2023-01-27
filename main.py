from flask import Flask,jsonify
import requests
import pandas as pd 
import json
from datetime import datetime
from datetime import timedelta



app = Flask(__name__)

headers = {'Authorization': 'Bearer F3NeiLJ8TesDDcqnM5Ix38ZMgyHHYDsre8BD5aMA'}

def get_stocks(time_period):
    if(time_period != None):
        publishedAfter = datetime.utcnow() - timedelta(days = int(time_period))
    else:
        publishedAfter = datetime.utcnow() - timedelta(days = 1)
    publishedAfterUTC = publishedAfter.strftime('%Y-%m-%dT%H:%M:%S')

    response = requests.get(f'https://api.marketaux.com/v1/news/all?sort=entity_sentiment_score&group_similar=false&published_after={publishedAfterUTC}', headers=headers)
    if response.status_code != 200:
        raise ValueError("Impossible de récupérer les données de l'API")

    data = json.loads(response.content)
    stocks = []
    for article in data['data']:
        stocks.extend(article['entities'])

    return stocks

def getStocksByIndustry(industry):
    print(f'https://api.marketaux.com/v1/news/all?group_similar=false&industries={industry}')
    response = requests.get(f'https://api.marketaux.com/v1/news/all?group_similar=false&industries={industry}', headers=headers)
    if response.status_code != 200:
        raise ValueError("Impossible de récupérer les données de l'API")

    data = json.loads(response.content)
    stocks = []
    for article in data['data']:
        stocks.extend(article['entities'])

    return stocks

def groupStocksByCountryAndIndustry(stocks):
    grouped_stocks = {}
    for stock in stocks:
        if(stock['country'] not in grouped_stocks):
            grouped_stocks[stock['country']] = { }
        if(stock['industry'] not in grouped_stocks[stock['country']]):
            grouped_stocks[stock['country']][stock['industry']] = []
        grouped_stocks[stock['country']][stock['industry']].append(stock)
    return grouped_stocks

@app.route('/api/top-performing-stocks/', defaults = {'time_period': None}, methods=['GET'])
@app.route('/api/top-performing-stocks/<time_period>', methods=['GET'])
def top_performing_stocks(time_period):
    stocks = get_stocks(time_period)
    grouped_stocks = groupStocksByCountryAndIndustry(stocks)
    return jsonify(grouped_stocks)

@app.route('/api/stocks-by-industry/<industry>', methods=['GET'])
def stocks_by_industry(industry):
    stocks = getStocksByIndustry(industry)
    return jsonify(stocks)
if (__name__== '__main__'):
    app.run(debug=True)