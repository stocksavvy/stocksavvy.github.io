"""REST API for individual stock pages."""
import os
import sys
import io
import base64
import flask
from urllib.request import urlopen
from flask import Response
import predictor
import datetime
import pandas as pd
import pandas_datareader.data as web
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np 
import tensorflow as tf


@predictor.app.route('/stock', methods=['GET'])
def get_stock():
    """Return stock information view API to be rendered by template"""
    # Store upper-case version of stock variable
    stock = flask.request.args.get('stock').upper()
    
    # Generate list of NASDAQ stocks
    symbols_url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
    stocks_list = []
    f = urlopen(symbols_url)
    lines = f.readlines()
    for i,line in enumerate(lines):
        if i != 0 and i != len(lines) - 1:
            splits = str(line).split('|')
            raw_stock = splits[0]
            stocks_list.append(raw_stock[2:])

    # Generate context dict
    context = {"stock" : stock}

    # Check if user stock is valid
    if stock not in stocks_list:
        return flask.render_template("invalid.html", **context)

    return flask.render_template("stock.html", **context)

@predictor.app.route('/<stock>-plot.png')
def get_graph(stock):
    # Define variables for data to be read
    alphavantage_key = '15H46IQZLXKESHV4'
    now = datetime.datetime.now()
    # Dates to reflect past 1 year of historical data
    start = datetime.datetime(now.year - 1, now.month, now.day)
    end = datetime.datetime(now.year, now.month, now.day)

    # Use Pandas DataReader to read in historical stock data
    df = web.DataReader(stock, "av-daily", start, end, api_key=alphavantage_key)

    # Generate Plot
    fig, ax = plt.subplots()
    ax.set_title("Price Predictions for " + stock + " Stock")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.plot(df.index, df.close)
    
    
    # Find at most 5 ticks on the y-axis at 'nice' locations
    max_xticks = 5
    xloc = plt.MaxNLocator(max_xticks)
    ax.xaxis.set_major_locator(xloc)

    # Convert Plot to PNG Image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    return Response(pngImage.getvalue(), mimetype='image/png')

def train_data(train_size, data):
    x_train = []
    y_train = []
    for i in range(len(data) - train_size - 1):
        x_train.append(np.array(data.iloc[i: i + train_size, 1]))
        y_train.append(np.array(data.iloc[i + train_size + 1, 1], np.float64))
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train, y_train

def test_data(test_size, data):
    x_test = []
    y_test = []
    for i in range(len(data) - test_size - 1):
        x_test.append(np.array(data.iloc[i: i + test_size, 1]))
        y_test.append(np.array(data.iloc[i + test_size + 1, 1], np.float64))
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    return x_test, y_test