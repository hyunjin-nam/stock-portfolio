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
from datetime import datetime as dt

# To make candlestick charts
from mplfinance.original_flavor import candlestick_ohlc
# import mplfinance as mpl
# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# For reading files
from os import listdir

# +
# Import data
avanza_data = pd.read_csv('sample_data.csv', encoding='utf-8')

# Translate to english
avanza_data.rename(columns={'Datum': 'Date', 
                            'Konto': 'Account',
                            'Typ av transaktion': 'Type',
                            'Värdepapper/beskrivning': 'Company',
                            'Antal': 'Amount',
                            'Kurs': 'Price',
                            'Belopp': 'TotalValueChange',
                            'Valuta': 'Currency'}, 
                   inplace=True)

avanza_data.replace({'Type' :
    {'Sälj': 'Sell',
     'Köp' : 'Buy',
     'Utdelning': 'Dividend',
     'Övrigt' : 'Other'}}, 
    inplace=True)

# Change date format and add column with numeric date values
avanza_data['Date'] = pd.to_datetime(avanza_data['Date'], format='%Y/%M/%d').dt.strftime('%Y-%M-%d')
avanza_data.insert(1, 'DateNum', mdates.date2num(avanza_data['Date']))

# Convert data types from string to numeric
avanza_data.replace('-', 'NaN', inplace=True)
avanza_data[['Price', 'TotalValueChange', 'Courtage']] = avanza_data[['Price', 'TotalValueChange', 'Courtage']].apply(pd.to_numeric, errors='coerce')
print(avanza_data)
# -

transaction_data = avanza_data.loc[avanza_data['Company'] == 'Boeing Co']
print(transaction_data)

# ### read stock data

# +
# Set label
stocks = ["BA"] # If you want to grab multiple stocks add more labels to this list

# Set start and end dates
start = datetime.datetime(2020, 1, 1)
end   = datetime.datetime(2021, 6, 30)

# Grab data
yahoo_data = pdr.get_data_yahoo(stocks, start = start, end = end)

# Remove space from column names
yahoo_data.rename(columns={'Adj Close': 'AdjClose'}, inplace=True)

# Change to numeric index and add date columns
yahoo_data = yahoo_data.reset_index()
yahoo_data.insert(1, 'DateNum', mdates.date2num(yahoo_data['Date']))
print(yahoo_data)
# -

# Merge transaction and Yahoo data frames
combined_data = yahoo_data.merge(transaction_data, on='DateNum', how='left')
combined_data.drop(columns='Date_y', inplace=True)
combined_data.rename(columns={'Date_x': 'Date'}, inplace=True)
print(combined_data)

# ## Visualization

# +
###############################################################################
#              4a. Visualize Data: Prepare data for Candlestick Chart         #
###############################################################################
# Get Open, High, Low, Close
ADI_candle = combined_data.iloc[:, [1, 2, 3, 4, 5]] # Analog Devices

# Get dates
# dates = combined_data['DateNum']

# Add dates column to OHLC DataFrames
# ADI_candle = pd.concat([dates, ADI_candle], axis = 1)
# -

# Prepare our data
x_buy = []
y_buy = []
x_sell = []
y_sell = []
for (d,v,t) in zip(combined_data['DateNum'], combined_data['Price'], combined_data['Type']):
    if t == 'Buy':
#         x_buy.append(mdates.date2num(dt.strptime(d, '%Y/%m/%d')))
        x_buy.append(d)
        y_buy.append(float(v))
    if t == 'Sell':
#         x_sell.append(mdates.date2num(dt.strptime(d, '%Y/%m/%d')))
        x_sell.append(d)
        y_sell.append(float(v))

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

# Plot our data
ax.plot(x_buy, y_buy, 'bo')
ax.plot(x_sell, y_sell, 'yo')

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



# ref: https://medium.com/analytics-vidhya/stock-market-trends-b24203484e0f
