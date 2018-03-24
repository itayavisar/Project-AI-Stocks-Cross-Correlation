import tensorflow as tf
import stocksDatabase as DB
import stock as stk
import numpy as np
np.random.seed(1000) # for reproducibility
from keras.layers import Dense
from keras.models import Sequential
import keras as krs
import pandas as pd
import time
import ANN

def main():
    ### init parameters ###
    err = []
    #ANN.base = 52
    length = 400
    correlation_length=400
    #sts paramerter
    prev_out = 0
    total_err = 0
    count_total=0
    count_swap = 0

    #cur_symbol = './csv_files\\AMZN.csv'
    cur_symbol = ANN.cur_symbol

    #cur_symbol = DB.csv_path + '\\^GSPC.csv'
    #cur_symbol = DB.csv_path + '\\BBY.csv'
    build_csv_table = {}
    build_csv_table[cur_symbol] = {}
    cur_stk = stk.Stock()
    test_stock = stk.Stock()

    for i in range(ANN.base,2,-1):
        #init stock
        print("initialize stock...")
        cur_stk.init_from_symbol(cur_symbol,base=i)
        test_stock.init_from_symbol(cur_symbol, base=i-1)
        test_stock_tags = test_stock.get_tags_history('Close',length=length)
        cur_y_tags = cur_stk.get_tags_history('Close',length=length)  #tags from index = 1
        print("symbol is=",cur_stk.name)
        # test
        Y_te = test_stock_tags[0]
        print("on iteration:========================",i)

        ##  prediction
        print("predict...")
        out = cur_y_tags[0]
        # round predictions

        cur_err = int(np.abs(out-Y_te))
        total_err = total_err+cur_err

        #build_csv_table[cur_symbol][cur_stk.Date[i]] = {'Correlated Symbol':correlate_symbol.split("\\")[1],
        #                               'Correlated Value': corr_val,'Lag': lag,'Y_lag': X_te[0][0],
        #                                                'Y_test': Y_te,'Prediction':out,'Err': cur_err}

        print("total_err:",total_err)
        count_total+=1
        precentage_err = total_err / count_total
        print("curr precentage_err===========>",precentage_err,"for i=",i)
        if prev_out != out:
            print("=======================================================")
            print("new out is=:",out,"and prev_out is =: ",prev_out)
            print("=======================================================")
            prev_out = out
            count_swap+=1

        time.sleep(1)


    err.append(total_err)
    print("=========================================")
    print("=========================================")
    print("|||   precentage_err = ", precentage_err, "|||")
    print("|||   count of swaps = ", count_swap    , "|||")
    print("=========================================")
    print("=========================================")
    print("total predictions = ",count_total)

    # build the results table

    #(pd.DataFrame.from_dict(data=build_csv_table[cur_symbol], orient='index').to_csv('results.csv', header=True))
    #(pd.DataFrame.from_dict(data=build_csv_table, orient='index').to_csv('results.csv', header=True))

if __name__ == '__main__':
    from sys import argv
    #assert len(argv) == 3
    main()
