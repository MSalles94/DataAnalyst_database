class table_clients():

    def __init__(self) -> None:
        self.prepare()
        self.get_clients_adress()
        self.generate_information()
        self.client_cluster()
        self.salesman_code()
        self.visit_date()
        self.print_to_csv()
    

    def prepare(self):
        from A01_TOOL_BOX import tool_box
        tool_box=tool_box()

        self.pandas=tool_box.pandas
        self.random=tool_box.random
        self.clients=tool_box.data
        self.datetime=tool_box.datetime
        

    def get_clients_adress(self):
        #use the original data set to get some address
        self.clients=self.clients[['Purchase Address']]
        #remove duplicates
        self.clients=self.clients.groupby(['Purchase Address']).count().reset_index() 
        #organize the address information in columns
        self.clients['Purchase Address']=self.clients['Purchase Address'].map(lambda x:x.split(','))
        self.clients['street']=self.clients['Purchase Address'].str.get(0).map(lambda x:x.strip().split(' ')[1:3])
        self.clients['street']=self.clients['street'].map(lambda x:x[0]+' '+x[1])
        self.clients['No']=self.clients['Purchase Address'].str.get(0).map(lambda x:x.strip().split(' ')[0])
        self.clients['city']=self.clients['Purchase Address'].str.get(1)
        self.clients['state']=self.clients['Purchase Address'].str.get(2).map(lambda x:x.strip().split(' ')[0])
        self.clients['zipcode']=self.clients['Purchase Address'].str.get(2).map(lambda x:x.strip().split(' ')[1])
        #remove the original column
        self.clients.drop(columns='Purchase Address',inplace=True)
        #chose a range of clients for each city, random chose
        range_cli_salesman=[25,100]
        t_clients_city=[]
        for i in self.clients['city'].unique():
            sample=list(self.clients[self.clients['city']==i].index)
            sample=self.random.sample(sample,
                                      self.random.randint(range_cli_salesman[0],
                                                                 range_cli_salesman[1]))
            sample=self.clients[self.clients.index.isin(sample)].reset_index(drop=True)
            sample['ID_client']=sample['zipcode']+sample.index.map(lambda x:'-'+str(x+1).zfill(3))
            t_clients_city.append(sample)

        self.clients=self.pandas.concat(t_clients_city).reset_index(drop=True)

    def generate_information(self):
        #create random names to each client
        name=['Father And Sons','Technologic','Genius','Alpha','Beta',
              'Digital','Essential','High Tech','Computer']
        organization=['S.A','Corporation','Company','Inc.','Electronics',
                      'Tech','Solutions','Techno','Store','World']
        cli_name=[]
        while len(cli_name)<len(self.clients):
            new_name=self.random.sample(name,1)[0]+' '+self.random.sample(organization,1)[0]+' '+str(self.random.randint(0,100)).zfill(3)
            if new_name not in cli_name:
                cli_name.append(new_name)
        self.clients['name']=cli_name
        #create random phone numbers
        self.clients['phone']='+001 '+self.clients['zipcode'].map(lambda x:x[0:3])+' '+self.clients.index.map(lambda x: str(self.random.randint(100,999)))+self.clients.index.map(lambda x: '-'+str(self.random.randint(1000,9999)))

        #create email, based on names
        self.clients['email']=self.clients['name'].map(lambda x:x.replace(' ','_')+['@gmail.com.br' if self.random.randint(0,3)>2 else '@outlook.com'][0] )
        #register date
        def random_date():
            dt_i=self.datetime.date(year=2000,month=1,day=1)
            dt_f=self.datetime.date(year=2020,month=12,day=31)
            return dt_i+(dt_f-dt_i)*self.random.random()
        self.clients['register_date']=self.clients.index.map(lambda x: random_date())

    def client_cluster(self):
        #create a cluster to classify the clients as the potential sales volume
        def sales_volume_potential():
            cluster=['A']*5+['B']*15+['C']*30+['D']*50
            return self.random.sample(cluster,1)[0]
        self.clients['cluster']=self.clients.index.map(lambda x:sales_volume_potential())  

    def salesman_code(self):
        #each city is a sector, each sector is atended by a salesman
        self.clients['ID_sector']=0
        a=0
        for i in self.clients['zipcode'].unique():
            a+=1
            self.clients.loc[self.clients['zipcode']==i,'ID_sector']=a
        self.clients['ID_sector']=self.clients['ID_sector'].map(lambda x:100+x if x>5 else 200+x)

    def visit_date(self):
        #insert the date clients are visited by salesman
        # the number indicates the weekday (1 = monday, ... 7=sunday)
        for i in self.clients['ID_sector'].unique():
            day_week=1
            for j in self.clients.loc[self.clients['ID_sector']==i,'ID_client'].unique():
                self.clients.loc[self.clients['ID_client']==j,'visit_day']=day_week%7 if day_week%7 else 7 
                day_week=day_week+1

    def print_to_csv(self):
        #organize columns
        columns=['ID_client','name','cluster','ID_sector','phone',
                 'email','register_date','zipcode','state','city','No','street','visit_day']
        self.clients=self.clients[columns]   

        self.clients.to_csv('NEW_DATASET/A03_TAB_CLIENTS.csv',decimal=',',sep=';',index=False)  

