import csv
import sidebar
import streamlit as st
import matplotlib.pyplot as plt
from scripts.plot_chart import plot_fig
import pandas
import os
import scripts


data_dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

form = st.sidebar.form("input form")
rf,period,interval,confidence_level,include_dividends,exclude_warrant,skipna,submitted,updated = sidebar.sidebar(form)

try:
    csvdir = scripts.process_csv.csvDirectory()
    bursa_companies_csv = csvdir.bursa_companies_csv
    sector_overview_csv = csvdir.sector_overview_csv
    subsector_overview_csv = csvdir.subsector_overview_csv
    
    
    if updated:
        scripts.refresh_data.refreshData(csvdir, rf=rf, period=period,interval=interval, 
                confidence_level=confidence_level, exclude_warrant=exclude_warrant)

    if submitted:
        csvdir = scripts.process_csv.csvDirectory(rf=rf, period=period,interval=interval, 
                                        confidence_level=confidence_level, 
                                        exclude_warrant=exclude_warrant)
        scripts.plot_chart.display_chart(bursa_companies_csv, sector_overview_csv, subsector_overview_csv, 
                                         period=period, csvdir=csvdir)

    if not submitted:
        scripts.plot_chart.display_chart(bursa_companies_csv, sector_overview_csv, 
                                         subsector_overview_csv, period=period, csvdir=csvdir)

except FileNotFoundError:
    st.markdown("# Bursa Stock Scraper")
    st.markdown("See original project [here](https://colab.research.google.com/gist/tys203831/75c60c26862d53adafe01b7ddd7fda3b/bursa-scraper.ipynb)")
    last_updated = scripts.set_dataframe.check_update(csvdir)
    st.warning("Please click the UPDATE button to update the data yourself.")
