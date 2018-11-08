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
from paydatelist import *
from collections import deque
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import csv
import decimal
import sys
import gspread
###############################################################################
# Functions
###############################################################################

def contrib_today(mypay):
    thedate = datetime.datetime.today().strftime('%m-%d-%Y')
    for i in range(0,len(mypay)):
        if thedate == mypay[i]:
            total = "304.16"
            break
        else:
            total = "0.00"
    return total

def get_last_row(csv_filename):
    with open(csv_filename,'r') as f:
        return deque(csv.reader(f), 1)[0]


###############################################################################
# Login to website
###############################################################################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=/home/john/.config/google-chrome/Profile 1")
chrome_options.add_argument("--kiosk")

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

###############################################################################
# Scrape total balance
###############################################################################

#if driver.find_element_by_class_name("bharosaPageTitle"):
#    print ("Ran into security verification notice. Unable to complete request.  Now exiting.")
#    sys.exit()


element = driver.find_element_by_id("total-balance")
elementext = element.text
elementext = elementext.replace('$','')
elementext = elementext.replace(',','')

###############################################################################
# Calculate Data to write
###############################################################################

today = datetime.datetime.today().strftime('%m-%d-%Y')
none = ""

contribtotal = contrib_today(paydate)
if contribtotal == "0.00":
    contrib1 = "0.00"
    contrib2 = "0.00"
else:
    contrib1 = "140.38"
    contrib2 = "163.78"

lastline = ",".join(get_last_row("/home/john/Projects/PrincipalScraper/403b.csv"))
values = lastline.split(",")
cumcontrib = float(values[6]) + float(contribtotal)
cumcontrib = str(round(cumcontrib,2))
gainloss = float(elementext) - float(cumcontrib)
gainloss = str(round(gainloss,2))

fields = [today,contrib1,contrib2,contribtotal,elemt,cumcontrib,gainloss]

###############################################################################
# Write to CSV
###############################################################################

with open(r'/home/john/Projects/PrincipalScraper/403b.csv','a') as file:
    write2file = csv.writer(file)
    write2file.writerow(fields)
    file.close()

###############################################################################
# Write to Google Sheets
###############################################################################

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google.json',scope)
client = gspread.authorize(creds)

sheet = client.open('403(b)trends').sheet1
sheet.append_row(fields)

###############################################################################
# Wrap it up
###############################################################################

print(today + " - Total balance: $" + elementext + ". File 403b.csv and Google Sheet  updated.")
driver.quit()
