
from statistics import geometric_mean
from scripts import get_data
import scipy
from typing import Tuple, Union
import logging
import pandas
import scipy.stats

def calc_linregress_data(excess_stock_return:list, excess_index_return:list, confidence_level: float, nan_policy: str ="propagate") -> Tuple[Union[float, str]]:
  beta, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(x=excess_index_return, y=excess_stock_return)
  rsquared: float = rvalue**2
  # skewsness and kurtosis reference: https://www.analyticsvidhya.com/blog/2021/05/shape-of-data-skewness-and-kurtosis/
  skewness: float = scipy.stats.skew(excess_stock_return, nan_policy=nan_policy) # negative skewed return is preferred -> frequent small returns and less big losses -> Reference: https://corporatefinanceinstitute.com/resources/knowledge/other/negatively-skewed-distribution/#:~:text=Negatively%20Skewed%20Distribution%20in%20Finance&text=Although%20many%20finance%20theories%20and,and%20a%20few%20large%20losses.
  pearson_kurtosis: float = scipy.stats.kurtosis(excess_stock_return, fisher=False, nan_policy=nan_policy) # Mesokurtic or normal distribution when kurtosis=3 
  fisher_kurtosis: float = scipy.stats.kurtosis(excess_stock_return, fisher=True, nan_policy=nan_policy) # unlike pearson kurtosis, already exclude 3
  normality: Union[bool, str] = normality_test(excess_stock_return, confidence_level)
  return beta, intercept, rsquared, pvalue, stderr, skewness, pearson_kurtosis, fisher_kurtosis, normality

def normality_test(excess_stock_return:list, confidence_level:float) -> Union[bool, str]:
  # The Kolmogorov-Smirnov test - to test normality of stock returns data
  # null hypothesis: the data sample is normal
  # Youtube link: https://www.youtube.com/watch?v=R-MBFCK3p9Q
  try:  
    k2, p= scipy.stats.kstest(excess_stock_return, scipy.stats.norm.cdf)
    if p > confidence_level: # if p-value greater than confidence level, accept null hypothesis 
      return "normal"
    elif p <= confidence_level: # if p-value lesser than confidence level, reject  null hypothesis
      return "not normal"
  except ValueError as error:
    logging.debug(error)

def getRegression(df: pandas.DataFrame, period: int, interval:str, rf: float, confidence_level: float) -> pandas.DataFrame:
  interval_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
  df_ny: pandas.DataFrame = get_data.filterDataBasedYear(df, period).set_index("Date").sub(rf/interval_dict[interval])
  df_ny: pandas.DataFrame = df_ny.apply(lambda x: calc_linregress_data(x.values.tolist(), df_ny["^KLSE"].values.tolist(), confidence_level=confidence_level), axis=0)
  df_ny: pandas.DataFrame = df_ny.transpose().reset_index()
  df_ny.columns = ["STOCK CODE",f"BETA_{period}Y", f"INTERCEPT_{period}Y", f"R-SQUARED_{period}Y", 
                   f"P-VALUE_{period}Y", f"BETA STANDARD ERROR_{period}Y",f"SKEWNESS_{period}Y" ,
                   f"PEARSON_KURTOSIS_{period}Y", f"FISHER_KURTOSIS_{period}Y",f"NORMALITY TEST_{period}Y" ] 
  df_ny["STOCK CODE"] = df_ny["STOCK CODE"].replace({"[.]KL": ""}, regex=True)
  return df_ny

def getAnnualizedReturn(df:pandas.DataFrame, interval:str, type:str="geometric", skipna:bool=False) -> float:
    """Params:
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    annualized_return: float = None
    annualized_return_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    if type == "arithmetic":
        arithmetic_mean: float = df.mean(skipna=skipna)
        annualized_return: float = arithmetic_mean * annualized_return_dict[interval]
    if type == "geometric":
        if skipna:
            geometric_mean: float = df.add(1).apply(lambda x: scipy.stats.gmean(x.dropna(inplace=False)), axis=0).sub(1)
        else:
            geometric_mean: float = df.add(1).apply(scipy.stats.gmean, axis=0).sub(1)
        annualized_return: float = ((1+geometric_mean) ** annualized_return_dict[interval]) -1
    return annualized_return

def getAnnualizedStdDeviation(df: pandas.DataFrame, interval:str, skipna:bool) -> float:
    """Params:
    interval : str
        Valid intervals: 1d,1wk,1mo,3mo
    """
    std_deviation: float = df.std(skipna=skipna)
    annualized_std_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    annualized_std: float  = std_deviation * annualized_std_dict[interval]
    return annualized_std
