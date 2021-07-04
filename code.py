# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Data Preparation

# ### read data

# +
###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
# For reading, processing, and visualizing data
import numpy as np
import pandas as pd
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import datetime

# To make candlestick charts
from mplfinance.original_flavor import candlestick_ohlc

# For reading files
from os import listdir
# -

df = pd.read_csv('sample_data.csv', encoding='utf-8')
df.rename(columns={'Värdepapper/beskrivning': 'company'}, inplace=True)

data_apple = df[df.company == 'Apple Inc']
print(data_apple)

# ### read stock data

# +
# To create datetime objects 
import datetime

# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# +
# Set label
stocks = ["AAPL"] # If you want to grab multiple stocks add more labels to this list

# Set start and end dates
start = datetime.datetime(2020, 1, 1)
end   = datetime.datetime(2021, 6, 30)

# Grab data
data = pdr.get_data_yahoo(stocks, start = start, end = end)

# +
###############################################################################
#              4a. Visualize Data: Prepare data for Candlestick Chart         #
###############################################################################
# Get Open, High, Low, Close
ADI_candle   = data.iloc[:, 0:4] # Analog Devices

# Get dates
dates = data.index.tolist()
dates = pd.DataFrame(mdates.date2num(dates), columns = ["Date"], index = data.index)

# Add dates column to OHLC DataFrames
ADI_candle = pd.concat([dates, ADI_candle], axis = 1)

# +
###############################################################################
#                 4b. Visualize Data: Make Candlestick Chart                  #
###############################################################################
# Define time interval to consider
start_date = datetime.date(2020, 1, 1) # Year-Month-Day
end_date   = datetime.date(2021, 6, 30)

# Create figure
fig, ax = plt.subplots(figsize=(13, 6.5))

# Plot ADI_OHLC data
candlestick_ohlc(ax, ADI_candle.values.tolist(), 
                 width=.6, 
                 colorup='green',
                 colordown='red')

# Set x and y axis limits
ax.set_xlim([start_date, end_date])
# ax.set_ylim([60, 69])

# Set axis labels
ax.set_ylabel("Price ($)", fontsize = 20)

# Rotate tick labels
xlabels = ax.get_xticklabels()
# ax.set_xticklabels(xlabels, rotation = 45, fontsize = 14)

# Change x-axis tick label fromat
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y%m%d'))

# Send gridlines to back
ax.set_axisbelow(True)

# Tight layout
plt.tight_layout()

# -

from datetime import datetime as dt
x = []
y = []
for (d,v) in zip(data_apple.Datum, data_apple.Kurs):
    x.append(dt.strptime(d, '%Y/%M/%d'))
    y.append(v)
ax.plot(x,y, marker='o', linestyle='None', color='blue')
fig



# ref: https://medium.com/analytics-vidhya/stock-market-trends-b24203484e0f
