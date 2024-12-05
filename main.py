import os
import pandas as pd
from setup_kaggle import *
from dotenv import load_dotenv

df = pd.read_csv('orders.csv', na_values=['Not Available', 'unknown'])

# print(df.head())
# print(df.columns)

df['Order Date'] = pd.to_datetime(df['Order Date'])
print(df.dtypes)
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')    
# print(df.columns)

df['discount_price'] = df['list_price'] * df['discount_percent']*0.01    
print(df['discount_price'])

df['sales_price'] = df['list_price'] - df['discount_price']
df['profit'] = df['sales_price'] - df['cost_price']

df = df.drop(columns = ['list_price', 'discount_percent', 'cost_price'])  

print(df.head())

from sqlalchemy import create_engine, text

load_dotenv()

username = os.getenv('MYSQL_USERNAME')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
database = os.getenv('MYSQL_DATABASE')

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

# Create the engine and connect
engine = create_engine(connection_string)
conn = engine.connect()

# df.to_sql('df_orders', con=conn, index =False, if_exists='append')

# find top 10 highest revenue generating products
query_1 = "SELECT * FROM df_orders ORDER BY sales_price DESC LIMIT 5;" 
# res_1 = conn.execute(text(query_1))

# for row in res_1:
#     print(row)

# find top 5 highest selling products in each region 
query_2 = """
        WITH ranked_df AS(
            SELECT region, sales_price, RANK() OVER(PARTITION BY region ORDER BY sales_price DESC) AS `rank`
            FROM df_orders
        )
        
        SELECT region,sales_price
        FROM ranked_df
        WHERE `rank`<=5;
"""
# res_2=conn.execute(query_2)
# for row in res_2:
#     print(row)

query_3= """
        SELECT region,sales_price
        FROM df_orders AS d1
        WHERE (SELECT COUNT(*)
               FROM df_orders as d2
               WHERE d2.region = d1.region AND d2.sales_price>d1.sales_price)
               <5
        ORDER BY region, sales_price DESC;
"""
# res_3 = conn.execute(query_3)
# for row in res_3:
#     print(row)
 
 # Sales on same month of two years   
query_4= """
        SELECT month(d1.order_date) AS MONTH,year(d1.order_date) AS YEAR1, year(d2.order_date) AS YEAR2,SUM(d1.sales_price),SUM(d2.sales_price)
        FROM df_orders AS d1
        JOIN df_orders AS d2
        ON month(d2.order_date) = month(d1.order_date)  
        WHERE year(d1.order_date) != year(d2.order_date) AND year(d1.order_date) < year(d2.order_date)
        GROUP BY month(d1.order_date) ,year(d1.order_date),year(d2.order_date)
        ORDER BY MONTH,YEAR1,YEAR2
"""
res_4 = conn.execute(query_4)
for row in res_4:
    print(row)
    
