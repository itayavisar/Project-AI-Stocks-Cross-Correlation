import stocksDatabase as DB
import stock as stk
import pandas as pd
import glob
import SPFG as SP
list_of_files = glob.glob(DB.csv_path+'/*.csv')

def build(length,correlation_length=400,base = 10):
    correlations = []
    table = {}
    for curSymbol in list_of_files:
        curStk = stk.Stock()
        curStk.init_from_symbol(curSymbol, base=base)
        table[curStk.name.split('\\')[1]] = {}
        for corSymbol in list_of_files:
            corStk = stk.Stock()
            corStk.init_from_symbol(corSymbol, base=base)
            #correlation,lag = curStk.get_correlation_and_lag(corStk,correlationLength= correlation_length)
            print("Inside build: correlation length = ",correlation_length)
            correlation, lag = SP.get_correlation_and_lag(curStk,corStk, correlationLength=correlation_length)
            table[curStk.name.split('\\')[1]][corStk.name.split('\\')[1]] = ["{0:.2f}".format(correlation),
                                                                             lag]
            #correlations = curStk.get_correlated_symbols(correlation_length,)
            #correlationsValue = [corr[0] for corr in correlations.values()]

    df = pd.DataFrame()
    #for symbol in correlations.keys():
    #    for corr_symbol in correlations[symbol]:

    #        table[corr_symbol.split('\\')[1]] = {'coreelation value': correlations[symbol][corr_symbol][0],
    #                              'correlation lag': correlations[symbol][corr_symbol][1]}

    #(pd.DataFrame.from_dict(data=df, orient='index').to_csv('correlations.csv', header=True))
    df = (pd.DataFrame.from_dict(data=table, orient='index'))
    #df.append(pd.DataFrame.from_dict([{'coreelation value': 123,'correlation lag': 333}]))
    df.to_csv('correlations.csv', header=True)

   # import csv
    # open a file for writing
    #with open('correlations2.csv','w') as employ_data:
    #    csvwriter = csv.writer(employ_data)
    #    count = 0
    #    for emp in correlations[symbol]:
    #        print("========  emp is",emp)
    #        if count == 0:
    #             header = ["value:","lag:"]
    #             csvwriter.writerow(header)
    #            count += 1
    #        csvwriter.writerow(correlations[symbol][emp])


print("build start:")
#'./csv_files_sp500\\AAPL.csv'
build(400,correlation_length=401)

print("build end")