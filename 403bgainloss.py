#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import matplotlib.dates as mdates

df = pd.read_csv("403b.csv")

#ax = df.plot(kind='line', grid=True, x="Date", y=["TotalBalance","CumulativeContribution"])
#ax.set_xlabel("Date", fontsize=12)
#ax.set_xticklabels(df['Date'], rotation=90)
#ax.set_ylabel("Balance", fontsize=12)
lines = plt.plot(df['Date'], df['GainOrLoss'])
plt.title("403(b) Balance Over Time")
ax = plt.axes()
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=60)
plt.grid(True, which="major", axis="both")
plt.xlabel("Date")
plt.ylabel("Gain/Loss")
plt.show()

