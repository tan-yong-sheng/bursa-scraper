import streamlit as st
import scripts
import pandas
from functools import reduce
import re

def refreshData(csvdir:scripts.process_csv.csvDirectory, rf: float, period:int,interval:str, 
                confidence_level:float, exclude_warrant:bool):
    ## Retrieve Data & Data Cleaning
    ### Step 1: Get stock ticker from Bursa
    with st.spinner("Get stock tickers from Bursa..."):
        clean_df_stock_list: list = scripts.get_data.getStockOverview()
        full_stock_list: list = scripts.get_data.getStockTicker(clean_df_stock_list)

    if exclude_warrant:
        with st.spinner("Excluding warrants from Bursa tickers"):
            full_stock_list: list = [stock for stock in full_stock_list if not bool(re.match
                                (pattern="\d+[a-zA-Z]+",string=stock))]

    # Step 2: Download stock return dataframe of Bursa Malaysia stocks from yahoo finance using yfinance
    with st.spinner("Download stock price history..."):
        stock_df = scripts.get_data.getData(ticker_code=full_stock_list, period=str(period)+"y",
                                            interval=interval)

    with st.spinner("Calculate stock return..."):   
        total_stock_return_df: pandas = scripts.get_data.getReturn(stock_df)

    #### -- Get beta and alpha using Linear Regression
    # Step 3: calculate beta using Linear Regression
    with st.spinner("Forming Linear Regression..."):   
        regression_df: pandas.DataFrame = scripts.calc_data.getRegression(total_stock_return_df, period=period, interval=interval, 
                                                    rf=rf, confidence_level=confidence_level)

        #### -- Calculate Annualized Return and Standard Devation
        # Step 4: Calculate 2Y-Beta, 5Y-Beta and standard deviation of equity to Google Spreadsheet: sheet "Calculated" 
        x_list = []
        descriptive_df = pandas.DataFrame()

        descriptive_df[f"annualized_standard_deviation_of_equity_{period}Y"] = scripts.calc_data.getAnnualizedStdDeviation(
                                                            scripts.get_data.filterDataBasedYear(total_stock_return_df, period =2) 
                                                            .set_index("Date"), interval=interval, skipna=False)
        descriptive_df[f"annualized_return_of_equity_{period}Y"] = scripts.calc_data.getAnnualizedReturn( 
                                                                    scripts.get_data.filterDataBasedYear(total_stock_return_df, period=2)
                                                                    .set_index("Date"), interval=interval, skipna=False, type="geometric")
        descriptive_df = descriptive_df.reset_index()
        descriptive_df = descriptive_df.rename(columns={"index":"STOCK CODE"})
        descriptive_df["STOCK CODE"] = descriptive_df["STOCK CODE"].replace("[.]KL", "", regex=True)

    # descriptive_df.sort_values(f"annualized_return_of_equity_{period}Y", ascending=False)

    ## Merge All DataFrame
    # merge dataframes of `clean_df_stock_list`, `regression_df`, `descriptive_df`
    with st.spinner("Combining data..."):
        main_dataframe = [clean_df_stock_list, regression_df, descriptive_df]

        merged_df = reduce(lambda left, right: pandas.merge(left, right, on="STOCK CODE", how ="left"), main_dataframe)

        # then calculate other performance metrics such as SHARPE RATIO, Treynor Ratio, and Jensen Alpha
        interval_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
        merged_df[f"SHARPE_RATIO_{period}Y"] = merged_df[f"annualized_return_of_equity_{period}Y"].sub((1+rf)**(1/interval_dict[interval]) -1).divide(merged_df[f"annualized_standard_deviation_of_equity_{period}Y"])
        merged_df[f"TREYNOR_RATIO_{period}Y"] = merged_df[f"annualized_return_of_equity_{period}Y"].sub((1+rf)**(1/interval_dict[interval]) -1).divide(merged_df[f"BETA_{period}Y"])

        
        ## Aggregate Data
        sub_sector_overview_df = merged_df.groupby(["SUBSECTOR", "SECTOR"]).agg({f"BETA_{period}Y": "mean",
                                            f"INTERCEPT_{period}Y": "mean",
                                            f"annualized_return_of_equity_{period}Y": "mean", 
                                            f"annualized_standard_deviation_of_equity_{period}Y": "mean"
                                            }).dropna()

        sector_overview_df = merged_df.groupby("SECTOR").agg({f"BETA_{period}Y": "mean",
                                            f"INTERCEPT_{period}Y": "mean",
                                            f"annualized_return_of_equity_{period}Y": "mean", 
                                            f"annualized_standard_deviation_of_equity_{period}Y": "mean"
                                            }).dropna()

    # save df to csv
    with st.spinner("Saving data..."):
        merged_df.to_csv(csvdir.bursa_companies_csv, columns= merged_df.columns)
        sector_overview_df.to_csv(csvdir.sector_overview_csv, columns= sector_overview_df.columns)
        sub_sector_overview_df.to_csv(csvdir.subsector_overview_csv, columns=sub_sector_overview_df.columns)
