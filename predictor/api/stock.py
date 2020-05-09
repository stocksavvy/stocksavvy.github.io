"""REST API for individual stock pages."""
import os
import sys
import io
import base64
import flask
from flask import Response
import predictor
import datetime
import pandas as pd
import pandas_datareader.data as web
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


@predictor.app.route('/stock', methods=['GET'])
def get_stock():
    """Return stock information view API to be rendered by template"""
    # Store stock variable
    stock = flask.request.args.get('stock')
    context = {"stock" : stock}

    return flask.render_template("stock.html", **context)

@predictor.app.route('/<stock>-plot.png')
def get_graph(stock):
    alphavantage_key = '15H46IQZLXKESHV4'
    now = datetime.datetime.now()
    start = datetime.datetime(2019, 1, 1)
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
    
    # for n, label in enumerate(ax.xaxis.get_ticklabels()):
    #     if n % 1000 != 0:
    #         label.set_visible(False)
    

    # Convert Plot to PNG Image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    return Response(pngImage.getvalue(), mimetype='image/png')
