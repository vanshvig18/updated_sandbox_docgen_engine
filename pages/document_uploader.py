import streamlit as st
import pandas as pd

def load_file(file):
    if file.type == "text/csv":
        return pd.read_csv(file)
    elif file.type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        return pd.read_excel(file)
    elif file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    else:
        return None

st.title("Document Uploader")

uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True, type=['txt','csv','xlsx'])

if uploaded_files:
    extracted_data = {}
    for file in uploaded_files:
        data = load_file(file)
        extracted_data[file.name] = data

    st.session_state['uploaded_data'] = extracted_data

    st.success("Files uploaded and data extracted successfully!")

    st.write("### Preview of uploaded data:")
    for filename, data in extracted_data.items():
        st.write(f"**{filename}**")
        if isinstance(data, pd.DataFrame):
            st.dataframe(data.head())
        else:
            st.text(data[:500])
