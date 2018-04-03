import glob
import numpy as np
import pandas as pd
from functools import partial
from operator import ne
from collections import defaultdict
import time
import matplotlib.pyplot as plt
import stock as stk
import agent
#import yahoo-market_data as ymd
#aapl = Share('MLNX')
#print(aapl)


#aapl.get_historical()
Database = defaultdict(list)
csv_path_debug = './csv_files'
csv_sp500_path = './csv_files_sp500'
csv_path = csv_sp500_path
list_of_files = glob.glob(csv_path+'/*.csv')

def get_tags_vector(samples, base, length):
    """
         This function gets a vector of samples and returns
         binary vector indicates the directinal movment 1-up,0-down
         output[i] = smaples[i]-samples[i-1]
    """
    ret_list= []
    for i in range(base, base+length):
        if samples[i-1] > samples[i]:
            ret_list.append(1)          # current sample is higher from previous
        else:
            ret_list.append(0)
    return ret_list

def cross_corellation_window(a,v,base_window,window_size):
    retvec = []
    for k in range(0,window_size):
        tmp_a = a[base_window+k:base_window+k+window_size]
        tmp_v = v[base_window:base_window+window_size]
        retvec.append(np.dot(tmp_a,tmp_v))
    return retvec

def parse_signal_from_csv_to_list(signal):
    signal = list(signal)[1:]
    signal = list(filter(partial(ne, 'null'), signal))
    signal = [float(cur) for cur in signal]
    signal.reverse()
    return signal

def parse_dates_from_csv_to_list(Dates_list):
    Dates_list = list(Dates_list)[1:]
    Dates_list = list(filter(partial(ne, 'null'), Dates_list))
    Dates_list.reverse()
    return Dates_list

def get_index_from_date(stock_symbol,date):
    import datetime
    while(not Database[stock_symbol]['Date'].__contains__(date)):
        date_obj = datetime.strptime(date,'%YYYY-%mm-%dd')
        date_obj=date_obj.replace(day=date_obj.day-1)
        date = date_obj.strftime('%YYYY-%mm-%dd')

    index_of_date = Database[stock_symbol]['Date'].index(date)
    print("index_of_date=",index_of_date,"db.Database[stock_symbol]['Close']=",Database[stock_symbol]['Close'][index_of_date])
    return index_of_date



correlated_symbols = []
for file_name in list_of_files:
    with open(file_name, newline='') as csvfile:
        df = pd.read_csv(csvfile, sep=',', header=None,encoding="utf-8-sig")
        if csv_path == csv_sp500_path:
            Date = parse_dates_from_csv_to_list(df[1].values)
            Open = parse_signal_from_csv_to_list(df[2].values)
            High = parse_signal_from_csv_to_list(df[3].values)
            Low = parse_signal_from_csv_to_list(df[4].values)
            Close = parse_signal_from_csv_to_list(df[5].values)
            Vol = parse_signal_from_csv_to_list(df[7].values)
        else:
            Date  = parse_dates_from_csv_to_list(df[0].values)
            Open  = parse_signal_from_csv_to_list(df[1].values)
            High  = parse_signal_from_csv_to_list(df[2].values)
            Low   = parse_signal_from_csv_to_list(df[3].values)
            Close = parse_signal_from_csv_to_list(df[4].values)
            Vol   = parse_signal_from_csv_to_list(df[6].values)

        Database[file_name] = {'Date':   Date,
                               'Open':   Open,
                               'High':   High,
                               'Low':    Low,
                               'Close':  Close,
                               'Volume':  Vol
                               }

