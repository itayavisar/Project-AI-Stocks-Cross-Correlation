import matplotlib.pyplot as plt
import stocksDatabase as DB
import stock as stk
import numpy as np

from sys import argv
import SPFG as SP

if argv.__len__() > 1:
    window_length = int(argv[1])
else:
    window_length = 400  # default

if argv.__len__() > 2:
    if argv[2] == 'binary':
        binary_correlation = True
    else:
        binary_correlation = False
else:
    binary_correlation = True # default

cur_symbol = DB.csv_path+'\\AAPL_10lag.csv'
corr_symbol = DB.csv_path+'\\AAPL.csv'

cur_stk = stk.Stock()
corr_stk = stk.Stock()
cur_stk.init_from_symbol(cur_symbol)
corr_stk.init_from_symbol(corr_symbol)
print(window_length)
if(window_length > cur_stk.Close.__len__()):
    print("window_length is bigger than",cur_stk.Close.__len__())
    exit(1)
curStkSignal = SP.normalize(cur_stk.Close[0:window_length])
corrStkSignal = SP.normalize(corr_stk.Close[0:window_length])

binCurStkSignal = cur_stk.get_tags_history('Close',length=window_length)
binCorrStkSignal = corr_stk.get_tags_history('Close',length=window_length)

plt.figure(1)
plt.subplot(311)
plt.xlabel("timeline")
plt.ylabel("stock value")
plt.title("Stocks AAPL vs AAPL_10Lag , Window Length = "+window_length.__str__())
plt.plot(curStkSignal, label="AAPL_10Lag",color='blue')
plt.plot(corrStkSignal, label="AAPL",color='yellow')
plt.legend()

if binary_correlation:
    signalA = binCurStkSignal
    signalB = binCorrStkSignal
else:
    signalA = curStkSignal
    signalB = corrStkSignal

cc = np.correlate(signalA,signalB,mode='same')
cc = cc/(np.linalg.norm(signalA)*np.linalg.norm(signalB))
cc = np.asarray(cc)

plt.subplot(313)

start = int(cc.__len__()/2)
end = cc.__len__()-start

x = [i for i in range(-start,end)]
plt.plot(x,cc[::-1], label="cc",color='green')
lag = (round(cc.__len__() / 2) - np.argmax(cc))
lbl = 'lag = '+lag.__str__()
plt.scatter(lag,max(cc), label=lbl,color='black')
print("lag = ",lag)
plt.legend(handles=[lag,max(cc)],labels=['lag','CC'])
plt.legend()
plt.title('CC Window Length = '+window_length.__str__())
plt.xlabel("CC Time Lag")
plt.ylabel("CC Value")
plt.show()

