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
from matplotlib.figure import Figure


@predictor.app.route('/stock', methods=['GET'])
def get_stock():
    """Return stock information view API to be rendered by template"""
    # Store variables 
    stock = flask.request.args.get('stock')
    alphavantage_key = '15H46IQZLXKESHV4'
    now = datetime.datetime.now()
    start = datetime.datetime(2019, 1, 1)
    end = datetime.datetime(now.year, now.month, now.day)

    # Use Pandas DataReader to read in historical stock data
    df = web.DataReader(stock, "av-daily", start, end, api_key=alphavantage_key)

    # Generate Plot
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Price Predictions for " + stock + " Stock")
    axis.set_xlabel("Date")
    axis.set_ylabel("Closing Price")
    axis.grid() 
    axis.plot(df.index, df.close)
    

    # Convert Plot to PNG Image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    return Response(pngImage.getvalue(), mimetype='image/png')
    # Encode PNG image to base64 string
    # pngImagesB64String = "data:image/png;base64,"
    # pngImagesB64String += base64.b64encode(pngImage.getvalue().decode('utf8'))

    context = {"stock" : stock,
               "image" : pngImage}
    return flask.render_template("stock.html", **context)