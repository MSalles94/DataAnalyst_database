class table_products():
    #create a table with the products information
    def __init__(self) -> None:
        self.prepare()
        self.get_products_data()
        self.create_clusters()
        self.create_primary_key()
        self.state_product_cost()
        self.order_table()
        self.print_to_csv()

    def prepare(self):
        from A01_TOOL_BOX import tool_box
        self.ToolBox=tool_box()

    def get_products_data(self):
        #import data
        self.tab_products=self.ToolBox.data
        #convert some columns into number type
        self.tab_products['Quantity Ordered']=self.tab_products['Quantity Ordered'].map(lambda x:int(x))
        self.tab_products['Price Each']=self.tab_products['Price Each'].map(lambda x:float(x))
        #group the diferent products
        self.tab_products=self.tab_products[['Product','Quantity Ordered','Price Each']].groupby(['Product']).sum()
        #get the average price. States it as the target price for marging calcules.
        self.tab_products['Target_price']=self.tab_products['Price Each']/self.tab_products['Quantity Ordered']
        self.tab_products['Target_price']=self.tab_products['Target_price'].map(lambda x:round(x,2))
        #state a minimum quantity to buy, units per pack. Based on the Quantity ordered
        self.tab_products['units/pack']=self.tab_products['Quantity Ordered'].map(lambda x:int(x/30))
        self.tab_products.drop(inplace=True,columns=['Quantity Ordered','Price Each'])

    def create_clusters(self):
        #Classify the products in clusters
        reference={
            'Monitor':['Monitor','TV'],
            'Others':['Batteries','Wired','Cable','Headphones'],
            'Phone':['Phone'],
            'home_appliances':['Dryer','Washing'],
            'Laptop':['Laptop']
        }
        self.tab_products['cluster']=self.tab_products.index
        for i in reference:
            for j in reference[i]:
                self.tab_products['cluster']=self.tab_products['cluster'].map(lambda x:i if x.find(j)!=-1 else x)    

    def create_primary_key(self):
        #create an ID to each product to use as primary key
        reference={
            'Monitor':'01',
            'Others':'02',
            'Phone':'03',
            'home_appliances':'04',
            'Laptop':'05'
        }
        self.tab_products.reset_index(inplace=True)
        self.tab_products['ID_products']=self.tab_products['cluster']
        
        for i in reference:
            self.tab_products['ID_products']=self.tab_products['ID_products'].map(lambda x:reference[i] if x==i else x)
        self.tab_products['ID_products']='9'+self.tab_products['ID_products']+self.tab_products.index.map(lambda x:str(x).zfill(3))

    def state_product_cost(self):
        reference={
            'Monitor':0.20,
            'Others':1.00,
            'Phone':0.30,
            'home_appliances':0.20,
            'Laptop':0.25
        }
        self.tab_products['markup']=self.tab_products['cluster']
        for i in reference:
            self.tab_products['markup']=self.tab_products['markup'].map(lambda x:x if x!=i else reference[i])

        self.tab_products['cost']=self.tab_products['Target_price']/self.tab_products['markup'].map(lambda x:(x+1))
        self.tab_products['cost']=self.tab_products['cost'].map(lambda x:round(x,2))

    def order_table(self):
        columns=['ID_products','Product','cluster','units/pack','cost','markup','Target_price']
        self.tab_products=self.tab_products[columns]


    def print_to_csv(self):

        self.tab_products.to_csv(path_or_buf='NEW_DATASET/A01_TAB_PRODUCTS.csv',sep=';',decimal=',',index=False)

