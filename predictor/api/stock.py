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

    # Preprocess Data 
    close_data = []
    for price in df.close: 
        close_data.append(price)
    x_train, y_train = train_data(10, close_data[:200])
    x_test, y_test = test_data(10, close_data[200:])
    actual = y_test
    
    print (x_train.shape, file=sys.stderr)
    print (x_test.shape, file=sys.stderr)
    x_train = x_train.reshape(189, 10, 1) / 200
    y_train = y_train / 200

    print (x_train, file=sys.stderr)
    print (y_train, file=sys.stderr)
    x_test = x_test.reshape(42, 10, 1) / 200
    y_test = y_test / 200

    # Create LSTM model using Keras
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(20, input_shape=(10, 1), return_sequences=True))
    model.add(tf.keras.layers.LSTM(20))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))

    model.compile(optimizer="adam", loss="mean_squared_error")

    # Fit model to training data and predict on the test data
    model.fit(x_train, y_train, epochs=50)
    
    predictions = []
    for prediction in model.predict(x_test):
        predictions.append(prediction[0] * 200)
    start_index = len(df.index) - len(predictions)
    modified_index = df.index[start_index:]

    # Generate Plot
    fig, ax = plt.subplots()
    ax.set_title("Price Predictions for " + stock + " Stock")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.plot(modified_index, actual, color="blue", label="Actual Stock Prices")
    ax.plot(modified_index, predictions, color="green", label="Predicted Stock Prices")    
    plt.legend(loc="upper left")
    
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
        x_train.append(np.array(data[i: i + train_size]))
        y_train.append(np.array(data[i + train_size], np.float64))
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train, y_train

def test_data(test_size, data):
    x_test = []
    y_test = []
    for i in range(len(data) - test_size - 1):
        x_test.append(np.array(data[i: i + test_size]))
        y_test.append(np.array(data[i + test_size], np.float64))
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    return x_test, y_test