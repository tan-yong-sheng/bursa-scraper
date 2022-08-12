import streamlit as st
from scripts import set_input

st.set_page_config("Input Form")

st.markdown("# Refresh data")

set_input.check_update()
input_form = set_input.InputForm()

