import stocksDatabase as DB
import stock as stk
import numpy as np
import copy
import scipy
import SPFG as SP

class Agent:
    def __init__(self, stockToPredict, correlatedStock,mode):
        self.stockToPredict = stockToPredict
        self.correlatedStock = correlatedStock
        self.mode = mode
        self.lag = 0

    def voteMuLagSinCC(self,binary_correlation,correlationLength):
        ccCloseVal, lagClose = SP.get_correlation_and_lag(self.stockToPredict, self.correlatedStock,
                                                          binary_correlation=binary_correlation,
                                                          correlationLength=correlationLength)
        if lagClose <=0:
            Y_LagClose, ccCloseVal, lagClose = 0,0,0
        else:
            y_tags = self.correlatedStock.get_tags_history('Close', length=correlationLength)
            windowS = max(0, lagClose - 1)
            windowE = lagClose+2
            Y_LagClose = np.argmax(np.bincount(y_tags[windowS:windowE]))
        return Y_LagClose, ccCloseVal, lagClose

    def voteSinLagSinCC(self,binary_correlation,correlationLength):
        ccCloseVal, lagClose = SP.get_correlation_and_lag(self.stockToPredict,self.correlatedStock,
                                                                           binary_correlation=binary_correlation,
                                                                           correlationLength=correlationLength)
        if lagClose <=0:
            Y_LagClose, ccCloseVal, lagClose = 0,0,0
        else:
            Y_LagClose = self.correlatedStock.get_tags_history('Close', length=correlationLength)[lagClose - 1]
        return Y_LagClose,ccCloseVal,lagClose

    def voteSinLagMuCC(self,binary_correlation,correlationLength):
        y_tags = self.correlatedStock.get_tags_history('Close', length=correlationLength)
        ccCloseVal, lagClose = SP.get_correlation_and_lag(self.stockToPredict, self.correlatedStock,
                                                          binary_correlation=binary_correlation,
                                                          correlationLength=correlationLength)
        ccVolumeVal, lagVolume = SP.get_correlation_and_lag(self.stockToPredict, self.correlatedStock,
                                                            signal='Volume',
                                                            binary_correlation=False,
                                                            correlationLength=correlationLength)
        ccMAVal, lagMA = SP.get_correlation_and_lag(self.stockToPredict, self.correlatedStock,
                                                    signal='MA',
                                                    binary_correlation=False,
                                                    correlationLength=correlationLength)
        ccOpenVSPrevCloseVal, lagOpenVSPrevClose = SP.get_correlation_and_lag(self.stockToPredict, self.correlatedStock,
                                                                              signal='OpenVSPrevClose',
                                                                              binary_correlation=False,
                                                                              correlationLength=correlationLength)

        ccPercentageChangeVal, lagPercentageChange = SP.get_correlation_and_lag(self.stockToPredict,
                                                                                self.correlatedStock,
                                                                                signal='PercentageChange',
                                                                                binary_correlation=False,
                                                                                correlationLength=correlationLength)
        ## financial signals may be used in the furure ##
        # ccGCRVal, lagGCR = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
        #                                                             signal='GCR',
        #                                                             binary_correlation=False,
        #                                                             correlationLength=correlationLength)
        # ccDCRVal, lagDCR = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
        #                                                               signal='DCR',
        #                                                              binary_correlation=False,
        #                                                              correlationLength=correlationLength)
        # ccRSIVal, lagRSI = self.stockToPredict.get_correlation_and_lag(self.correlatedStock,
        #                                                               signal='RSI',
        #                                                               binary_correlation=False,
        #                                                               correlationLength=correlationLength)

        lags = [lagClose, lagVolume, lagMA, lagOpenVSPrevClose, lagPercentageChange]
        CCs = [ccCloseVal, ccVolumeVal, ccMAVal, ccOpenVSPrevCloseVal,
               ccPercentageChangeVal]

        PLbls = ['Close', 'Volume', 'MA', 'OvsC', '%change']

        validLagsIndices = [i for i in range(0, lags.__len__()) if lags[i] > 0]
        validLags        = [lags[i] for i in validLagsIndices]
        validCCs         = [CCs[i] for i in validLagsIndices]
        validPLbls       = [PLbls[i] for i in validLagsIndices]

        if validCCs.__len__() < 1:
            Y_Lag, cc, lag,PLbl = 0, 0, 0, 0
        else:
            maxCC  = max(validCCs)
            maxIdx = validCCs.index(maxCC)
            lag    = validLags[maxIdx]
            cc     = validCCs[maxIdx]
            PLbl   = validPLbls[maxIdx]
            Y_Lag  = y_tags[lag - 1]

        return Y_Lag, cc, lag,PLbl


    def vote(self,binary_correlation = True,agentMode='SinLag_SinCC',correlationLength=401,PVMode=False):
        lag,cc,PLbl = 0,0,0  # PLbl relevant only for agentMode = SinLag_MuCC

        if agentMode == 'SinLag_SinCC':
            Y_Lag,cc,lag  = self.voteSinLagSinCC(binary_correlation=binary_correlation,correlationLength=correlationLength)

        elif agentMode == 'SinLag_MuCC':
            Y_Lag,cc,lag,PLbl = self.voteSinLagMuCC(binary_correlation=binary_correlation, correlationLength=correlationLength)

        elif agentMode == 'MuLag_SinCC':
            Y_Lag, cc, lag = self.voteMuLagSinCC(binary_correlation=binary_correlation,correlationLength=correlationLength)

        if lag <= 0:
            Y_Lag,cc = 0,0

        self.lag = lag
        if PVMode == True:
            Y_Lag = Y_Lag*cc

        return Y_Lag, cc, PLbl