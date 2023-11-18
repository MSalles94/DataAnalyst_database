01_CREATING_DATABASE

DATA SOURCE:
The original dataset is from the follow link: https://www.kaggle.com/code/ayushmi77al/sales-data-analysis-of-electronic-store/input
From this dataset I created another one more complex.

GENERAL VIEW
I want to create a business case using the original dataset. This first step of portfolio I wanna show my skills manipulating and cleaning data.
Basically I use two libraries here: pandas and random.
Pandas is used to create the DataFrame object to manipulate tables.
Random is mostly used to increace the dataset complexity.
Starting from the original dataset I create five tables that gonna be used to feed the database.

TABLES
At this step the data are stored in .csv.
In the future the idea is to simulate a ERP sistem (Enterprise Resource Planning) tho show some SQL skills.
As a database I split the data in several tables, this technique is used to spare space in a database.
I'm not a DataBaseAdministrator so I just made it simple. There are ways to improve the data storagment but this is not my goal here.
Also there are ways to imporve the business case complexity (as using days or the day the salesman can visit the client) but I guess its good for now.

A1_products - register of every product (cost, name, code, minimum order)
A2_tab_price - register of the possible prices (table reference, price) 
A3_salesman - register of every salesman (code, name, supervisor)
A4_clients  - register of clients (code, adress, cluster)
A5_sales_order - register of the sales order made in four months ( client, order number, quantity, invoicing, week)



