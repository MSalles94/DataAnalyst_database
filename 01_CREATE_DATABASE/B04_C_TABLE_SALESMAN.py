class table_salesman():

    def __init__(self) -> None:
        self.prepare()
        self.salesman_info()
        self.print_to_csv()
        
    def prepare(self):
        from A01_TOOL_BOX import tool_box
        tool_box=tool_box()

        self.pandas=tool_box.pandas
        self.random=tool_box.random

        self.salesman=self.pandas.read_csv('NEW_DATASET/A03_TAB_CLIENTS.csv',sep=';',decimal=',')
    
    def salesman_info(self):
        #get the ID_sector from clients
        self.salesman=self.salesman.groupby(['ID_sector']).count()[[]].reset_index()

        #generate names
        first_name=['Jonh','Paul','Jack','Bob','Jonny','James','Ben','Max']
        last_name=['Lee','Adams','Smith','Silva','Stark','Baume','MacArthur']
        self.salesman['Name']=self.salesman.index.map(lambda x:self.random.sample(first_name,1)[0]+' '+self.random.sample(last_name,1)[0])

        #separate the salesman by supervision
        self.salesman['supervisor']=self.salesman['ID_sector'].map(lambda x : int(str(x)[0])*100)
    
    def print_to_csv(self):
        self.salesman.to_csv('NEW_DATASET/A04_TAB_SALESMAN.csv',sep=';',decimal=',',index=False)
    
        
