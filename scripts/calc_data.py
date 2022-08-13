
from scripts import get_data
import scipy
from typing import Tuple, Union
import logging
import pandas

def calc_beta(excess_stock_return:list, excess_index_return:list, confidence_level: float) -> Tuple[float, float, float, float, float, str]:
    beta, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(x=excess_index_return, y=excess_stock_return)
    rsquared = rvalue**2
    normality = normality_test(excess_stock_return, confidence_level) 
    return beta, intercept, rsquared, pvalue, stderr, normality

def normality_test(excess_stock_return:list, confidence_level:float, nan_policy="propagate") -> Union[bool, str]: 
    # D’Agostino’s K-squared test on excess return data
    try:  
        k2, p = scipy.stats.normaltest(excess_stock_return, nan_policy=nan_policy)
        if p > confidence_level:
            return False
        elif p <= confidence_level:
            return "normal"
    except ValueError as error:
        logging.debug(error)

def getRegression(df: pandas.core.frame.DataFrame, period: int, rf: float, confidence_level: float) -> pandas.core.frame.DataFrame:
    df_ny = get_data.filterDataBasedYear(df, period).set_index("Date").sub(rf)
    df_ny = df_ny.apply(lambda x: calc_beta(x.values.tolist(), df_ny["^KLSE"].values.tolist(), confidence_level=confidence_level), axis=0)
    df_ny = df_ny.transpose().reset_index()
    df_ny.columns = ["STOCK CODE",f"BETA_{period}Y", f"INTERCEPT_{period}Y", f"R-SQUARED_{period}Y", f"P-VALUE_{period}Y", f"BETA STANDARD ERROR_{period}Y", f"NORMALITY TEST_{period}Y"] 
    df_ny["STOCK CODE"] = df_ny["STOCK CODE"].replace({"[.]KL": ""}, regex=True)
    return df_ny

def getAnnualizedReturn(df:pandas, interval:str, type:str="geometric", skipna:bool=False):
    """Params:
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    if type == "arithmetic":
        df= df.mean(skipna=skipna)
    elif type == "geometric":
        if skipna:
            df = df.add(1).apply(lambda x: scipy.stats.gmean(x.dropna(inplace=False)), axis=0).sub(1)
        else:
            df = df.add(1).apply(scipy.stats.gmean).sub(1)
    annualized_return_dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    annualized_return = df.multiply(annualized_return_dict[interval])
    return annualized_return

def getAnnualizedStdDeviation(df:pandas, interval:str, skipna:bool):
    """Params:
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    df = df.std(skipna=skipna)
    annualized_std_dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    annualized_std = df.multiply(annualized_std_dict[interval])
    return annualized_std
