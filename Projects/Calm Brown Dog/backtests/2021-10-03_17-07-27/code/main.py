class CalmBrownDog(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        self.qqq = self.AddEquity("QQQ" ,  Resolution.Hour).Symbol

        self.entryTicket = None
        self.stopMarketTicket = None
        self.entryTime = datetime.min
        self.stopMarketOrderFillTime = datetime.min
        self.highestPrice = 0



    def OnData(self, data):

        #Checks for 30 days in fiat
        if(self.Time - self.stopMarketOrderFillTime).days < 30:
            return

        price = self.Securities[self.qqq].Price

        #Sends Limit Order
        if not self.Portfolio.Invested and not self.Transactions.GetOpenOrders(self.qqq):
            quantity = self.CalculateOrderQuantity(self.qqq, 0.9)
            self.entryTicket = self.LimitOrder(self.qqq, quantity, price, "Entry Order")
            self.entryTime = self.Time

        #Change limit Price if order not filled after a day
        if (self.Time - self.entryTime).days > 1 and self.entryTicket.Status!= OrderStatus.Filled:
            self.entryTime =  self.Time
            updateFields = UpdateOrderFields()
            updateFields.LimitPrice = price
            self.entryTicket.Update(updateFields)

        #Trail Stoploss
        if self.stopMarketTicket is not None and self.Portfolio.Invested:
            if price > self.highestPrice:
                self.highestPrice = price
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = price * 0.95
                self.stopMarketTicket.Update(updateFields)

    def onOrderEvent(self, orderEvent):

        #Eliminiated Unfilled Cases
        if orderEvent.Status != OrderStatus.Filled:
            return

        #Sends Stop Loss order if Limit Order is filled
        if self.entryTicket is not None and self.entryTicket.OrderId == orderEvent.OrderID:
            self.stopMarketTicket = self.StopMarketOrder(self.qqq, self.entryTicket.Quantity,
                                                         0.95*self.entryTicket.AverageFillPrice)
        #Store Stop Loss order Time
        if self.stopMarketTicket is not None and self.stopMarketTicket.OrderID ==  orderEvent.OrderID:
            self.stopMarketOrderFillTime = self.Time
            self.highestPrice = 0
