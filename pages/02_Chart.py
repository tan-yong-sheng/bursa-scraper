import sidebar
import streamlit as st
import matplotlib.pyplot as plt
from scripts.plot_chart import plot_fig
import pandas
import os
import scripts
import streamlit.components.v1 as components

def display_chart(bursa_companies_csv:str, sector_overview_csv:str, subsector_overview_csv:str, rf:float):
    bursa_companies_df = pandas.read_csv(bursa_companies_csv)
    sector_overview_df = pandas.read_csv(sector_overview_csv)
    subsector_overview_df = pandas.read_csv(subsector_overview_csv)

    st.markdown("# Bursa Stock Scraper")
    st.markdown("See original project [here](https://colab.research.google.com/gist/tys203831/75c60c26862d53adafe01b7ddd7fda3b/bursa-scraper.ipynb)")
    last_updated = scripts.set_dataframe.check_update(csvdir)
    st.markdown("## Bursa Companies - Excess Returns vs Standara Deviation")
    plot_fig(df=bursa_companies_df, normalize=True, legend="SECTOR", 
                       x=f"annualized_standard_deviation_of_equity_{int(period)}Y",
                       y=f"annualized_excess_return_of_equity_{int(period)}Y")
    
    st.markdown("## Bursa Companies - Excess Returns vs Beta")
    plot_fig(df=bursa_companies_df, normalize=True, legend="SECTOR", 
                       x=f"BETA_{int(period)}Y",
                       y=f"annualized_excess_return_of_equity_{int(period)}Y")

    #st.markdown("## Subsector Overview")
    #st.pyplot(plot_fig(df=subsector_overview_df, period=period, normalize=False, legend="SECTOR"))

    #st.markdown("## Sector Overview")
    #st.pyplot(plot_fig(df=sector_overview_df, period=period, normalize=False, legend="SECTOR"))


data_dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

form = st.sidebar.form("input form")
rf,period,interval,confidence_level,include_dividends,exclude_warrant,skipna,submitted,updated = sidebar.sidebar(form)

try: 
    bursa_companies_csv = os.path.join(data_dirname, f"bursa_companies_p{int(period)}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv")
    sector_overview_csv = os.path.join(data_dirname, f"sector_overview_p{int(period)}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv")
    subsector_overview_csv = os.path.join(data_dirname, f"subsector_overview_p{int(period)}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv")
    csvdir = scripts.process_csv.csvDirectory()
    
    if updated:
        scripts.refresh_data.refreshData(csvdir, rf=rf, period=period,interval=interval, 
                confidence_level=confidence_level, exclude_warrant=exclude_warrant)

    if submitted:
        csvdir = scripts.process_csv.csvDirectory(rf=rf, period=period,interval=interval, 
                                        confidence_level=confidence_level, 
                                        exclude_warrant=exclude_warrant)
        display_chart(bursa_companies_csv, sector_overview_csv, subsector_overview_csv, rf=rf)

    if not submitted:
        display_chart(bursa_companies_csv, sector_overview_csv, subsector_overview_csv, rf=rf)

except FileNotFoundError:
    st.markdown("# Bursa Stock Scraper")
    st.markdown("See original project [here](https://colab.research.google.com/gist/tys203831/75c60c26862d53adafe01b7ddd7fda3b/bursa-scraper.ipynb)")
    last_updated = scripts.set_dataframe.check_update(csvdir)
    st.warning("Please click the UPDATE button to update the data yourself.")
