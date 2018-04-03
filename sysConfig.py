import stocksDatabase as DB
#cur_symbol = DB.csv_path+'\\QCOM.csv'
#cur_symbol = DB.csv_path+'\\AAPL_10lag.csv'
#cur_symbol = DB.csv_path+'\\AAPL.csv'
cur_symbol = DB.csv_path+'\\AA.csv' #--- for the experiment
#cur_symbol = DB.csv_path+'\\AEE.csv'
#cur_symbol = DB.csv_path+'\\AEP.csv'
#cur_symbol = DB.csv_path+'\\AVGO.csv'
#cur_symbol = DB.csv_path + '\\^GSPC.csv'
#cur_symbol = DB.csv_path + '\\BBY.csv'
#cur_symbol = DB.csv_path + '\\AAL.csv'
#cur_symbol = DB.csv_path + '\\MLNX.csv'

# featuresMode = 'BEST_AGENT' / 'NONE' #
featuresMode = 'NONE'

# binary_correlation = True/False #
binary_correlation = True

# PVMode = True/False #
PVMode = True

# agentMode = 'SinLag_SinCC'/'SinLag_MuCC'/'MuLag_SinCC' #
agentMode = 'MuLag_SinCC'

length = 401
correlation_length = 401
number_of_samples = 50