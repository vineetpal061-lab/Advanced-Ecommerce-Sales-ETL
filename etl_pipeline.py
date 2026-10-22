import pandas as pd
import sqlite3

INPUT = "data/raw_sales.csv"
DB = "sales.db"

# Extract
df = pd.read_csv(INPUT)

# Transform
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

df = df.dropna(subset=["order_id", "order_date", "product", "quantity", "unit_price"])
df = df[df["quantity"] > 0]
df["total_amount"] = df["quantity"] * df["unit_price"]

# Load
conn = sqlite3.connect(DB)
df.to_sql("sales", conn, if_exists="replace", index=False)

# A few SQL analysis queries
queries = {
    "total_revenue": "SELECT SUM(total_amount) AS revenue FROM sales;",
    "top_products": '''
        SELECT product, SUM(total_amount) AS revenue
        FROM sales
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 5;
    ''',
    "city_sales": '''
        SELECT customer_city, SUM(total_amount) AS revenue
        FROM sales
        GROUP BY customer_city
        ORDER BY revenue DESC;
    '''
}

for name, query in queries.items():
    print(f"\n{name.upper()}")
    print(pd.read_sql_query(query, conn))

conn.close()
print("\nETL pipeline completed successfully.")
