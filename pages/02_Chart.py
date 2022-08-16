import sidebar
import streamlit as st
import matplotlib.pyplot as plt
from scripts.plot_chart import plot_fig
import pandas
import os
import scripts


data_dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

st.markdown("# Bursa Stock Scraper")
st.markdown("See notebook project [here](https://github.com/tys203831/bursa-scraper/blob/main/notebook/Bursa_scraper.ipynb)")

form = st.sidebar.form("input form")
rf,period,interval,confidence_level,include_dividends,exclude_warrant,skipna,submitted,updated = sidebar.sidebar(form)

try:
    csvdir = scripts.process_csv.csvDirectory(rf=rf, period=period,interval=interval, 
                                confidence_level=confidence_level, 
                                exclude_warrant=exclude_warrant)
    
    if updated:
        csvdir = scripts.process_csv.csvDirectory(rf=rf, period=period,interval=interval, 
                                confidence_level=confidence_level, 
                                exclude_warrant=exclude_warrant)
        scripts.refresh_data.refreshData(csvdir, rf=rf, period=period,interval=interval, 
                confidence_level=confidence_level, exclude_warrant=exclude_warrant)

    if submitted:
        csvdir = scripts.process_csv.csvDirectory(rf=rf, period=period,interval=interval, 
                                        confidence_level=confidence_level, 
                                        exclude_warrant=exclude_warrant)
        last_updated = scripts.set_dataframe.check_update(csvdir, rf=rf, period=period,interval=interval, 
                                            confidence_level=confidence_level, 
                                            exclude_warrant=exclude_warrant)
        scripts.plot_chart.display_chart(csvdir.bursa_companies_csv, csvdir.sector_overview_csv, csvdir.subsector_overview_csv, 
                                         period=period, csvdir=csvdir)

    if not submitted:
        last_updated = scripts.set_dataframe.check_update(csvdir, rf=rf, period=period,interval=interval, 
                                            confidence_level=confidence_level, 
                                            exclude_warrant=exclude_warrant)
        scripts.plot_chart.display_chart(csvdir.bursa_companies_csv, csvdir.sector_overview_csv, 
                                         csvdir.subsector_overview_csv, period=period, csvdir=csvdir)

except FileNotFoundError:
    st.warning("Please click the UPDATE button to update the data yourself.")
    
except KeyError as error:
    st.warning("Please click the UPDATE button to update the data yourself.")
    st.warning("Table element not found: " + str(error))