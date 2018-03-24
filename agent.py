import stocksDatabase as DB
import stock as stk
import numpy as np
import copy
import scipy
import SPFG as SP

class Agent:
    #def __init__(self ,stockToPredict=stk.Stock(),correlatedStock = stk.Stock()):
    def __init__(self, stockToPredict, correlatedStock,mode = 'SinLag_SinCC'):
        self.stockToPredict = stockToPredict
        self.correlatedStock = correlatedStock
        self.mode = mode
        self.lag = 0
        
    def vote(self,binary_correlation = True,agentMode='SinLag_SinCC',correlationLength=401,PVMode=False):

        y_tags = self.correlatedStock.get_tags_history('Close',length=correlationLength)
#        ccCloseVal , lagClose  = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
#                                                                             binary_correlation=binary_correlation,
#                                                                             correlationLength=correlationLength)
        ccCloseVal, lagClose = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                           binary_correlation=binary_correlation,
                                                                           correlationLength=correlationLength)


        if agentMode == 'SinLag_MuCC':
            ccVolumeVal, lagVolume = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                               signal='Volume',
                                                                                binary_correlation=False,
                                                                                 correlationLength=correlationLength)
            ccMAVal, lagMA = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                                 signal='MA',
                                                                                 binary_correlation=False,
                                                                                 correlationLength=correlationLength)

            #ccGCRVal, lagGCR = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
            #                                                             signal='GCR',
            #                                                             binary_correlation=False,
            #                                                             correlationLength=correlationLength)
            #ccDCRVal, lagDCR = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
            #                                                               signal='DCR',
            #                                                              binary_correlation=False,
            #                                                              correlationLength=correlationLength)
            #ccRSIVal, lagRSI = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
            #                                                               signal='RSI',
            #                                                               binary_correlation=False,
            #                                                               correlationLength=correlationLength)

            ccOpenVSPrevCloseVal, lagOpenVSPrevClose = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                                                   signal='OpenVSPrevClose',
                                                                                                   binary_correlation=False,
                                                                                                   correlationLength=correlationLength)

            ccPercentageChangeVal, lagPercentageChange = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                           signal='PercentageChange',
                                                                           binary_correlation=False,
                                                                           correlationLength=correlationLength)

            lags = [lagClose,lagVolume,lagMA,lagOpenVSPrevClose,lagPercentageChange]
            CCs  = [ccCloseVal,ccVolumeVal, ccMAVal, ccOpenVSPrevCloseVal,
                                ccPercentageChangeVal]


            #lags = [lagClose, lagVolume, lagMA]
            #CCs = [ccCloseVal, ccVolumeVal, ccMAVal]
            PLbls = ['Close', 'Volume', 'MA','OvsC','%change']
            #PLbls = ['Close','Volume','MA']

            validLagsIndices = [i for i in range(0,lags.__len__()) if lags[i]>0]
            validLags  = [lags[i] for i in validLagsIndices]
            validCCs   = [CCs[i] for i in validLagsIndices]
            validPLbls = [PLbls[i] for i in validLagsIndices]
            #print("validCCs = ", validCCs)
            #print("validPLbls = ", validPLbls)
            if validCCs.__len__()<1:
                return 0,0,0
            maxCC  = max(validCCs)
            maxIdx = validCCs.index(maxCC)
            lag    = validLags[maxIdx]
            cc     = validCCs[maxIdx]
            PLbl   = validPLbls[maxIdx]
            Y_Lag = y_tags[lag - 1]
            self.lag = lag
            if PVMode == True:
                Y_Lag = Y_Lag * cc
            return Y_Lag,cc,PLbl

        if lagClose <= 0:
            Y_LagClose,ccCloseVal = 0,0
            return Y_LagClose,ccCloseVal

        elif agentMode == 'MuLag_SinCC':
            windowS = max(0, lagClose - 2)
            windowE = lagClose + 1
            Y_LagClose = np.argmax(np.bincount(y_tags[windowS:windowE]))
            #print("Inside agent vote")
            #print("agentMode = ", agentMode)
            #print("y_tags[windowS:windowE] = ", y_tags[windowS:windowE])
            #print("Y_LagClose = ", Y_LagClose)
            if Y_LagClose > 1:
                print("stop")
        elif agentMode == 'SinLag_SinCC':
            Y_LagClose = y_tags[lagClose - 1]



        self.lag = lagClose
        if PVMode == True:
            Y_LagClose = Y_LagClose*ccCloseVal
        if Y_LagClose > 1:
            print("stop")
        return Y_LagClose ,ccCloseVal