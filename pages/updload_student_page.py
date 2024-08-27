import os
import streamlit as st
import mysql.connector
from mysql.connector import Error

st.title("Crate student")
code = st.text_input(label="Student code")
full_name = st.text_input(label='Student name')
emails = st.text_input(label='Email address')
course_id = st.text_input(label="Course id")
submit = st.button("Submit")

if submit:
    st.write(f"Student name is: {full_name}")
    st.write(f"database name: {os.getenv("DB_NAME")}")
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
            INSERT INTO students (code, full_name, emails, course_id)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                code,
                full_name,
                emails,
                course_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()

            st.write("The student has been successfully saved")

    except Error as e:
        st.error("Error connecting to database")
        connection = None