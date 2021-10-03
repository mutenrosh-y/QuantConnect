class CalmBrownDog(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)  
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)  
        
        self.qqq = AddEquity("QQQ" ,  Resolution.Hour).Symbol
        
        self.entryTicket = None 
        self.stopMarketTicket = None
        self.entryTime = datetime.min
        self.stopMarketFillTime = datetime.min 
        self.highestPrice = 0
       


    def OnData(self, data):
        
        pass
        
