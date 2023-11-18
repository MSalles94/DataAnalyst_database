coment="""COMERCIAL ANALYST
BUSINESS CASE:
There is a supplier company(DELIVER ELETONIC S.A.).
The company has a customer portfolio and a sales team designed to atending the clients.
A produtc portfolio of this company is compound of many porducts classified by clusters and groups.

To create a database I gonna generate data based on dataset: https://www.kaggle.com/code/ayushmi77al/sales-data-analysis-of-electronic-store/input
"""


class create_database():
    # I propose to create the database to the business case
    # the target is tho show the data manipulation skills, knowledge of the business subject and SQL
    def __init__(self) -> None:
        self.import_tool()
        self.import_original_dataset()
        self.create_T_products()
        self.create_T_price()
        self.create_T_salesman()
        self.create_T_clients()
        self.crete_T_sales()
        self.check_tables()
        self.print_tables() #use to fix/save created tables

    def import_tool(self):
        import pandas
        self.pandas=pandas
        import random
        self.random=random

    def import_original_dataset(self):
        #import and prepare dataset
        self.original_base=self.pandas.read_csv('ORIGINAL_DATASET/Sales_April_2019.csv')  
        self.original_base=self.original_base[self.original_base['Product'].isna()==False]
        self.original_base=self.original_base[self.original_base['Quantity Ordered'].str.isnumeric()]
        self.original_base.reset_index(inplace=True,drop=True)
        #print(self.original_base.isna().sum()) #lookin for nan valuess
        
        #convert data
        i='Quantity Ordered'
        self.original_base[i]=self.original_base[i].map(lambda x:int(x))
        i='Price Each'
        self.original_base[i]=self.original_base[i].map(lambda x:float(x))

    def create_T_products(self):
        #create a table to reference to each product
        products=self.original_base.copy()
        products=products.groupby(['Product']).count()[[]]
        products.reset_index(inplace=True)
        
        def define_cluster(df,cluster,col_name,n_index='Product'):
            #classifying the products by names
            for i in cluster:
                for j in df[n_index]:
                    if j.find(i)!=-1:
                        df.loc[df[n_index]==j,col_name]=cluster[i]
            return df
        
        #Organize products in clusters
        cluster={
            'Monitor':'Monitor',
            'TV':'Monitor',
            'Batteries':'others',
            'Charging':'others',
            'Headphones':'Headphones',
            'Phone':'Phone',
            'Laptop':'Laptop',
            'LG':'home_appliances'
        }
        products=define_cluster(df=products,cluster=cluster,col_name='cluster',n_index='Product')

        #State the minimum order a client can make for SKU
        cluster={
            'Monitor':20,
            'others':100,
            'Headphones':100,
            'Phone':30,
            'Laptop':10,
            'home_appliances':15
        }
        products=define_cluster(df=products,cluster=cluster,col_name='min_order',n_index='cluster')

        #State a margin base to each product, this number will be used to construct price tables
        cluster={
            'Monitor':20,
            'others':10,
            'Headphones':10,
            'Phone':30,
            'Laptop':30,
            'home_appliances':20
        }
        products=define_cluster(df=products,cluster=cluster,col_name='base_margin',n_index='cluster')

        #create a SKU code based on the clusters
        cluster={
            'Monitor':99,
            'others':98,
            'Headphones':97,
            'Phone':96,
            'Laptop':95,
            'home_appliances':94
        }
        products=define_cluster(df=products,cluster=cluster,col_name='cod_prod',n_index='cluster')
        
        products['cod_prod']=products['cod_prod'].map(lambda x:str(int(x)))+products['Product'].index.map(lambda x:str(x).zfill(4))
        products.set_index('cod_prod',inplace=True)

        #define the cost of each product based on the original dataset
        #use the mean costume price and the base_margin I find out the product_cost
        price=self.original_base.copy()
        price=price.groupby(['Product']).sum(numeric_only=True)
        price['base_value']=price['Price Each']/price['Quantity Ordered']
        price.drop(columns=['Price Each','Quantity Ordered'],inplace=True)
        products=self.pandas.merge(left=products,right=price,left_on='Product',right_index=True,how='left')
        products['prod_cost']=products['base_value']/((products['base_margin']/100) +1)
        for i in ['base_value','prod_cost']:
            products[i]=products[i].map(lambda x:round(x,2))
        self.products=products.reset_index()

    def create_T_price(self):
        #create a table for sell products dependin on the client type and volume
        #we are creating six tables (1-6)
            # (1-3) clients of low potential
            # (4-6) high potential clients 
        tab_price=self.pandas.DataFrame()
        ref_tables={1:10, 2:7, 3:5, 4:2, 5:1, 6:-3}
        for i in ref_tables:
            table=self.products.copy()
            table['table']='tab_'+str(i)
            table['tab_factor']=ref_tables[i]+table['base_margin']
            tab_price=self.pandas.concat([tab_price,table])
        #organize table
        tab_price['tab_value']=tab_price['prod_cost']*((tab_price['tab_factor']/100)+1)
        tab_price['tab_value']=tab_price['tab_value'].map(lambda x:round(x,2))
        tab_price.drop(columns=['Product','cluster','min_order','base_margin','base_value','prod_cost'],inplace=True)
        tab_price.reset_index(inplace=True)
        tab_price['ID_tab_CodProd']=tab_price['table']+'-'+tab_price['cod_prod']
        self.tab_price=tab_price

    def create_T_salesman(self):
        #generate the salesman team based on the cities
        #we gonna have 2 supervisors
        #each supervisor take care of five salesman
        salesman=self.original_base.copy()
        salesman=salesman.groupby(['Purchase Address']).count()
        salesman.index=salesman.index.str.split(',')
        self.clients=salesman.copy()
        salesman['CITY']=salesman.index.str.get(1)
        salesman['STATE']=salesman.index.str.get(2).map(lambda x:x.replace(' ','')[:2])
        salesman=salesman.groupby(['CITY','STATE']).count()[[]].reset_index()
        salesman['id']=salesman['CITY']+'_'+salesman['STATE']
        x=101
        team=[]
        for i in salesman['id']:
            team.append(x)
            x=x+1
            if x==106:
                x=201
        salesman['cod_salesman']=team
        salesman['cod_supervisor']=salesman['cod_salesman'].map(lambda x:int(str(x)[0])*100)
        columns=['cod_salesman','cod_supervisor','STATE','CITY']
        salesman=salesman[columns]
        salesman.set_index('cod_salesman',inplace=True)
        #create names for them
        first_name=['Joe','Jack','Tom','Willian']
        last_name=['Smith','Jonson','Holmes','Drake']
        team=[]
        while len(team)<len(salesman):
            name=self.random.sample(first_name,1)[0]+' '+self.random.sample(last_name,1)[0]
            if name not in team:
                team.append(name)
        salesman['NAME']=team
        self.salesman=salesman

    def create_T_clients(self):
        #create clients, the adress will be based on the original dataset
        #I get the adress using random funcions
        #give to all salesman 10-15 customers
        self.clients['CITY']=self.clients.index.str.get(1)
        self.clients['ADRESS']=self.clients.index.str.get(0)
        columns=['CITY','ADRESS']
        clients=self.clients[columns].reset_index(drop=True)
        #get a random number of customers
        adress=[]
        for i in self.salesman['CITY']:
            cut=self.random.randint(10,15)
            st_list=list(clients.loc[clients['CITY']==i,'ADRESS'])
            st_list=st_list[:cut]
            for j in st_list:
                adress.append([i,j])
        #organize table, create a unique code to clients
        adress=self.pandas.DataFrame(adress,columns=['CITY','ADRESS']).set_index('CITY')
        clients=self.pandas.merge(left=self.salesman,right=adress,left_on='CITY',right_index=True,how='left')
        clients.drop(columns=['cod_supervisor','NAME'],inplace= True)
        clients.reset_index(inplace=True)
        clients['ID_client']=clients['cod_salesman'].map(lambda x:str(x).zfill(4))+'-'+clients.index.map(lambda x:str(x).zfill(4))
        clients.set_index('ID_client',inplace=True)
        #create random data to clients
        name=['Father And Sons','Technologic','Genius','Alpha','Beta','Digital','Essential','High Tech','Computer']
        organization=['S.A','Corporation','Company','Inc.','Electronics','Tech','Solutions','Techno','Store','World']
        clients['NAME']=''
        clients['TEL']=''
        name_cli=''
        tel_cli=''
        for i in clients.index:
            while name_cli in list(clients['NAME']) or name_cli=='':
                name_cli=self.random.sample(name,1)[0]+' '+self.random.sample(organization,1)[0]+' '+str(self.random.randint(0,99)).zfill(2)
            clients.loc[i,'NAME']=name_cli
            while tel_cli in list(clients['TEL']) or tel_cli=='':
                tel_cli=str(self.random.randint(9000,9999))+'-'+str(self.random.randint(0,9999)).zfill(4)
            clients.loc[i,'TEL']=tel_cli
        clients['EMAIL']=clients['NAME'].map(lambda x:x.replace(' ','')+'@email.com')
        #classify the clients by size (random)
        clients['REF_POTENTIAL']=clients.index.map(lambda x:self.random.random())
        clients.loc[:,'POTENTIAL']='D'
        clients.loc[clients['REF_POTENTIAL']>0.4,'POTENTIAL']='C'
        clients.loc[clients['REF_POTENTIAL']>0.6,'POTENTIAL']='B'
        clients.loc[clients['REF_POTENTIAL']>0.9,'POTENTIAL']='A'
        clients.drop(columns='REF_POTENTIAL',inplace=True)

        self.clients=clients

    def crete_T_sales(self):
        #create sales orders from a month
            #a month with 4 weeks
        #based on the clients table

        #create a random week_parameter for the order volume
        client_sale=self.clients.copy()[['POTENTIAL','cod_salesman']]
        w=['w1','w2','w3','w4','w5','w6','w7','w8','w9','w10','w11','w12']
        for i in w:
            client_sale[i]=client_sale.index.map(lambda x:self.random.random())
        salesman=self.salesman.copy()
        #create a random parameter for the salesman "quality"
        salesman['QUALITY']=salesman.index.map(lambda x:self.random.random())
        #using the salesman quality and the client week_parameter to generate order_quality
        client_sale=self.pandas.merge(left=client_sale,right=salesman[['QUALITY']],left_on='cod_salesman',right_index=True,how='left')
        week=self.pandas.DataFrame()
        for i in w:
            client_sale[i]=client_sale[i]*client_sale['QUALITY']
            x=client_sale.copy()
            x['week']=i
            x=x[[i,'week','POTENTIAL']].rename(columns={i:'order_quality'})
            week=self.pandas.concat([week,x])
        client_sale=week
        client_sale['w_cli']=client_sale['week']+'_'+client_sale.index
        client_sale.set_index('w_cli',inplace=True)
        #create a relation between the POTENTIAL and the number of SKUs 
        sku_pot={'A':[10,18],'B':[8,12],'C':[5,12],'D':[1,6]}
        order_itens=self.pandas.DataFrame()
        for i in client_sale.index:
            n_sku=self.random.randint(sku_pot[client_sale.loc[i,'POTENTIAL']][0],sku_pot[client_sale.loc[i,'POTENTIAL']][1])
            sku=self.random.sample(list(self.products.index),n_sku)
            products=self.products.loc[sku]
            products['w_cli']=i
            order_itens=self.pandas.concat([order_itens,products])
        order_itens.set_index('w_cli',inplace=True)
        client_sale=self.pandas.merge(left=client_sale,right=order_itens,left_index=True,right_index=True)
        #create a random volume 
        client_sale.reset_index(inplace=True)
        vol_pot={'A':[10,20],'B':[3,12],'C':[1,7],'D':[1,3]}
        for i in client_sale.index:
            potential=client_sale.loc[i,'POTENTIAL']
            vol=self.random.randint(vol_pot[potential][0],vol_pot[potential][1])
            client_sale.loc[i,'PACKS_QNT']=vol

        client_sale['PACKS_QNT']=client_sale['PACKS_QNT']*client_sale['order_quality']*10
        client_sale['PACKS_QNT']=client_sale['PACKS_QNT'].map(lambda x:int(x))
        client_sale['UNITS_QNT']=client_sale['PACKS_QNT']*client_sale['min_order']
        client_sale.drop(columns=['Product','cluster','base_margin','base_value','prod_cost','order_quality','min_order'],inplace=True)
        client_sale=client_sale[client_sale['PACKS_QNT']>0]
        #select the price table based on volume
            #C,D 0-7 tab1, 8-14 tab2, +14 tab3
            #A,B 0-7 tab4, 8-14 tab5, +14 tab6
        client_sale.loc[client_sale['POTENTIAL'].isin(['C','D']) & (client_sale['PACKS_QNT']>=0),'T_PRICE']='tab_1'
        client_sale.loc[client_sale['POTENTIAL'].isin(['C','D']) & (client_sale['PACKS_QNT']>=8),'T_PRICE']='tab_2'
        client_sale.loc[client_sale['POTENTIAL'].isin(['C','D']) & (client_sale['PACKS_QNT']>=15),'T_PRICE']='tab_3'
        client_sale.loc[client_sale['POTENTIAL'].isin(['A','B']) & (client_sale['PACKS_QNT']>=0),'T_PRICE']='tab_4'
        client_sale.loc[client_sale['POTENTIAL'].isin(['A','B']) & (client_sale['PACKS_QNT']>=8),'T_PRICE']='tab_5'
        client_sale.loc[client_sale['POTENTIAL'].isin(['A','B']) & (client_sale['PACKS_QNT']>=15),'T_PRICE']='tab_6'
        client_sale['ID_tab_CodProd']=client_sale['T_PRICE']+'-'+client_sale['cod_prod']
        client_sale=self.pandas.merge(left=client_sale,right=self.tab_price[['ID_tab_CodProd','tab_value']],left_on='ID_tab_CodProd',right_on='ID_tab_CodProd',how='left')
        client_sale['INVOICING']=client_sale['tab_value']*client_sale['UNITS_QNT']
        #organize columns
        client_sale['COD_CLI']=client_sale['w_cli'].str.split('_').map(lambda x:x[1])
        client_sale['NUM_ORDER']=client_sale.index.map(lambda x:'Y1-'+str(x+1).zfill(6))
        client_sale.drop(columns=['POTENTIAL','UNITS_QNT','ID_tab_CodProd','tab_value','w_cli'],inplace=True)
        self.sales_order=client_sale

    def check_tables(self):
        #remove extra columns
        self.products.drop(columns=['base_margin','base_value'],inplace=True)
        self.tab_price.drop(columns=['index','tab_factor'],inplace=True)
        self.salesman.reset_index(inplace=True)
        self.clients.reset_index(inplace=True)

    def print_tables(self):
        #save tables
        path='NEW_DATASET/'
        name='A1_products.csv'
        self.products.to_csv(path+name,sep=',',index=False)
        name='A2_tab_price.csv'
        self.tab_price.to_csv(path+name,sep=',',index=False)
        name='A3_salesman.csv'
        self.salesman.to_csv(path+name,sep=',',index=False)
        name='A4_clients.csv'
        self.clients.to_csv(path+name,sep=',',index=False)
        name='A5_sales_order.csv'
        self.sales_order.to_csv(path+name,sep=',',index=False)

create_database()