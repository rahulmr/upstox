# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 10:29:35 2018

@author: Gireesh Sundaram
"""

#Importing packages
from upstox_api.api import *
from datetime import datetime, time
import time as sleep
import os
import pandas as pd

#%%
api_key = "uvWJebUEBC5MuZz0SWoyx9Il4HX9taXn59rpERsR"
api_secret = "d2kv2xvksl"
redirect_uri = "http://127.0.0.1"
s = Session(api_key)
s.set_redirect_uri(redirect_uri)
s.set_api_secret(api_secret)
print(s.get_login_url())
code = input("Enter the code from the browser: ")

s.set_code (code)
access_token = s.retrieve_access_token()

u = Upstox (api_key, access_token)

print("Login successful. Verify profile:")
print(u.get_profile())

#%%
master = u.get_master_contract('NSE_EQ')  # get contracts for NSE EQ

#Function to fetch the current available balance:
def CheckBalance():
    balance = pd.DataFrame(u.get_balance())
    balance1 = balance["equity"]["available_margin"]
    return balance1

#function to fetch historic data
def historicData(script, start_dt, end_dt):
    data = pd.DataFrame(u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', script),
                      OHLCInterval.Minute_1,
                      datetime.strptime(start_dt, '%d/%m/%Y').date(),
                      datetime.strptime(end_dt, '%d/%m/%Y').date()))
    data = data.tail(100)
    data["sma5"] = data.cp.rolling(window=5).mean()
    data["sma50"] = data.cp.rolling(window=50).mean()
    return data

def buy(script, amount, stoploss, squareoff):
    return u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', script),  # instrument
                 1,  # quantity
                 OrderType.Limit,  # order_type
                 ProductType.OneCancelsOther,  # product_type
                 amount,  # price
                 None,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 stoploss,  # stop_loss
                 squareoff,  # square_off
                 20)  # trailing_ticks 20 * 0.05

def sell(script, amount, stoploss, squareoff):
    return u.place_order(TransactionType.Sell,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', script),  # instrument
                 1,  # quantity
                 OrderType.Limit,  # order_type
                 ProductType.OneCancelsOther,  # product_type
                 amount,  # price
                 None,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 stoploss,  # stop_loss
                 squareoff,  # square_off
                 20)  # trailing_ticks 20 * 0.05

def SMACrossOver(ScriptData, script):
    if ScriptData.sma5.iloc[-6] < ScriptData.sma50.iloc[-6] and ScriptData.sma5.iloc[-5] < ScriptData.sma50.iloc[-5] and ScriptData.sma5.iloc[-4] < ScriptData.sma50.il$
        squareoff = float(round(abs(ScriptData.cp.iloc[-1] - (ScriptData.cp.iloc[-1] * 1.01)), 0))
        stoploss = float(round(abs(ScriptData.cp.iloc[-1] - (ScriptData.cp.iloc[-1] * 1.01)), 0))
        print("Buying at: %s -- stop loss at: %s --  square off at: %s" %(ScriptData.cp.iloc[-1], stoploss, squareoff))
        buy(script, ScriptData.cp.iloc[-1], stoploss, squareoff)

    if ScriptData.sma5.iloc[-6] > ScriptData.sma50.iloc[-6] and ScriptData.sma5.iloc[-5] > ScriptData.sma50.iloc[-5] and ScriptData.sma5.iloc[-4] > ScriptData.sma50.il$
        squareoff = float(round(abs(ScriptData.cp.iloc[-1] - (ScriptData.cp.iloc[-1] * 1.01)), 0))
        stoploss = float(round(abs(ScriptData.cp.iloc[-1] - (ScriptData.cp.iloc[-1] * 1.01)), 0))
        print("Selling at: %s -- stop loss at: %s --  square off at: %s" %(ScriptData.cp.iloc[-1], stoploss, squareoff))
        sell(script, ScriptData.cp.iloc[-1], stoploss, squareoff)


#%%
def CheckTrades():
    now = datetime.now()
    now_time = now.time()

    if time(3,51) <= now_time <= time(8,45) and CheckBalance() > 1500:
        bucket = ["BANKINDIA", "ADANIENT", "CANBK", "JINDALSTEL", "VAKRANGEE", "FORTIS", "JISLJALEQS", "GRAPHITE", "PCJEWELLER", "BOMDYEING", "RELCAPITAL", "IBREALEST"$

        for script in bucket:
            print("~~~~~~~~~~~~~~~~~~~~~~~ \n Now the time is: %s" % datetime.now().time())
            print("Checking for 50 min 5min MA Crossover for %s" % script)
            SMACrossOver(historicData(script, "20/03/2018", "21/03/2018"), script)

    elif time(9,28) <= now_time <= time(9,30):
        print("Exiting all the open position now and exiting execution")
        u.cancel_all_orders() #Cancel all open orders
        exit()

    else:
        print("There is no market activity now. Checking in 10 mins.. Now the time is: %s" % datetime.now().time())
        sleep.sleep(120)

#%%
while True:
    CheckTrades()
    print("\n***Now waiting for 30 seconds")
    sleep.sleep(30)
