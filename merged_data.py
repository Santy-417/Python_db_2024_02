import mysql.connector
import os
import streamlit as st

def insert_merged_data_in_bulk(df, order_id, table_name='merged_data'):
    connection = None
    cursor = None

    try:
        df['order_id'] = order_id

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            st.write("Connected to the database successfully.")
            cursor = connection.cursor()

            insert_query = f"""
            INSERT INTO {table_name} (OrderID, ProductID, OrderDate, Quantity, CustomerName, DeliveryAddress, ProductName, Category, Price, Size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            merged_data = df[['OrderID', 'ProductID', 'OrderDate', 'Quantity', 'CustomerName', 'DeliveryAddress', 'ProductName', 'Category', 'Price', 'Size']].to_records(index=False).tolist()

            cursor.executemany(insert_query, merged_data)
            
            connection.commit()

            st.write(f"{cursor.rowcount} rows inserted successfully.")

    except mysql.connector.Error as e:
        st.write(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
