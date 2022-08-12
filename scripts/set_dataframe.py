import pandas
import streamlit as st
import sys, os

def create_dataframe(df: pandas, heading: str, file_name:str):
    with st.container():
        col1, col2 = st.columns([2,1])
        col1.markdown(f"## {heading}")
        col2.download_button(label="Download full data", data = df.to_csv().encode("utf-8"),file_name=f"{file_name}.csv")
        st.dataframe(df)
        st.markdown("---")

def display_data():
    try: 
        df_bursa_companies = pandas.read_csv("./data/bursa_companies.csv")
        df_sector_overview = pandas.read_csv("./data/sector_overview.csv")
        df_subsector_overview = pandas.read_csv("./data/subsector_overview.csv")

        create_dataframe(df=df_bursa_companies.iloc[:,1:], heading="Bursa Companies",file_name="bursa_companies")
        create_dataframe(df=df_sector_overview, heading="Sector Overview", file_name="sector_overview")
        create_dataframe(df=df_subsector_overview, heading="Sub-sector Overview", file_name="subsector_overview")
        
    except FileNotFoundError:
        pass

