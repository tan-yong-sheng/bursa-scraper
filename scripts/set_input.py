from operator import sub
import streamlit as st

def check_update():
    _ , col2 = st.columns([3,1])
    last_updated = [date for date in open("./data/last_updated.txt", "r") if date.isalnum()]

    if last_updated:
        col2.write(f"Last Updated at {last_updated}")
    else:
        col2.write("Haven't Updated yet.")

class InputForm:
    def __new__(self):
        with st.form("input form"):
            self.rf: float = st.number_input(value=0.04, label="Risk free rate: ")# 0.04 # risk free rate
            self.period: int = st.number_input(value = 5, min_value=1, max_value=10, label="Valid period: 1-10 Year") # 5 # e.g. 5 = 5 years
            self.interval: str = st.selectbox(options = ["1d","1wk","1mo","3mo"],index=1, label="Valid interval: 1d,1wk,1mo,3mo") #"1wk"
            self.confidence_level: float = st.selectbox(options=[0.1, 0.05, 0.01, 0.001], index=1, label="Confidence level of linear regression: ")
            self.include_dividends: bool = False #: bool = st.checkbox(value=False, label="Whether to consider dividend into stock returns when calculating beta?")
            self.exclude_warrant: bool = st.checkbox(value=True, label="Exclude warrant from Bursa stocks.")
            self.skipna: bool = False # st.checkbox(value=False, label="Skip NaN values for annualized return & standard deviation.")#False # skip NaN values for annualized return & annualized standard deviation  
            self.submitted = st.form_submit_button("Submit")
        return self.rf, self.period, self.interval, self.confidence_level, \
                self.include_dividends, self.exclude_warrant, self.skipna, self.submitted


