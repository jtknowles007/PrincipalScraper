#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import matplotlib.dates as mdates
import numpy as np
import matplotlib as mpl
import matplotlib.style
from cycler import cycler
import sys

if len(sys.argv) >1:
    user = sys.argv[1]
else:
    print("You did not suppy a user.")
    exit()

mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
basefile = '/home/john/Projects/PrincipalScraper/'
if user == "john":
    thefile = basefile + '403b.csv'
elif user == 'carla':
    thefile = basefile + '401k.csv'
else:
    print("I don't know that user.")
    exit()

df = pd.read_csv(thefile, usecols=['Date','Total Balance','Cumulative Contribution'], parse_dates=['Date'])
df.set_index('Date',inplace=True)

fig, ax = plt.subplots(figsize=(15,7))
df.plot(ax=ax)

fmt = '${x:,.0f}'
tick = ticker.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick)

start, end = ax.get_ylim()
if user == 'john':
    ax.yaxis.set_ticks(np.arange(6000, end, 1000))
    ax.set_title("403b Total Balance and Contributions Over Time")
elif user == 'carla':
    ax.yaxis.set_ticks(np.arange(0, end, 25))
    ax.set_title("401k Total Balance and Contributions Over Time")
ax.grid(which='major',axis='both')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xticks(rotation=90, horizontalalignment="center")
plt.show()
