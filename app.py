import streamlit as st
import pandas as pd
from student_db_helper import insert_students_in_bulk



def _extract_data_from_excel(excel_file):
    """Extracts data from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
        return df
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return None

st.title("Upload and Merge Excel Files")

uploaded_files = st.file_uploader("Upload Excel files", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"{len(uploaded_files)} files were uploaded successfully.")
    
    if len(uploaded_files) == 2:
        # Verifica si los dos archivos son iguales comparando sus nombres
        if uploaded_files[0].name == uploaded_files[1].name:
            st.write("Error: Both files are the same. Please upload two different files.")
        else:
            df1 = _extract_data_from_excel(uploaded_files[0])
            df2 = _extract_data_from_excel(uploaded_files[1]) 
            
            if df1 is not None and df2 is not None:
                st.write("DataFrame file 1:")
                st.write(df1)
                
                st.write("DataFrame file 2:")
                st.write(df2)

                if st.button("Merge DataFrames"):
                    merged_df = pd.merge(df1, df2, on='ProductID', how='inner')
                    
                    st.write("Merged DataFrame")
                    st.write(merged_df)
            else:
                st.write("Error: One or both files could not be read.")
    else:
        st.write("Please upload exactly 2 files to be able to merge the files.")
