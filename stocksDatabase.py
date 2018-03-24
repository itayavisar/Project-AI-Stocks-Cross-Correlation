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


#Database['./csv_files\\AAPL.csv']['Close']=Database['./csv_files\\MLNX.csv']['Close'][10:]
#Database['./csv_files\\AAPL.csv']['Open']=Database['./csv_files\\MLNX.csv']['Open'][10:]
#Database['./csv_files\\AAPL.csv']['Date']=Database['./csv_files\\MLNX.csv']['Date'][10:]
#Database['./csv_files\\AAPL.csv']['Volume']=Database['./csv_files\\MLNX.csv']['Volume'][10:]
#Database['./csv_files\\AAPL.csv']['High']=Database['./csv_files\\MLNX.csv']['High'][10:]
#Database['./csv_files\\AAPL.csv']['Low']=Database['./csv_files\\MLNX.csv']['Low'][10:]
#print("first date =",Database['./csv_files\\AAPL.csv']['Date'][0])
#a=normalize(Database['./csv_files\\MLNX.csv']['Close'])[20:20+400]
#b=normalize(Database['./csv_files\\AAPL.csv']['Close'])[20:20+400]
#cc1=(np.correlate(b,a, mode='same'))/((np.linalg.norm(a) * np.linalg.norm(b)))
#print("len = ",cc1.__len__(),"estimated lag =",(cc1.__len__()/2)-np.argmax(cc1))
#plt.plot(cc1, label="CC1",color='red')
#plt.plot(a, label="a",color='pink')
#plt.plot(b, label="b",color='green')
#plt.show()

#print("mlnx is:",Database['./csv_files\\MLNX.csv']['Close'][0])
#print("appl is:",Database['./csv_files\\AAPL.csv']['Close'][10])


#def get_correlated_stocks(cur_stock,length,binary_correlation = True):

'''
def get_correlated_symbols(cur_symbol,base,length,binary_correlation = True):
    print("getting correlations for stock: ",cur_symbol)
    correlated_symbols = {}
    correlated_symbols[cur_symbol] = {}
    a1 = normalize(Database[cur_symbol]['Close'][base:base + length])
    bin_a1 = get_tags_vector(Database[cur_symbol]['Close'], base, length)
    #a1=a1[0:300] # TODO debug
    for correlated_stock_symbol in list_of_files:
        if correlated_stock_symbol != cur_symbol:
            #print("after if: correlated_stock_symbol =", correlated_stock_symbol, "cur_symbol=", cur_symbol)
            # The first signal is the shifted one
            bin_v1 = get_tags_vector(Database[correlated_stock_symbol]['Close'], base, length)
            v1 = normalize(Database[correlated_stock_symbol]['Close'][base:base+length])
            if binary_correlation:
                cc1 = np.correlate(bin_a1, bin_v1, mode='same')
                cc1 = np.asarray(cc1)/(np.linalg.norm(bin_a1) * np.linalg.norm(bin_v1))
            else:
                cc1 = np.correlate(a1, v1, mode='same')
                cc1 = np.asarray(cc1)/(np.linalg.norm(a1) * np.linalg.norm(v1))

            lag = (round(cc1.__len__() / 2) - np.argmax(cc1))
            cc1_val = max(cc1)
            #plt.plot(cc1_val, label="CC2",color='green')
            #plt.show()
            i=0;
            #while lag <= 0 and max(cc1)>0:
            #    cc1[np.argmax(cc1)] = 0
            #    lag = (round(cc1.__len__() / 2) - np.argmax(cc1))
            #    cc1_val = max(cc1)
               #plt.plot(cc1_val, label="CC2", color='green')
               #plt.show()
            #    i=i+1
            #    if lag > 0:
            #        print("lag for correlated_stock",correlated_stock_symbol,"is finally > 0 and lag is ",
            #              lag, "and i is ",i)
            #if lag<=0:
            #    print("on stock ",correlated_stock_symbol,"lag is ",lag,"on i ",i,
            #          "and cc1_val is ",cc1_val)
            correlated_symbols[cur_symbol][correlated_stock_symbol] = [cc1_val, lag]
    return correlated_symbols
'''

#s = './csv_files\\MLNX.csv'
#correlated_symbols = get_correlated_symbols(s,17,400)
#cc = correlated_symbols[s][max(correlated_symbols[s], key=lambda k: correlated_symbols[s][k])][1]
#print("cc lag is :",cc,"correlated_symbols:",correlated_symbols)
#a=[1,5,8,5,  2  ,9,9,10,8]
#v=[8,5,2,9,  9  ,10,8]

#a2 = Database[ './csv_files\\AAPL.csv']['Close'][17:17+600]
#a2 = (a2-np.mean(a2))/np.std(a2)
#v2 = Database['./csv_files\\MLNX.csv']['Close'][17:17+600]
#v2 = (v2-np.mean(v2))/np.std(v2)
#cc2 = np.correlate(a2,v2, mode='same')
#cc2 /= (np.linalg.norm(a2) * np.linalg.norm(v2))
#lag = (int(cc2.__len__() / 2) - np.argmax(cc2))
#print(np.argmax(cc2))
#plt.plot(cc2, label="CC2",color='green')
#plt.plot(a2, label="a2",color='blue')
#plt.plot(v2, label="v2",color='yellow')
#plt.show()
#plt.plot(cc1, label="CC1",color='green')

############################
## way to normelize the data
##############################
#a=(a-np.mean(a))/np.std(a)
#v=(v-np.mean(v))/np.std(v)
#goog=(goog-np.mean(goog))/np.std(goog)
#avgo=(avgo-np.mean(avgo))/np.std(avgo)

###################################
## way to correlate
#######################################
#cc1 = np.correlate(a, v, mode='same')
#cc1=cc1/(np.linalg.norm(a)*np.linalg.norm(v))
#cc2 = np.correlate(a, goog, mode='same')
#cc2=cc2/(np.linalg.norm(a)*np.linalg.norm(goog))
#cc3 = np.correlate(a, avgo, mode='same')
#cc3=cc3/(np.linalg.norm(a)*np.linalg.norm(avgo))

#############################################
## way to plot
#############################################
#import matplotlib.pyplot as plt
#plt.plot(cc1, label="CC1",color='red')
#plt.plot(cc2, label="CC2",color='blue')
#plt.plot(cc3, label="CC3",color='green')
#plt.show()

#############################################
## trying to correlate by window
#############################################

'''
a=[1,5,8,5,  2  ,9,9,10,8,20,24,19,18]
v=[8,5,2,9,  9  ,10,8,20,24,19,18]
#a=(a-np.mean(a))/np.std(a)
#v=(v-np.mean(v))/np.std(v)
plt.plot(a, label="a2",color='blue')
plt.plot(v, label="v2",color='yellow')
#cc1 = np.correlate(a,v, 17)
cc1 = cross_corellation_window(a,v,4,4)
#cc1 = cc1/(np.linalg.norm(a)*np.linalg.norm(v))
print(np.argmax(cc1))
print(cc1)
plt.plot((cc1), label="cc1",color='yellow')
plt.show()
'''