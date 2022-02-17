from iqoptionapi.stable_api import IQ_Option

class IqoptionAPI:
    def __init__(self, email, password, mode):
        self.email    = email
        self.password = password
        self.mode     = mode
    
    def connect(self):
        self.iq=IQ_Option(self.email,self.password,active_account_type=self.mode)
        check, reason=self.Iq.connect()#connect to iqoption
        self.CLIENT_TIME = time.time()
        if check:
            print(f'connected to iqoption {self.email} {self.mode}')
            self.print_latency()
        else:
            print('failed to connect ', reason)

    def print_latency(self):
        self.LATENCY= int((self.CLIENT_TIME-self.SERVER_TIME)*1000)
        print(f'latency {self.LATENCY} ms')