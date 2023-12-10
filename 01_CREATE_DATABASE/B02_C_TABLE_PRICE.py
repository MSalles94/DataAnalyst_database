class table_price():
    def __init__(self) -> None:
        self.prepare()
        self.prices_and_reference()
        self.print_to_csv()
    
    def prepare(self):
        from A01_TOOL_BOX import tool_box
        tool_box=tool_box()

        self.pandas=tool_box.pandas
        self.random=tool_box.random

        self.ref_prod=self.pandas.read_csv('NEW_DATASET/A01_TAB_PRODUCTS.csv',decimal=',',sep=';')
        
    def prices_and_reference(self):
        #create a random table to be used based on the client volume
        parameter={ #random parameter to construct prices
            'tab_1':[7,15],
            'tab_2':[5,7],
            'tab_3':[3,5],
            'tab_4':[0,3],
            'tab_5':[-2,0],
            'tab_6':[-10,-2]
        }
        columns=['ID_products','markup','cost']
        ref_prod=self.ref_prod[columns]
        tables=[]
        for i in parameter:
            table=ref_prod.copy()
            table['table']=i
            table['random_factor']=table.index.map(lambda x: self.random.randint(parameter[i][0],parameter[i][1])/100)
            tables.append(table)
        self.table_price=self.pandas.concat(tables)
        self.table_price['table_ID']=self.table_price['table']+'_'+self.table_price['ID_products'].map(lambda x:str(x))
        self.table_price['random_factor']=self.table_price['markup']+self.table_price['random_factor']
        self.table_price['unit_price']=self.table_price['cost']*(1+self.table_price['random_factor'])
        self.table_price['unit_price']=self.table_price['unit_price'].map(lambda x:round(x,2))
        #organize table
        columns=['table_ID','ID_products','table','unit_price']
        self.table_price=self.table_price[columns]

    def print_to_csv(self):
        self.table_price.to_csv('NEW_DATASET/A02_TAB_PRICE.csv',sep=';',decimal=',',index=False)
