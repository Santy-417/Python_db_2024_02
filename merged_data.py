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

            # Prepare the insert query
            insert_query = f"""
            INSERT INTO {table_name} (OrderID, ProductID, OrderDate, Quantity, CustomerName, DeliveryAddress, ProductName, Category, Price, Size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Convert DataFrame to list of tuples with the correct order
            merged_data = df[['OrderID', 'ProductID', 'OrderDate', 'Quantity', 'CustomerName', 'DeliveryAddress', 'ProductName', 'Category', 'Price', 'Size']].to_records(index=False).tolist()


            # Execute the insert query in bulk
            cursor.executemany(insert_query, merged_data)
            
            # Commit the transaction
            connection.commit()

            st.write(f"{cursor.rowcount} rows inserted successfully.")

    except mysql.connector.Error as e:
        st.write(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
