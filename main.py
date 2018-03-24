import tensorflow as tf
import stocksDatabase as DB
import stock as stk
import numpy as np
import predictor_sts as sts
np.random.seed(1000) # for reproducibility
from keras.layers import Dense
#from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
import keras as krs
import pandas as pd
import time

#cur_symbol = DB.csv_path+'\\QCOM.csv'
#cur_symbol = DB.csv_path+'\\AAPL_10lag.csv'
#cur_symbol = DB.csv_path+'\\AAPL.csv'
cur_symbol = DB.csv_path+'\\AA.csv' #--- for the experiment
#cur_symbol = DB.csv_path+'\\AEE.csv'
#cur_symbol = DB.csv_path+'\\AEP.csv'
#cur_symbol = DB.csv_path+'\\AIG.csv'       #showing lairs
#cur_symbol = DB.csv_path+'\\AVGO.csv'
#cur_symbol = DB.csv_path + '\\^GSPC.csv'
#cur_symbol = DB.csv_path + '\\BBY.csv'
#cur_symbol = DB.csv_path + '\\AAL.csv'
#cur_symbol = DB.csv_path + '\\MLNX.csv'
base = 42

def main():
    #featuresMode = 'BEST_AGENT'
    featuresMode = 0
    binary_correlation = True
    PVMode = False
    #agentMode = 'SinLag_SinCC'
    agentMode = 'MuLag_SinCC'
    #agentMode = 'SinLag_MuCC'
    #agentMode = 0
    errVec = []
    trivialErrVec =[]
    length = 401
    correlation_length = 401
    choise=5
    while(choise == '9'):
        print("choose:\n1:  experiment#1\n2:  experiment#2\n3:  experiment#3\n","4:  predictor\n9:  exit\n")
        choise = input()
        if choise == '1':
            choise=5
        elif choise == '4':
            choise = 5
        elif choise == '9':
            return
        else:
            break

    ### init parameters ###
    # sts paramerter
    psts = sts.Psts()

    build_csv_table = {}
    build_csv_table[cur_symbol] = {}
    timelineDate = []
    pointLbl=[]
    timeline = []
    cntIter = 0
    corrValVec=[]

    cur_stk = stk.Stock()
    for i in range(base,2,-1):
        #init stock
        print("initialize stock...")
        cur_stk.init_from_symbol(cur_symbol,base=i)
        test_stock = stk.Stock()
        test_stock.init_from_symbol(cur_symbol, base=i-1)
        test_stock_tags = test_stock.get_tags_history('Close',length=length)
        cur_y_tags = cur_stk.get_tags_history('Close',length=length)  #tags from index = 1

        # train set
        print("getting train set...")
        Y_tr = cur_y_tags[0:length]
        X_tr, symbol_corr, bestCorrVal, bestAgentLag,*rest = cur_stk.getFeatures(length,
                                                                                 correlation_length=correlation_length,
                                                                                 featuresMode = featuresMode,
                                                                                 binary_correlation = binary_correlation,
                                                                                 agentMode= agentMode,
                                                                                 PVMode=PVMode)
        print("X_tr[0] is ",X_tr[0])

        # test set
        print("getting test set...")
        if agentMode == 'SinLag_MuCC':
            X_te, correlate_symbol, bestCorrVal,bestAgentLag,PLbl = test_stock.getFeatures(1,
                                                                                           correlation_length=correlation_length,
                                                                                           featuresMode = featuresMode,
                                                                                           binary_correlation=binary_correlation,
                                                                                           agentMode=agentMode,
                                                                                           PVMode=PVMode)
        else:
            X_te, correlate_symbol, bestCorrVal, bestAgentLag,*rest = test_stock.getFeatures(1,
                                                                                             correlation_length=correlation_length,
                                                                                             featuresMode=featuresMode,
                                                                                             binary_correlation=binary_correlation,
                                                                                             agentMode=agentMode,
                                                                                             PVMode=PVMode)
        Y_te = test_stock_tags[0]
        trivial_pred = test_stock_tags[1]

        corrValVec.append(bestCorrVal)
        timelineDate.append(cur_stk.Date[0])
        timeline.append(cntIter)
        cntIter+=1
        if agentMode == 'SinLag_MuCC':
            pointLbl.append(PLbl)
            print("appending Point labe = ",pointLbl)
        print("for cur_stk.symbol = ", cur_stk.name)
        print("for test_stk.symbol = ", test_stock.name)
        print("for test_stk.Date[i] = ", cur_stk.Date[0], " and i is ",i)
        print("corr_symbol , bestCorrVal , lag  = ",correlate_symbol,bestCorrVal, bestAgentLag)
        print("on iteration:========================",i)

        ### create keras model
        scores = [0.4, 0.4]
        badCount = 0
        while scores[0] >= 0.4 and badCount < 3:
            print("creates the network...")
            model = Sequential()
            model.add(Dense((X_tr.shape[1]), input_dim=X_tr.shape[1], activation='relu'))
            model.add(Dense(5, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
            #model.add(Dense(5, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
            model.add(Dense(1, activation='sigmoid', kernel_initializer='random_uniform', bias_initializer='zeros'))

            # Compile model
            # model.compile(loss='binary_crossentropy', optimizer=krs.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True), metrics=['accuracy'])

            model.compile(loss='binary_crossentropy', optimizer=krs.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True),
                          metrics=['binary_accuracy'])

            #keras fit model
            print("fitting the network...")
            print("previous Error Rate===========>", psts.errorRate, "for i=", i)
            print("num of iterations Past = ", psts.iterationsPast, "total Error=", psts.totalErr,
                  " number new predictions= ",psts.numOfNewPredictions)
            model.fit(X_tr, Y_tr, epochs=150, batch_size=10,verbose=0,shuffle=False)

            # evaluate the model
            scores = model.evaluate(X_tr, Y_tr)
            print("\nscores for the train = ", scores)
            if scores[0] > 0.4:
                print("bad scores for fitting.")
                badCount += 1
                if badCount < 3:
                    print("re-create classifier...")



        ##  keras prediction
        print("predict...")
        predictions = model.predict(X_te)

        # round predictions
        out = [round(x[0]) for x in predictions]
        out=out[0]
        print("<><><><><><> cur_stk.Close[0] = ",cur_stk.Close[0],"<><><><><><>")
        print("\n==> for date = ",cur_stk.Date[0],": out = ", out, " Y_te=", Y_te, " X_te[0]=", X_te[0]," predictions is ", predictions)
        if out != Y_te:
            cur_err = 1
        else:
            cur_err = 0
        if trivial_pred != Y_te:
            trivialErr = 1
        else:
            trivialErr = 0
        errVec.append(cur_err)
        trivialErrVec.append(trivialErr)

        psts.totalErr += cur_err
        psts.trivialTotalErr += trivialErr

        build_csv_table[cur_symbol][cur_stk.Date[i]] = {'Correlated Symbol':correlate_symbol.split("\\")[1],
                                       'Correlated Value': bestCorrVal,'Lag': bestAgentLag,'Y_lag': X_te[0][0],
                                                        'Y_test': Y_te,'Prediction':out,'Err': cur_err}

        print("total Error:",psts.totalErr)
        psts.iterationsPast+=1
        psts.errorRate = psts.totalErr / psts.iterationsPast
        psts.trivialErrRate = psts.trivialTotalErr / psts.iterationsPast
        print("curr Error Rate==================>",psts.errorRate,"for i=",i)
        print("curr Err ============================>",cur_err, "for i=", i)
        print("count total= ", psts.iterationsPast, "total Error=", psts.totalErr)
        if psts.curOutput!= out:
            print("=======================================================")
            print("new output is=:",out,"and previous output is =: ",psts.curOutput)
            print("=======================================================")
            psts.curOutput = out
            psts.numOfNewPredictions+=1

    print("=========================================")
    print("===============SUMMERY===================")
    print("=========================================")
    print("|||   Error rate = ", psts.errorRate, "|||")
    print("|||   trivial Error rate = ", psts.trivialErrRate, "|||")
    print("|||   number of New Predictions = ", psts.numOfNewPredictions    , "|||")
    print("=========================================")
    print("=========================================")
    print("total predictions = ",psts.iterationsPast)


    # build the results table
    print("create output file...")
    (pd.DataFrame.from_dict(data=build_csv_table[cur_symbol], orient='index').to_csv('results.csv', header=True))
    print("output file in results.csv")

    #plot graphs
    import matplotlib.pyplot as plt
    print("corrValVec = ",corrValVec," errVec = ",errVec)
    fig = plt.figure(1)
    ax1 = fig.add_subplot(311)
    color = ['red' if l == 1 else 'green' for l in errVec]
    ax1.scatter(range(0,timeline.__len__()),corrValVec, c=color,)
    for i, txt in enumerate(pointLbl):
        ax1.annotate(txt, (timeline[i], corrValVec[i]))

    ax1.set_xticks(range(len(timelineDate)))
    ax1.set_xticklabels(timelineDate)
    ax1.text(3, 8, 'Error Rate = '+psts.errorRate.__str__(), style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    fig.autofmt_xdate(rotation=90)
    ax1.set_xlabel("time")
    ax1.set_ylabel("CC")
    ax1.title.set_text("Classification over CC for stock : "+cur_stk.name.split('\\')[1])
    plt.gcf().text(0.02, 0.95, 'Error Rate = ' + psts.errorRate.__str__(), fontsize=9,fontweight='bold')
    plt.legend()

    #fig2 = plt.figure(2)
    ax2 = fig.add_subplot(313)
    color2 = ['red' if v == 1 else 'green' for v in trivialErrVec]
    ax2.scatter(range(0,timeline.__len__()), corrValVec, c=color2, )
    ax2.set_xticks(range(len(timelineDate)))
    ax2.set_xticklabels(timelineDate)
    ax2.title.set_text("Trivial Classification over CC for stock : " + cur_stk.name.split('\\')[1])
    ax2.set_xlabel("time")
    ax2.set_ylabel("CC")
    plt.gcf().text(0.02, 0.5, 'trivial Error Rate = ' + psts.trivialErrRate.__str__(), fontsize=9,fontweight='bold')

    fig.autofmt_xdate(rotation=90)
    plt.show()


if __name__ == '__main__':
    from sys import argv
    #assert len(argv) == 3
    main()
