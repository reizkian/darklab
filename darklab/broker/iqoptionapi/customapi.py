import time
from darklab.broker.iqoptionapi.stableapi import IQ_Option

class IQOPTION_API:
    def __init__(self, email, password, mode):
        self.email    = email
        self.password = password
        self.mode     = mode
        # UNINITIALIEZED CLASS VARIABLE
        # self.stable_api
        # self.CLIENT_TIME
        # self.LATENCY
        # self.account_balance
        # self.asset
        # self.time_zone 
        # self.time_resolution
        # self.count_candles

    def connect(self):
        self.stableapi_iq=IQ_Option(self.email,self.password,active_account_type=self.mode)
        check, reason = self.stableapi_iq.connect()#connect to iqoption
        self.CLIENT_TIME = time.time()
        self.get_server_time()
        if check:
            print(f'connected to iqoption {self.email} {self.mode}')
            self.get_latency()
        else:
            print('failed to connect ', reason)

    def get_server_time(self):
        self.SERVER_TIME = self.stableapi_iq.get_server_timestamp()

    def get_latency(self):
        self.LATENCY = int((self.CLIENT_TIME-self.SERVER_TIME)*1000)

    def account_check_balance(self):
        mode = self.stableapi_iq.get_balance_mode()
        self.account_balance = self.Iq.get_balance()
        # print(f'{self.email} {mode} {self.account_balance}$')

    def get_candles_historicaldata(self, asset, time_zone, time_resolution, count_candles, **kwargs):
        '''
        RETURN: pandas dataframe of historical candlesticks data
        PARAM:
            [1] asset#string, name of the asset ('EURUSD', 'GBPUSD', etc)
            [2] time_resolution#int, time resolution in seconds (1,5,10,1,5,10,15,30,60,120, etc)
            [3] count_candles#int, number of candles data
            [4] timezone#int, ranging from -12 to 14 according to Corrdinated Universal Timezone (UTC) 
                input 0 for using default UTC
            [5] time_specific#int, specific UNIX timestamp in the past
        '''
        self.get_server_time()
        self.asset = asset
        self.time_zone = time_zone
        self.time_resolution = time_resolution
        self.count_candles = count_candles

        # check for specific historical time
        try:
            time_now = int(kwargs['time_specific'])
        except:
            time_now = time.time()

        RESPOND = []
        REQUEST_BATCH = self.separate1e3(count_candles)
        # request data to iqoption
        for eachBatch in REQUEST_BATCH:
            eachRespond = self.Iq.get_candles(asset, time_resolution, eachBatch, time_now)
            RESPOND = eachRespond+RESPOND
            time_now = int(eachRespond[0]["from"])-1       

        # time
        # timestamp using UNIX epoch
        '''
        Unix time is a system for describing a point in time. 
        It is the number of seconds that have elapsed since the Unix epoch, 
        excluding leap seconds. The Unix epoch is 00:00:00 UTC on 1 January 1970.
        '''
        df_responddata = pd.DataFrame(RESPOND)
        df_responddata['at'] = (df_responddata['at']/1e9).astype('int') # UNIX epoch
        df_responddata.rename(columns = {'at':'time_unix'}, inplace=True) # UNIX epoch
        
        if time_zone == 0:
            df_responddata['time_stamp'] = pd.to_datetime(df_responddata['time_unix'], unit='s')
        else:
            days_in_seconds = time_zone * 60 * 60
            df_responddata['time_unix'] = (df_responddata['time_unix'] + days_in_seconds).astype('int')
            df_responddata['time_stamp'] = pd.to_datetime(df_responddata['time_unix'], unit='s')

        # delete column
        df_responddata.drop('to', axis=1, inplace=True)
        df_responddata.drop('from', axis=1, inplace=True)
        # df_responddata.drop('time_unix', axis=1, inplace=True)
        # rearrange column
        df_responddata = df_responddata[['id','time_stamp','time_unix','open','close','min','max','volume']]
        df_responddata.set_index('time_stamp', inplace=True)

        # set meta data info
        self.time_start = str(np.array(df_responddata.index[0:])[0])
        self.time_stop  = str(np.array(df_responddata.index[-1:])[0])
        # log dataframe info
        # print(f'{self.asset} time_zone utc{self.time_zone} time_resolution {self.time_resolution}s')
        # self.print_latency()
        # print('------------------------------------')
        # df_responddata.info()
        self.print_candle_metadata()
        return df_responddata

    # --------------------------------------------------------------------------------------
    # UTILITY FUNCTION
    # --------------------------------------------------------------------------------------
    def separate1e3(self, n):
        '''
        iqoptionapi limits 1000 point data per call
        separate an integer > 1000 into list

        example:
        PARAM: n=3742
        RETURN: [1000,1000,1000,742]
        '''
        batch = []
        for i in range(n//1000):
            batch.append(1000)
        if n%1000 != 0:
            batch.append(n%1000)
        return batch