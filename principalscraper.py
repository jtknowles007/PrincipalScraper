#!/usr/bin/env python3
#
###############################################################################
#
# Author: John T. Knowles, RN, RHIA
# Date: October 26, 2018
# Version: 0.1
#
###############################################################################
#
'''
Principal Scraper: Scrape current balance data from Principal Retirement site
'''
###############################################################################
# IMPORT
###############################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from credentials import *
from collections import deque
from paydatelist import *
import time
import datetime
import csv
import decimal
###############################################################################
# Login to website
###############################################################################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=/home/john/.config/google-chrome")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://secure05.principal.com/member/accounts")
time.sleep(2)

username = driver.find_element_by_id("userid")
password = driver.find_element_by_id("pass")

username.clear()
username.send_keys(user)
password.clear()
password.send_keys(pswd)

driver.find_element_by_id("loginBtn").click()

time.sleep(2)

element = driver.find_element_by_id("total-balance")
elementext = element.text
elementext = elementext.replace('$','')
elementext = elementext.replace(',','')
print(elementext)

today = datetime.datetime.today().strftime('%m-%d-%Y')
none = ""
def contrib_today(mypay):
    thedate = datetime.datetime.today().strftime('%m-%d-%Y')
    for i in range(0,len(mypay)):
        if thedate == mypay[i]:
            total = "304.16"
            break
        else:
            total = "0.00"
    return total
contribtotal = contrib_today(paydate)
if contribtotal == "0.00":
    contrib1 = "0.00"
    contrib2 = "0.00"
else:
    contrib1 = "140.38"
    contrib2 = "163.78"

def get_last_row(csv_filename):
    with open(csv_filename,'r') as f:
        return deque(csv.reader(f), 1)[0]

lastline = ",".join(get_last_row("/home/john/Projects/PrincipalScraper/403b.csv"))
values = lastline.split(",")
cumcontrib = float(values[6]) + float(contribtotal)
cumcontrib = str(round(cumcontrib,2))
gainloss = float(elementext) - float(cumcontrib)
gainloss = str(round(gainloss,2))

fields = [today,contrib1,contrib2,contribtotal,elementext,none,cumcontrib,gainloss]
with open(r'/home/john/Projects/PrincipalScraper/403b.csv','a') as file:
    write2file = csv.writer(file)
    write2file.writerow(fields)
    file.close()
print("csv updated")


