import scripts
import streamlit as st
import pandas
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PanTool, ZoomInTool, ZoomOutTool, WheelZoomTool, ResetTool, SaveTool
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap
from typing import Optional

sector_list = ['TECHNOLOGY', 'CONSUMER PRODUCTS & SERVICES', 'PLANTATION',
    'EXCHANGE TRADED FUND-BOND', 'INDUSTRIAL PRODUCTS & SERVICES',
    'FINANCIAL SERVICES', 'PROPERTY', 'CONSTRUCTION', 'HEALTH CARE',
    '', 'TRANSPORTATION & LOGISTICS', 'ENERGY',
    'REAL ESTATE INVESTMENT TRUSTS', 'TELECOMMUNICATIONS & MEDIA', 'UTILITIES']

def normalize_data(df: pandas.DataFrame, x:str, y:str):
  x = df[x]; y = df[y]
  df = df[x.between(x.quantile(0.05), x.quantile(0.95)) & y.between(y.quantile(0.05), y.quantile(0.95))]
  return df

def filter_value(df: pandas.DataFrame, column: str, unique_val_in_col: list):
  return df[df[column].isin(unique_val_in_col)]

def plot_fig(df:pandas.DataFrame, x:str, y:str, legend:str, x_label: str, y_label: str, normalized: bool=False, filter_category: Optional[list[str]]=None):
  fig = figure(height=600,width=1000,tools="hover",  toolbar_location="above", 
              x_axis_label=x, y_axis_label=y,
              tooltips=[("STOCK","@STOCK_SYMBOL"),("SUBSECTOR", "@SUBSECTOR"), ("SECTOR", "@SECTOR"),
                        (f"{y_label}", f"@{y}"),  
                        (f"{x_label}", f"@{x}")])
  fig.add_tools(PanTool(), ZoomInTool(), ZoomOutTool(), WheelZoomTool(), ResetTool(), SaveTool())

  adjusted_df = df.copy(deep=True).dropna()
  
  if filter_category:
    adjusted_df = filter_value(adjusted_df, legend, filter_category)
  if normalized:
    adjusted_df = normalize_data(adjusted_df,x=x,y=y)
  source = ColumnDataSource(data=adjusted_df)

  fig.scatter(source=source, y=y, x=x, legend_field=legend, 
              fill_color=factor_cmap(legend, Category20c[20], factors=adjusted_df[legend].unique()),
              line_color=None, size=10)

  fig.add_layout(fig.legend[0], 'right')
  return fig


def display_chart(bursa_companies_csv:str, sector_overview_csv:str, subsector_overview_csv:str, period:int, csvdir: scripts.process_csv.csvDirectory):
    bursa_companies_df = pandas.read_csv(bursa_companies_csv)
    sector_overview_df = pandas.read_csv(sector_overview_csv)
    subsector_overview_df = pandas.read_csv(subsector_overview_csv)
    
    sector_multiselect = st.multiselect(label="Sectors",
                                        options= [el for el in bursa_companies_df["SECTOR"].dropna().unique() if el in sector_list], 
                                        default=[el for el in bursa_companies_df["SECTOR"].dropna().unique() if el in sector_list])
    normalized = st.checkbox(value=True, label="Remove Outliers")

    # Plot Excess Returns vs Standard Deviation
    st.markdown("## Bursa Companies - Excess Returns vs Standard Deviation")  
    st.bokeh_chart(plot_fig(df=bursa_companies_df, normalized=normalized, legend="SECTOR",
                x = f"annualized_standard_deviation_of_equity_{int(period)}Y",
                y=f"annualized_excess_return_of_equity_{int(period)}Y", 
                filter_category=sector_multiselect, x_label="Standard Deviation", 
                y_label= "Excess Return"
                ))
    
    # Plot Excess Returns vs Beta
    st.markdown("## Bursa Companies - Excess Returns vs Beta")
    st.bokeh_chart(plot_fig(df=bursa_companies_df, normalized=normalized, legend="SECTOR",
                x = f"BETA_{int(period)}Y",
                y=f"annualized_excess_return_of_equity_{int(period)}Y", 
                filter_category=sector_multiselect, x_label="Beta", 
                y_label= "Excess Return"
                ))
    
    st.markdown("## Bursa Companies - Excess Returns vs Skewness")
    st.bokeh_chart(plot_fig(df=bursa_companies_df, normalized=normalized, legend="SECTOR",
                x = f"SKEWNESS_{int(period)}Y",
                y=f"annualized_excess_return_of_equity_{int(period)}Y", 
                filter_category=sector_multiselect, x_label="SKEWNESS", 
                y_label= "Excess Return"
                ))

    st.markdown("## Bursa Companies - Excess Returns vs Kurtosis")
    st.bokeh_chart(plot_fig(df=bursa_companies_df, normalized=normalized, legend="SECTOR",
                x = f"FISHER_KURTOSIS_{int(period)}Y",
                y=f"annualized_excess_return_of_equity_{int(period)}Y", 
                filter_category=sector_multiselect, x_label="FISHER_KURTOSIS", 
                y_label= "Excess Return"
                ))