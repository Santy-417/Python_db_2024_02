import streamlit as st
import pandas as pd
from merged_data import insert_merged_data_in_bulk

def _extract_data_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file)
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None

st.title("Upload and Merge Excel Files")

uploaded_files = st.file_uploader("Upload Excel files", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files were uploaded successfully.")
    
    if len(uploaded_files) == 2:
        if uploaded_files[0].name == uploaded_files[1].name:
            st.error("Error: Both files are the same. Please upload two different files.")
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
                    
                    st.success("Merged DataFrame")
                    st.write(merged_df)

                    order_id = 1  
                    insert_merged_data_in_bulk(merged_df, order_id)

                    st.success("Data inserted into the database successfully.")
            else:
                st.error("Error: One or both files could not be read.")
    else:
        st.info("Please upload exactly 2 files to be able to merge the files.")
