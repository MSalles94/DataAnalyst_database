class tool_box():
    def __init__(self) -> None:
        self.import_tool()
        self.import_data()
        pass
    def import_tool(self):
        import pandas
        self.pandas=pandas
    def import_data(self):
        #import original data
        self.data=self.pandas.read_csv(filepath_or_buffer='ORIGINAL_DATASET/Sales_April_2019.csv')
        #clean data
        self.data=self.data[self.data['Product'].isna()==False]
        self.data=self.data[self.data['Product']!='Product']
        self.data.reset_index(inplace=True,drop=True)