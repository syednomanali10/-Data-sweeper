#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO


#set up our app
st.set_page_config(page_title="💿 Data sweeper", layout="wide")
st.title("💿 Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsuported file type: {file_ext}")
            continue


        #display info about tha file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")


        #show 5 rows of our data frame(df)
        st.write("🔍Preview the head of the data frame")
        st.dataframe(df.head())

        #options for data cleaning
        st.subheader("🛠 Data cleaning options")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Dupliacates removed!")
                
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")


        #choose specific columns to keep or convert
        st.subheader("🎯Select columns or Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #create some visualization
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])


        #Convert the file -> CSV to Excel
        st.subheader("🔄Conversion options")
        conversion_types = st.radio(f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_types == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                
            if conversion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #download
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_types}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            )

st.success("🎉 All files processed!")