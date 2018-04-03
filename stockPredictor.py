import tensorflow as tf
import stocksDatabase as DB
import stock as stk
import numpy as np
np.random.seed(1000) # for reproducibility
from keras.layers import Dense
from keras.models import Sequential
import keras as krs
from datetime import datetime
import sysConfig as CFG

class stockPredictor():

    def __init__(self,stockSymbol,date):
        self.stockToPredict = stk.Stock()
        cur_symbol = DB.csv_path + '\\' + stockSymbol + '.csv'
        self.stockToPredict.init_from_symbol(cur_symbol,base=self.get_index_from_date(cur_symbol, date))

    def get_index_from_date(self,stock_symbol, date):
        while (not DB.Database[stock_symbol]['Date'].__contains__(date)):
            date_obj = datetime.strptime(date, '%YYYY-%mm-%dd')
            date_obj = date_obj.replace(day=date_obj.day - 1)
            date = date_obj.strftime('%YYYY-%mm-%dd')

        index_of_date = DB.Database[stock_symbol]['Date'].index(date)
        return index_of_date

    def predict(self):
        print("stockPredictor: initialize stock...")
        Y_tags = self.stockToPredict.get_tags_history('Close',length=CFG.length)  #tags from index = 1

        # train set #
        print("stockPredictor: getting train set...")
        Y_tr = Y_tags[0:CFG.length]
        X_tr, symbol_corr, bestCorrVal, bestAgentLag,*rest = self.stockToPredict.getFeatures(firstSampleIndex = 1,
                                                                                 numberOfsamples=CFG.length,
                                                                                 correlation_length=CFG.correlation_length,
                                                                                 featuresMode = CFG.featuresMode,
                                                                                 binary_correlation = CFG.binary_correlation,
                                                                                 agentMode= CFG.agentMode,
                                                                                 PVMode=CFG.PVMode)
        # test sample #
        print("stockPredictor: getting test set...")
        X_te, correlate_symbol, bestCorrVal,bestAgentLag,PLbl = self.stockToPredict.getFeatures(firstSampleIndex = 0,
                                                                                                numberOfsamples=1,
                                                                                               correlation_length=CFG.correlation_length,
                                                                                               featuresMode = CFG.featuresMode,
                                                                                               binary_correlation=CFG.binary_correlation,
                                                                                               agentMode=CFG.agentMode,
                                                                                               PVMode=CFG.PVMode)

        # create keras model #
        scores = [0.4, 0.4]
        badCount = 0
        while scores[0] >= 0.4 and badCount < 3:
            print("stockPredictor: creates the network...")
            model = Sequential()
            model.add(Dense((X_tr.shape[1]), input_dim=X_tr.shape[1], activation='relu'))
            model.add(Dense(5, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
            model.add(Dense(1, activation='sigmoid', kernel_initializer='random_uniform', bias_initializer='zeros'))

            # Compile model #
            model.compile(loss='binary_crossentropy', optimizer=krs.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True),
                          metrics=['binary_accuracy'])

            # keras fit model #
            print("stockPredictor: fitting the network...")
            model.fit(X_tr, Y_tr, epochs=150, batch_size=10,verbose=0,shuffle=False)

            # evaluate the model #
            scores = model.evaluate(X_tr, Y_tr)
            print("\nstockPredictor: scores for the train = ", scores)
            if scores[0] > 0.4:
                print("stockPredictor: bad scores for fitting.")
                badCount += 1
                if badCount < 3:
                    print("stockPredictor: re-create classifier...")

        #  keras prediction #
        print("predict...")
        predictions = model.predict(X_te)

        # round predictions
        out = [round(x[0]) for x in predictions]
        out=out[0]
        print("<><><><><><> The current Close price is = ",self.stockToPredict.Close[0],"<><><><><><>")
        print("\n======> for date = ",self.stockToPredict.Date[0],": the predictin is = ", out)


print("choose symbol:")
stock_symbol = input()
print("choose date in format YYYY-mm-dd:")
date = input()
stkPred = stockPredictor(stock_symbol,date)
stkPred.predict()