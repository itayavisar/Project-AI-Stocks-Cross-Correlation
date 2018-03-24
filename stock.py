import stocksDatabase as DB
import numpy as np
import glob
import agent as ag
import time
import SPFG as SP

csv_path_debug = './csv_files'
csv_sp500_path = './csv_files_sp500'
csv_path = csv_sp500_path
list_of_files = glob.glob(csv_path+'/*.csv')

def vectorSubstract(a,b=None):
    retval = np.zeros(a.__len__())
    i = 0
    if b is None:
        b = a[1:]
    for cura, curb in zip(a, b):
        retval[i] = cura-curb
        i += 1
    return retval


class Stock:

    def __init__(self,open=[], close=[], high=[], low=[], volume=[],name=None,base=0):
        self.Open = open[base:]
        self.Close = close[base:]
        self.High = high[base:]
        self.Low = low[base:]
        self.Volume = volume[base:]
        self.name = name
        self.base = base

    def init_from_symbol(self,symbol,base=0):
        self.Open  = DB.Database[symbol]['Open'][base:]
        self.Close = DB.Database[symbol]['Close'][base:]
        self.High  = DB.Database[symbol]['High'][base:]
        self.Low   = DB.Database[symbol]['Low'][base:]
        self.Volume = DB.Database[symbol]['Volume'][base:]
        self.Date   = DB.Database[symbol]['Date'][base:]
        self.name   = symbol
        self.base   = base

    def getMA(self,period,prev_days=0):
        if prev_days is 0:
            ma = np.sum(self.Close[-(period):])/period
        else:
            ma = np.sum(self.Close[-(period+prev_days):-prev_days])/period
        return ma

    def getOpenVsPrevClose(self):
        openVsClosePrevDay = (np.divide(self.Open[0:-1], self.Close[1:]))
        return openVsClosePrevDay

    # Returns a moving average vector over all the stock Close signal
    def getMAVector(self, period,length = 0):
        start = 0
        end = start + period
        if length == 0 :
            length = self.Close.__len__()

        vec= []
        while end < length:
            end = start + period
            tmp_window_to_avg = self.Close[start:end]
            start+=1
            vec.append(np.average(tmp_window_to_avg))
        return vec

    def getGCRVec(self,short_term,long_term,length=401):
        gc = []
        ma_short_term_vec = self.getMAVector(short_term,length=length)
        ma_long_term_vec = self.getMAVector(long_term,length=length)
        for cur in range(0,ma_long_term_vec.__len__()-1):
            if ma_short_term_vec[cur] >= ma_long_term_vec[cur] and\
                            ma_short_term_vec[cur+1] < ma_long_term_vec[cur+1]:
                gc.append(1)
            else:
                gc.append(0)
        return gc

    def getDCRVec(self, short_term, long_term,length=401):
        dc = []
        ma_short_term_vec = self.getMAVector(short_term,length=length)
        ma_long_term_vec = self.getMAVector(long_term,length=length)
        for cur in range(0, ma_long_term_vec.__len__()-1):
            if ma_short_term_vec[cur] <= ma_long_term_vec[cur] and\
                            ma_short_term_vec[cur+1] > ma_long_term_vec[cur+1]:
                dc.append(1)
            else:
                dc.append(0)
        return dc

    def get_dclose_dt_vector(self):
        return vectorSubstract(self.Close)

    def getPercentageChange(self):
        vec =  vectorSubstract(self.Close)
        for i in range(0,vec.__len__()-1):
            vec[i] /= self.Close[i+1]
        return vec

    def get_avg_gain_vector(self, period=14,length=401):
        tmp_gain_vec=[]
        for i in range(0,length):
            if self.Close[i]>self.Close[i+1]:
                tmp_gain_vec.append(self.Close[i]-self.Close[i+1])
            else:
                tmp_gain_vec.append(0)

        avg_gain_vec = Stock(close=tmp_gain_vec).getMAVector(period=period,length=length)
        return avg_gain_vec

    def get_avg_loss_vector(self, period=14,length=401):
        tmp_loss_vec=[]
        for i in range(0,length):
            if self.Close[i]<self.Close[i+1]:
                tmp_loss_vec.append(abs(self.Close[i]-self.Close[i+1]))
            else:
                tmp_loss_vec.append(0)

        avg_loss_vec = Stock(close=tmp_loss_vec).getMAVector(period=period,length=length)
        return avg_loss_vec

    def getRSIVec(self,period,length):
        gain_vec = self.get_avg_gain_vector(period,length=length)
        loss_vec = self.get_avg_loss_vector(period,length=length)
        rsi_vec = []
        for i in range(0,gain_vec.__len__()):
            if loss_vec[i]==0:
                rsi_vec.append(100)
            else:
                rsi_vec.append(100-(100/(1+(gain_vec[i]/loss_vec[i]))))
        return(rsi_vec)

    def get_tags_history(self,attr,length=-1):
        ret_list = []
        samples = self.Close
        #if length==-1:
            #length=samples.__len__()
        if attr is 'Close':
            samples=self.Close
        elif attr is 'Volume':
            samples = self.Volume

        #for i in range(1, samples.__len__()):
        for i in range(1, length+1):
            if samples[i-1] > samples[i]:
                ret_list.append(1)          # current sample is higher from previous
            else:
                ret_list.append(0)
        return ret_list

