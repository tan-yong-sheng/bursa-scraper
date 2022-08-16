import streamlit as st

st.markdown("# Introduction")
st.warning("This is a hobby project and is built for academic application of CAPM model in \
        Bursa stock market. In any event, the project creator shall neither be liable\
        for any use of materials and data herein and nor promise the accuracy\
       and completeness of the data.")

st.markdown("## Concept of the project")
st.write("This project aims to calculate beta, annualized return (or expected return), \
        and some other performance metrics such as Sharpe ratio, Treynor ratio\
         of all Bursa equity using CAPM model as below:")
st.latex(r"""E(r_i) = r_f + \beta(E(r_m) - r_f)""")
st.write("where:")
st.latex(r"""
         \\ r_i : \,Expected\,return\,of\,the\,equity \\
         r_f: \,Risk\,free\,rate \\
         \beta: \,Beta\,of\,the\,equity \\
         r_m:\,Expected\,market\,return \\
         """)

st.write("Here is how some of the variables calculated in this project:")
st.latex(r"Annualized\,return\,of\,equity: \sqrt[n]{(1+r_i) \times (1+r_i+2) \times \cdots \times (1+r_n)}")
st.latex(r"Skewness: \frac{1}{N} \sum_{i=1}^{n} \left[ \frac{r_i - \overline{r_i}}{\sigma} \right] ^3")
st.latex(r"Pearson\,Kurtosis: \frac{1}{N} \sum_{i=1}^{n} \left[ \frac{r_i - \overline{r_i}}{\sigma} \right] ^4")
st.latex(r"Fisher\,Kurtosis: \frac{1}{N} \sum_{i=1}^{n} \left[ \frac{r_i - \overline{r_i}}{\sigma} \right] ^4 - 3")

st.latex(r"""Sharpe\,ratio: \frac{E(r_m) -r_f}{\sigma}""")
st.latex(r"""Treynor\,ratio: \frac{E(r_m) - r_f}{\beta}""")
st.info("You may take reference with below YouTube video to know how to calculate some of the variables above in Excel: \
        [Risk-adjusted performance evaluation: Sharpe, Treynor, and Jensen's Alpha (Excel)](https://www.youtube.com/watch?v=zvChPqsKZjc&t=462s)")

st.markdown("## How This Project is Built?")
st.markdown("I have spent about 2 weeks to build this project. This project is built using python \
        language, with some libraries installed such as `yfinance` to scrape yahoo finance \
         price history, `requests` to fetch stock tickers from i3investor website, `scipy` \
         to calculate beta using linear regression plot and  expected return using geometric \
        formula. Besides, `pandas` is used to handle, clean and process the data in tabular \
        structure and `bokeh` to plot simple [interactive charts](/chart) on this `streamlit` dashboard.")

st.markdown("## Limitations of This Project")
st.write("We could not promise the accuracy of the \
        data due to some technical inabilities. Below are some limitations: ")
st.markdown("1. Data Inconsistency")
st.write("We scrape price data from a free website: Yahoo Finance. Thus, the server \
         may return us certain WRONG PRICE variables mixed inside the our \
        scraped data if the server found us sending too much requests to get the data")
st.markdown("2. Not using T-bill yield history as risk free rate")
st.write("""This project assumes the risk free rate input as a CONSTANT risk free rate history yield  
         instead of Malaysian government bond yield. Currently, haven't yet explore website \ 
         that is easy to scrape for this information.""")
st.markdown("3. Exclude Dividend in Stock Return & Beta Calculation")
st.write("""This project does not include dividends when calculating stock return due to \ 
         server constraints because the scraping process would be very slow if want to scrape dividend
         data of all the bursa tickers.""")
st.markdown("4. Potential Calculation Mistake")
st.write("""Due to massive data and processes to be handled, I haven't yet cross-checked the calculation \
        and thus honestly, the project is prone to errors. Also, this project uses other python """)

st.markdown("## Why I Build This Project?")
st.write("I believe data should be easy for people to access for better information decision. \
        During degree, I was troubled when picking which stocks or companies with certain criteria to \
        be applied in finance or portfolio model.  And this shall be a starter project for that.")

