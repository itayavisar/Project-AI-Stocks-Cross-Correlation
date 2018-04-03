import numpy as np

def normalize(signal):
    ret_signal=[]
    if np.std(signal)!=0:
        ret_signal = (signal-np.average(signal))/np.std(signal)
    else:
        ret_signal.extend(signal)
    return ret_signal


def get_correlation_and_lag(curStk, corStk, correlationLength, binary_correlation=True, signal='Close'):
    if signal == 'Close':
        signalA = curStk.Close
        signalV = corStk.Close
    elif signal == 'Volume':
        signalA = curStk.Volume
        signalV = corStk.Volume
    elif signal == 'MA':
        signalA = curStk.getMAVector(period=14, length=correlationLength + 1)
        signalV = corStk.getMAVector(period=14, length=correlationLength + 1)
    elif signal == 'GCR':
        signalA = curStk.getGCRVec(short_term=14, long_term=200)
        signalV = corStk.getGCRVec(short_term=14, long_term=200)
    elif signal == 'DCR':
        signalA = curStk.getDCRVec(short_term=14, long_term=200)
        signalV = corStk.getDCRVec(short_term=14, long_term=200)
    elif signal == 'RSI':
        signalA = curStk.getRSIVec(period=14, length=correlationLength)
        signalV = corStk.getRSIVec(period=14, length=correlationLength)
    elif signal == 'OpenVSPrevClose':
        signalA = curStk.getOpenVsPrevClose()
        signalV = corStk.getOpenVsPrevClose()
    elif signal == 'PercentageChange':
        signalA = curStk.getPercentageChange()
        signalV = corStk.getPercentageChange()

    if binary_correlation:
        binA = curStk.get_tags_history(signal, length=correlationLength)[0:correlationLength]
        binV = corStk.get_tags_history(signal, length=correlationLength)[0:correlationLength]
        #if binA.__len__() != binV.__len__():
        #    print("Itay stop")
        cc = np.correlate(binA, binV, mode='same')
        cc = np.asarray(cc) / (np.linalg.norm(binA) * np.linalg.norm(binV))
    else:
        a = normalize(signalA[0:correlationLength])
        v = normalize(signalV[0:correlationLength])
        cc = np.correlate(a, v, mode='same')
        if max(cc) != 0:
            cc = np.asarray(cc) / (np.linalg.norm(a) * np.linalg.norm(v))

    lag = (round(cc.__len__() / 2) - np.argmax(cc))
    maxCC = max(cc)
    return maxCC, lag