#    def get_correlation_and_lag(self, cor_stock, correlationLength=401, binary_correlation=True,signal = 'Close'):
#        if signal == 'Close':
#            signalA = self.Close
#            signalV = cor_stock.Close
#        elif signal == 'Volume':
#            signalA = self.Volume
#            signalV = cor_stock.Volume
#        elif signal == 'MA':
#            signalA = self.getMAVector(period=14,length=correlationLength+1)
#            signalV = cor_stock.getMAVector(period=14, length=correlationLength+1)
#        elif signal == 'GCR':
#            signalA = self.getGCRVec(short_term=14, long_term=200)
#            signalV = cor_stock.getGCRVec(short_term=14, long_term=200)
#        elif signal == 'DCR':
#            signalA = self.getDCRVec(short_term=14, long_term=200)
#            signalV = cor_stock.getDCRVec(short_term=14, long_term=200)
#        elif signal == 'RSI':
#            signalA = self.getRSIVec(period=14,length=correlationLength)
#            signalV = cor_stock.getRSIVec(period=14,length=correlationLength)
#        elif signal == 'OpenVSPrevClose':
#            signalA = self.getOpenVsPrevClose()
#            signalV = cor_stock.getOpenVsPrevClose()
#        elif signal == 'PercentageChange':
#            signalA = self.getPercentageChange()
#            signalV = cor_stock.getPercentageChange()

#        a = SP.normalize(signalA[0:correlationLength])
#        v = SP.normalize(signalV[0:correlationLength])

#        if binary_correlation:
#            binA = self.get_tags_history(signal,length=correlationLength)
#            binV = cor_stock.get_tags_history(signal,length=correlationLength)
#            cc = np.correlate(binA, binV, mode='same')
#            cc = np.asarray(cc) / (np.linalg.norm(binA) * np.linalg.norm(binV))
#        else:
#            cc = np.correlate(a, v, mode='same')
#            if max(cc)!=0:
#                cc = np.asarray(cc) / (np.linalg.norm(a) * np.linalg.norm(v))

