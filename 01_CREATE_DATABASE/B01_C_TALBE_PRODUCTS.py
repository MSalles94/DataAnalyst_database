class table_products():
    #create a table with the products information
    def __init__(self) -> None:
        self.prepare()
        self.organize_products()
        self.create_clusters()

    def prepare(self):
        from A01_TOOL_BOX import tool_box
        self.ToolBox=tool_box()

    def organize_products(self):
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
        reference={
            'Monitor':'Monitor'
        }
        for i in reference:
            self.tab_products['cluster']=self.tab_products.index.map(lambda x:i if x.find(reference[i])!=-1 else '')
      
