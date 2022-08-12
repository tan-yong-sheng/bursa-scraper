from operator import sub
import streamlit as st

def check_update():
    _ , col2 = st.columns([3,1])
    last_updated = [date for date in open("./data/last_updated.txt", "r") if date.isalnum()]

    if last_updated:
        col2.write(f"Last Updated at {last_updated}")
    else:
        col2.write("Haven't Updated yet.")



