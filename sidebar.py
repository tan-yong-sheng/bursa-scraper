import streamlit as st

def sidebar(form: st.form):  
  interval_dict = dict(zip(["1 day","1 week","1 month","3 month"], ["1d","1wk","1mo","3mo"]))
  
  rf: float = form.number_input(value=4.00, step=0.01 ,label="Risk free rate (%): ", key="risk free rate")/100 # 0.04 # risk free rate
  period: int = form.number_input(value = 5, min_value=1, max_value=10, label="Valid period: 1-10 Year", key="period") # 5 # e.g. 5 = 5 years
  #
  interval: str = form.selectbox(options = ["1 day","1 week","1 month","3 month"],index=1, label="Valid interval: 1 day,1 week,1 month, 3month", key="interval") #"1wk"
  confidence_level: float = form.selectbox(options=[10.0, 5.0, 1.0], index=1, label="Confidence level of linear regression (%): ", key="confidence_level")/100
  include_dividends: bool = False #: bool = st.checkbox(value=False, label="Whether to consider dividend into stock returns when calculating beta?")
  exclude_warrant: bool = False #form.checkbox(value=True, label="Exclude warrant from Bursa stocks.")
  skipna: bool = False # st.checkbox(value=False, label="Skip NaN values for annualized return & standard deviation.")#False # skip NaN values for annualized return & annualized standard deviation  
  col1, col2 = form.columns([1,1]) # button
  submitted: bool = col1.form_submit_button("Submit")
  updated: bool = col2.form_submit_button("Update")
  form.warning("Please click SUBMIT button to see whether data is downloaded before. If not available, \
            then click UPDATE button to fetch data from Yahoo Finance. \
              Hope not to overuse it to avoid getting ban.")
  
  interval = interval_dict[interval] # change human-readable choice to machine readable choice
  return rf,period,interval,confidence_level,include_dividends,exclude_warrant,skipna, submitted, updated
