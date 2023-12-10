class table_order_item():
    def __init__(self):
        #here the target is to create a table of itens, wich products and how much every client did buy.

        self.prepare()
        self.random_client_status()
        self.print_table()

    def prepare(self):
        #import tools
        from A01_TOOL_BOX import tool_box
        tool_box=tool_box()
    
        self.pandas=tool_box.pandas
        self.random=tool_box.random
        self.datetime=tool_box.datetime 

        #import data
        self.sales_orders=self.pandas.read_csv(filepath_or_buffer='./NEW_DATASET/A05_TAB_ORDER_MAIN.csv',
                                               sep=';',decimal=',')
        
        self.products=self.pandas.read_csv(filepath_or_buffer='./NEW_DATASET/A01_TAB_PRODUCTS.csv',sep=';',decimal=',')

        self.client=self.sales_orders.groupby(['ID_client']).count()[[]]

    def random_client_status(self):
        #first of all I will create two random factors to states how good is the client, both in volume and products
        self.client['factor_volume']=self.client.index.map(lambda x: self.random.randint(1,100))
        self.client['factor_products']=self.client.index.map(lambda x: self.random.randint(1,100))

        #chose the products every client gonna buy for each order
        self.sales_orders=self.pandas.merge(left=self.sales_orders,right=self.client,left_on='ID_client',right_index=True,how='left')
        self.sales_orders['merge_id']=0
        self.products['merge_id']=0
        self.sales_orders=self.pandas.merge(left=self.sales_orders,right=self.products[['merge_id','ID_products','units/pack']],left_on='merge_id',right_on='merge_id',how='left').drop(columns=['merge_id'])
        self.sales_orders['buy_packs']=self.sales_orders['factor_products'].map(lambda x:self.random.randint(1,100)<=x)
        self.sales_orders=self.sales_orders.loc[self.sales_orders['buy_packs']==True,:] #remove the filtered records

        #state the volume based on the factor_volume
        self.sales_orders['buy_packs']=self.sales_orders['units/pack'].map(lambda x:x)

        products_volume_range={ 
            0:[[0,18],[1,5]],
            1:[[19,24],[3,10]],
            2:[[25,68],[10,20]],
            3:[[75,200],[20,30]]
        }
        for layer in products_volume_range:
            vol_filter=products_volume_range[layer][0]
            vol_range=products_volume_range[layer][1]
            self.sales_orders['buy_packs']=self.sales_orders['buy_packs'].map(lambda x:self.random.randint(vol_range[0],vol_range[1]) if x>=vol_filter[0] and x<vol_filter[1] else x)
        
        cluster_factor={
            'A':1,
            'B':2,
            'C':3,
            'D':4
        }
        for cluster in cluster_factor:
            self.sales_orders.loc[self.sales_orders['cluster']==cluster,'cluster_factor']=cluster_factor[cluster]
        self.sales_orders['buy_packs']=self.sales_orders['buy_packs']*self.sales_orders['cluster_factor']
        #format dataset
        self.sales_orders.drop(columns=['factor_volume','factor_products','units/pack','cluster_factor','cluster','ID_sector'],inplace=True)
        self.sales_orders.rename(columns={'buy_packs':'pack'})
    def print_table(self):
        self.sales_orders.to_csv('./NEW_DATASET/A06_TAB_ORDER_ITEM.csv',sep=';',decimal=',',index=False)
