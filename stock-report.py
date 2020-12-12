#!/usr/bin/python3

import yahoo_fin.stock_info as si
import pandas as pd
import datetime


with open("/home/paul/investment/my-investments") as file:
  for line in file:
    if not line.startswith("#"):
      # convert each line to a sublist
      line     = line.strip().split(' ')

      # get symbol, qty and cost from each line
      symbol   = line[0]
      qty      = float(line[1])
      cost     = float(line[2])
      asset    = line[3]
      broker   = line[4]
      owner    = line[5]
      category = line[6]

      # use yahoo_fin to get the stock info
      #price   = round(si.get_live_price(symbol),2)
      si_result=si.get_quote_table(symbol)
      price    =round(si_result["Quote Price"],2)
      pre_close=round(si_result["Previous Close"],2)

      # do some calculation
      daily_chg      =round((price-pre_close),2)
      daily_chg_rate =round((daily_chg/pre_close*100),2)
      mktvalue       = round((qty*price),2)
      gain           = round((mktvalue-cost),2)
      gain_rate      = round((gain/cost*100),2)
      
      # get year, month, and day
      year   = datetime.datetime.today().year
      month  = datetime.datetime.today().month
      day    = datetime.datetime.today().day

      # generate the report
      if "stock" in asset:
        one_yr_r = si_result["52 Week Range"]
        morningstart_r="N/A"
      elif "fund" in asset:
        ytd_return = si_result["YTD Return"]
        one_yr_r = ytd_return[:-1]
        morningstart_r =  si_result["Morningstar Rating"]
      print(year,":",month,":",day,":",symbol,":",qty,":",price,":",cost,":",mktvalue,":",daily_chg,":",daily_chg_rate,":",gain,":",gain_rate,":",one_yr_r,":",asset,":",broker,":",owner,":",category)
        
