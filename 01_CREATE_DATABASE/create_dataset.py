def create_data_set():
    from B01_C_TABLE_PRODUCTS  import table_products
    table_products()

    from B02_C_TABLE_PRICE import  table_price
    table_price()

    from B03_C_TABLE_CLIENTS import table_clients
    table_clients()

    from B04_C_TABLE_SALESMAN import table_salesman
    table_salesman()

    from B05_C_TABLE_ORDERS_MAIN import table_order_main
    table_order_main()

create_data_set()