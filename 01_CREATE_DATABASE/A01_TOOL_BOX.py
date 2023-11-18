class tool_box():
    def __init__(self) -> None:
        self.import_tool()
        self.import_data()
        pass
    def import_tool(self):
        import pandas
        self.pandas=pandas
    def import_data(self):
        self.data=self.pandas.read_csv('/ORIGINAL_DATASET/Sales_April_2019.csv',sep=';')
        print(self.data)