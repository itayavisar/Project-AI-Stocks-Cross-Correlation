# Project-AI-Stocks-Cross-Correlation
This Project is about to predict the directional movements of a stock, using cross-correltion with other stocks

################################################################################
Description
################################################################################

Our code implement a system for stock's directional movements prediction, using Cross-Correlation between other stocks. The system is configurable by various parameters.

################################################################################
Objective
################################################################################ 

The Project Objective was to predict the daily directional movement of a stock. The Data we used of the historical data for each stock for a given window of time.
The historical data contains the stocks' Close,Open,High,Low prices and the Volume of the stocks. 

################################################################################
Pre-Condition
################################################################################

CSV files of the historical data with headers of No.,Date,Open,High,Low,Close,Adj Close, Volume. 
The order of column is important, but the headers are not. all the data should be from the second row.
The rows are ordered by chronological timeline from past to present as the rows go down.
All CSV files, should be located in path '.\csv_files_sp500'

################################################################################
Generatin CSVs data
################################################################################ 

After creating the directory '.\csv_files_sp500', edit in file csv_generate.py the requested stocks for csv generation by editing the list variable SP500_symbol.
This script generate from the list all the requested CSVs for the Database in path '.\csv_files_sp500'.

################################################################################
Running the Code
################################################################################

config:
=======
First choose the system configuration in file sysConfig.py.
in the config file you choose the: 
-agentMode:  'SinLag_SinCC'/'SinLag_MuCC'/'MuLag_SinCC' 
-featureMode: 'BEST_AGENT' / 'NONE' 
-Probabily Vote Mode: True/False
-binary_correlation mode: True/False
-correlation_length: integer
-number_of_samples for train: integer

run stockPredictor:
===================
1)run the system from stockPredictor.py. 
2)Choose the symbol of the stock to predict from the generated CSVs. 
3)Choose the Date within the scope of the generated CSVs. type the Date in the format of YYYY-mm-dd
example:
1) $python stockPredictor.py
2) $AA
3) $2017-04-28

run tests:
==========
1) choose the stock for running on it tests in the config by this row-
cur_symbol = DB.csv_path+'\\<symbol>.csv' 
where <symbol> is the chosen symbol
2) run main.py 

################################################################################
Result
################################################################################ We submitted our Ridge-Random Forest model to the Boston Data Week hackathon hosted at Hack/Reduce. Information about the competition is available at https://inclass.kaggle.com/c/boston-data-festival-hackathon

During running the tests the results are printed to the console. At the end of the tests the results are plot by a scatter graph

################################################################################

Files
################################################################################ process.ipynb notebook Notebook describing our work and our main contributions

sysConfig.py      - the configuration file which hold all the configurations for the system
csv_generate.py   - need to run as pre-condition in order to generate the relevant CSVs in the reuqired dates.
stocksDatabase.py - read the CSVs and organize all the raw data for convenient access
SPFG.py           - signal processor and feature generation. apply the normalization. calculates CC and the relevant lag
agent.py          - implement the agent module 
stock.py          - implement the stock module 
stockPredictor.py - the stock predictor system for a single required date
main.py           - run tests over several recent iterations
CCTuning.py       - used for tunning the parameters for the CC by having same stocks
                    run: $python CCTuning.py <window_length> <string for binary for binary CC>
predictor_sts.py  - hold the statistic databases
build_correlation_table.py - build table of the CC values between all stocks
correlations.csv  - table of all the stocks' CC between each other (on a specific date). generated from file build_correlation_table.py
