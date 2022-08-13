import pandas
import streamlit as st
import sys, os
from scripts import process_csv
import datetime
from typing import Union

def check_update(csvdir: process_csv.csvDirectory) -> st.write:
  try:
    _ , col2 = st.columns([3,2])
   
    last_updated: str = datetime.datetime.fromtimestamp(os.path.getmtime(csvdir.subsector_overview_csv)).strftime("%d-%m-%Y %H:%M")
    col2.write(f"Last Updated at {last_updated}")
  except FileNotFoundError:
    col2.write("Haven't Updated yet.")
    return col2

def create_dataframe(df: pandas, heading: str, file_name:str, key:Union[str,int]):
    with st.container():
        col1, col2 = st.columns([2,1])
        col1.markdown(f"## {heading}")
        col2.download_button(label="Download", key= key, data = df.to_csv().encode("utf-8"),file_name=f"{file_name}.csv")
        st.dataframe(df)
        st.markdown("---")

def display_data(csvdir: process_csv.csvDirectory):
    try: 
        df_bursa_companies = pandas.read_csv(csvdir.bursa_companies_csv)
        df_sector_overview = pandas.read_csv(csvdir.sector_overview_csv)
        df_subsector_overview = pandas.read_csv(csvdir.subsector_overview_csv)

        create_dataframe(df=df_bursa_companies.iloc[:,1:], heading="Bursa Companies",file_name="bursa_companies", key="bursa_companies")
        create_dataframe(df=df_subsector_overview, heading="Sub-sector Overview", file_name="subsector_overview", key="subsector_overview")
        create_dataframe(df=df_sector_overview, heading="Sector Overview", file_name="sector_overview",key="sector_overview")
        
    except FileNotFoundError:
        st.warning("Please click the UPDATE button to update the data yourself.")