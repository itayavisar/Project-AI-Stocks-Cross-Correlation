import pandas as pd
from yahoo_historical import Fetcher

# SP500_symbol = ['AAPL', 'ABT', 'ABBV', 'ACN', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL',
#                 'AMG', 'A', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL',
#                 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME',
#                 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK',
#                 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BXLT',
#                 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX',
#                 'BMY', 'BRCM', 'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CPB', 'COF', 'CAH', 'HSIC',
#                 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK',
#                 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS',
#                 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'CNX', 'ED', 'STZ',
#                 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL',
#                 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV','DPS',
#                 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA','EMR',
#                 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC',
#                 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE',
#                 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GPS',
#                 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG',
#                 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES',
#                 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST','HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE',
#                 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI',
#                 'JPM', 'JNPR', 'KSU', 'K', 'KEY','KMB', 'KIM', 'KMI', 'KLAC', 'KSS','KR', 'LB','LLL', 'LH',
#                 'LRCX', 'LM', 'LEG', 'LEN','LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW',
#                 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC',
#                 'MCD', 'MCK','MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ',
#                 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL',
#                 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG',
#                 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR',
#                 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI','PNC','RL', 'PPG',
#                 'PPL', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH',
#                 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG','RHI',
#                 'ROK', 'COL', 'ROP', 'ROST', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW',
#                 'SPG', 'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE','SWK', 'SBUX','STT', 'SRCL', 'SYK',
#                 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC','TXN', 'TXT', 'HSY', 'TRV',
#                 'TMO', 'TIF', 'TWX', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP','FOXA', 'TSN','UA', 'UNP', 'UNH',
#                 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO','VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB',
#                 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT','ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR','WMB',
#                 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX','XL', 'XYL','YUM', 'ZBH', 'ZION', 'ZTS','TSLA']

class csvGenerator:
    @staticmethod
    def loadCsv(symbols: list, output_dir: str, start_date = [2015, 5, 24], end_date = [2020, 10, 9]):

        import time
        for symbol in symbols:
            print("generate csv to symbol ", symbol, "...")
            time.sleep(2)
            data = Fetcher(symbol, start_date, end_date)
            try:
                with open(output_dir + '/' + symbol + '.csv', 'w') as csvfile:
                    dataf = pd.DataFrame(data.getHistorical())
                    if dataf.empty:
                        raise Exception('dataframe is empty')
                    dataf.to_csv(path_or_buf=csvfile, mode='w')
                print("success generate csv to symbol ", symbol)
            except:
                print("FAILD!!!! generate csv to symbol ", symbol)
if __name__ == '__main__':
    symbols =['AAPL','AMD','TSLA','NVDA','MSFT']
    out_dir = './csv_files_08_10_2020'

    # [YYYY,M,D]
    start_date = [2015,5,24]
    end_date = [2020,10,9]
    csvGenerator.loadCsv(symbols, out_dir, start_date, end_date)