#        lag = (round(cc.__len__() / 2) - np.argmax(cc))
#        maxCC= max(cc)
#        return maxCC, lag

    def get_correlated_symbols(self, length, binary_correlation=True):
        print("getting correlations for stock: ", self.name)
        correlated_symbols = {}
        correlated_symbols[self.name] = {}
        for correlated_stock_symbol in list_of_files:
            if correlated_stock_symbol != self.name:
                cor_stock = Stock()
                cor_stock.init_from_symbol(correlated_stock_symbol,base=self.base)
                ccClose,lagClose = SP.get_correlation_and_lag(self,cor_stock,binary_correlation=binary_correlation)

                correlated_symbols[self.name][cor_stock.name] = [ccClose,lagClose]
        return correlated_symbols

    def getFeatures(self, length, correlation_length=400, featuresMode = 'BEST_AGENT',
                    binary_correlation=True,
                    agentMode=0,PVMode=False):
        print("getting Features with:")
        print("featuresMode = ",featuresMode)
        print("binary_correlation = ", binary_correlation)
        print("agentMode = ", agentMode)
        samples_with_features = []

        # build features #
       # ma_vec = SP.normalize(self.getMAVector(ma_period))
       # gc_vec = self.getGCRVec(short_term, long_term)
       # dc_vec = self.getDCRVec(short_term, long_term)
       # dcolse_dt = SP.normalize(self.get_dclose_dt_vector())
       # d2colse_d2t = SP.normalize(Stock(dcolse_dt, dcolse_dt).get_dclose_dt_vector())
       # change_percentage = self.getPercentageChange()
       # rsi_vec = self.getRSIVec(rsi_period)
        openVsPrevClose = self.getOpenVsPrevClose()

        for i in range(0, length):  # Not including sample #base because it has not own tag value
            #print("Inside getFeatures on sample = ",i)
            stockToPredict = Stock()
            correlatedStock = Stock()
            stockToPredict.init_from_symbol(self.name,base=self.base+i+1)
            agent_features = []
            bestAgentCC = 0
            bestAgentVotes= [0 , 1]
            bestAgentLag=0
            bestAgentSymbol = DB.csv_path + '\\NONE_SYMBOL.csv'
            bestAgentPLbl = 0
            PLbl = 0
            for correlate_symbol in list_of_files:
                if correlate_symbol == self.name:
                    continue
                #print("IN PROGRESS correlated symbol = ",correlate_symbol)
                correlatedStock.init_from_symbol(correlate_symbol, base=stockToPredict.base)
                agent = ag.Agent(stockToPredict=stockToPredict,correlatedStock=correlatedStock)
                if agentMode == 'SinLag_MuCC':
                    tag, lag, PLbl = agent.vote(binary_correlation=binary_correlation, agentMode=agentMode,PVMode=PVMode)
                    votes = [tag,lag]
                else:
                    tag, lag, *rest = agent.vote(binary_correlation=binary_correlation, agentMode=agentMode,PVMode=PVMode)
                    votes = [tag,lag]

                #update bestAgent
                if (votes[1] > bestAgentCC and agent.lag > 0):
                    bestAgentSymbol = correlate_symbol
                    bestAgentCC = votes[1]
                    bestAgentVotes = votes
                    bestAgentLag = agent.lag
                    bestAgentPLbl = PLbl

                if featuresMode == 'BEST_AGENT':
                    agent_features = bestAgentVotes
                elif featuresMode == 'SinLag_MuCC':
                    bestAgentSymbol = 'agentMode : SinLag_MuCC'
                    bestAgentCC = 'agentMode : SinLag_MuCC'
                    bestAgentVotes = 'agentMode : SinLag_MuCC'
                    bestAgentLag = 'agentMode : SinLag_MuCC'
                    agent_features.extend(votes)
                else:
                    agent_features.extend(votes)


            samples_with_features.append(agent_features)
            #samples_with_features.append(
            #    [y_lagClose, ccClose,y_lagVolume,ccVolume ,y_lagClose * corr_valClose, (float(y_lagClose * corr_valClose) / lagClose), openVsPrevClose[i]])
            # samples_with_features.append([corr_val, (float(y_lag * corr_val) / lag), openVsPrevClose[i]])
            # samples_with_features.append([y_lag,corr_val,y_lag*corr_val,(float(y_lag*corr_val)/lag),ma_vec[i],gc_vec[i],
            #                              dc_vec[i],dcolse_dt[i],d2colse_d2t[i],change_percentage[i],rsi_vec[i],ma_vec2[i],
            #                              gc_vec2[i],dc_vec2[i],dcolse_dt_2[i],d2colse_d2t_2[i],change_percentage2[i],
            #                              rsi_vec2[i]],openVsPrevClose[i])

        samples_with_features = np.asarray(samples_with_features)
        #return samples_with_features, correlate_symbol, lagClose, corr_valClose
        #return samples_with_features, correlate_symbol, votes[2], votes[1]
        return samples_with_features, bestAgentSymbol,bestAgentCC, bestAgentLag,bestAgentPLbl

















#a=[1,10,5,15,20]
#stk1=Stock(a,a,a,a,a)
#z= stk1.getPercentageChange()
#print(z)
#z=stk1.getGCRVec(2,8)
#print("z is:",z)