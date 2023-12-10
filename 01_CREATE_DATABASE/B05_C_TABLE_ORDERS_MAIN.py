class table_order_main():
    def __init__(self) -> None:
        self.prepare()
        self.order_day()
        self.order_number()
        self.print_data()
      

    def prepare(self):
        #import tools
        from A01_TOOL_BOX import tool_box
        tool_box=tool_box()
    
        self.pandas=tool_box.pandas
        self.random=tool_box.random
        self.datetime=tool_box.datetime 

        #import data
        self.sales_orders=self.pandas.read_csv(filepath_or_buffer='./NEW_DATASET/A03_TAB_CLIENTS.csv',
                                               sep=';',decimal=',')[['ID_client','cluster','visit_day','ID_sector']]
        
    def order_day(self):
        #to keep the problem simple, every client can make only at his visit day
        #get a set of dates
        import datetime
        dt_start=datetime.date(year=2023,month=1,day=2)
        days=datetime.date(year=2023,month=4,day=30)-dt_start
        days=days.days        
        dt_list=[dt_start + datetime.timedelta(days=i) for i in range(days)]
        dt_list=[i for i  in dt_list]
        dt_list=self.pandas.DataFrame(dt_list,columns=['Date'])
        dt_list['week']=dt_list['Date'].map(lambda x:x.isocalendar().week)
        dt_list['weekDay']=dt_list['Date'].map(lambda x:x.isocalendar().weekday)
        dt_list['month']=dt_list['Date'].map(lambda x:x.month)
        #set the date to the client
        self.sales_orders=self.pandas.merge(left=self.sales_orders,right=dt_list,left_on='visit_day',right_on='weekDay',how='left')
        self.sales_orders.drop(columns=['weekDay','visit_day'],inplace=True)
        #set the chance the client can by nothing at month
        self.sales_orders.loc[:,'filter']=''
        for i in self.sales_orders['ID_client'].unique():
            for j in self.sales_orders['month'].unique():
                if self.random.random()<0.05: # 5% of chance a client will not buy any product at the month
                    filter=(self.sales_orders['ID_client']==i) & (self.sales_orders['month']==j)
                    self.sales_orders.loc[filter,'filter']='remove'
            if self.random.random()<0.10: #10% of chance a client will not buy at the visit
                filter=(self.sales_orders['ID_client']==i) 
                self.sales_orders.loc[filter,'filter']='remove'
        #remove the filter orders
        self.sales_orders=self.sales_orders[self.sales_orders['filter']!='remove'].reset_index(drop=True)
        self.sales_orders.drop(columns=['filter'],inplace=True)
    
    def order_number(self):
        #set an ID of the order to register 
        self.sales_orders['order_n']=0
        self.sales_orders.sort_values(by=['Date','ID_client'],inplace=True)
        self.sales_orders.reset_index(inplace=True,drop=True)
        new=1
        self.sales_orders.loc[0,'order_n']=1
        for i in self.sales_orders.index[1:]:
            if self.sales_orders.loc[i,'Date']==self.sales_orders.loc[i-1,'Date']:
                new=self.sales_orders.loc[i-1,'order_n']+1
            else:
                new=1
            self.sales_orders.loc[i,'order_n']=new
        self.sales_orders['order_n']=self.sales_orders['Date'].map(lambda x:str(x).replace('-','').zfill(4))+self.sales_orders['order_n'].map(lambda x:str(x))
        self.sales_orders.drop(columns=['week','month'],inplace=True)
    
    def print_data(self):
        self.sales_orders.to_csv('NEW_DATASET/A05_TAB_ORDER_MAIN.csv',sep=';',decimal=',',index=False) 
