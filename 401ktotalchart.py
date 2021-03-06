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

mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

df = pd.read_csv("/home/john/Projects/PrincipalScraper/401k.csv", usecols=['Date','Total Balance','Cumulative Contribution'], parse_dates=['Date'])
df.set_index('Date',inplace=True)

fig, ax = plt.subplots(figsize=(15,7))
df.plot(ax=ax)

fmt = '${x:,.0f}'
tick = ticker.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick)

start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(50, end, 25))

ax.set_title("401k Total Balance")
ax.grid(which='major',axis='both')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xticks(rotation=90, horizontalalignment="center")
plt.show()
