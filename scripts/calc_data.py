import scripts
import scipy
from typing import Tuple, Union
import logging
import pandas
import scipy.stats
import math

def calc_linregress_data(excess_stock_return:list, excess_index_return:list, confidence_level: float, nan_policy: str ="propagate") -> Tuple[float, float, float, float, float, str]:
  beta, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(x=excess_index_return, y=excess_stock_return)
  rsquared = rvalue**2
  normality = normality_test(excess_stock_return, confidence_level)
  return beta, intercept, rsquared, pvalue, stderr, normality

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

def getRegression(df: pandas.core.frame.DataFrame, period: int, interval:str, rf: float, confidence_level: float) -> pandas.core.frame.DataFrame:
  interval_dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
  df_ny = scripts.get_data.filterDataBasedYear(df, period).set_index("Date").sub((1+rf)**(1/interval_dict[interval]) -1)
  df_ny = df_ny.apply(lambda x: calc_linregress_data(x.values.tolist(), df_ny["^KLSE"].values.tolist(), confidence_level=confidence_level), axis=0)
  df_ny = df_ny.transpose().reset_index()
  df_ny.columns = ["STOCK CODE",f"BETA_{period}Y", f"INTERCEPT_{period}Y", f"R-SQUARED_{period}Y", f"P-VALUE_{period}Y", f"BETA STANDARD ERROR_{period}Y", f"NORMALITY TEST_{period}Y" ] 
  df_ny["STOCK CODE"] = df_ny["STOCK CODE"].replace({"[.]KL": ""}, regex=True)
  return df_ny
import math

def getAnnualizedReturn(df:pandas.DataFrame, period:str, calc_type:str="geometric", skipna:bool=False) -> float:
    """Params:
    interval : str
        Valid intervals: 1d, 1wk,1mo,3mo
    """
    annualized_return: float = None
    annualized_return_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    if calc_type == "arithmetic":
        print("Please use geometric return calc_type!")
    if calc_type == "geometric":
        annualized_return: float = df.add(1).cumprod(skipna=skipna).iloc[-1] ** (1/period) -1
    return annualized_return
  
def getAnnualizedStdDeviation(df: pandas.DataFrame, interval:str, skipna:bool) -> float:
    """Params:
    interval : str
        Valid intervals: 1d,1wk,1mo,3mo
    """
    annualized_std_dict: dict = {"1d": 252,"1wk":52, "1mo":12, "3mo":4}
    annualized_std: float = df.std(skipna=skipna) * math.sqrt(annualized_std_dict[interval])
    return annualized_std

def getSkewness(df: pandas.DataFrame) -> float:
  # skewsness and kurtosis reference: https://www.analyticsvidhya.com/blog/2021/05/shape-of-data-skewness-and-kurtosis/
  skewness = scipy.stats.skew(df, nan_policy="propagate") # negative skewed return is preferred -> frequent small returns and less big losses -> Reference: https://corporatefinanceinstitute.com/resources/knowledge/other/negatively-skewed-distribution/#:~:text=Negatively%20Skewed%20Distribution%20in%20Finance&text=Although%20many%20finance%20theories%20and,and%20a%20few%20large%20losses.
  return skewness

def getPearsonKurtosis(df: pandas.DataFrame) -> float:
  pearson_kurtosis = scipy.stats.kurtosis(df, fisher=False, nan_policy="propagate") # Mesokurtic or normal distribution when kurtosis=3 
  return pearson_kurtosis

def getFisherKurtosis(df: pandas.DataFrame) -> float:
  fisher_kurtosis = scipy.stats.kurtosis(df, fisher=True, nan_policy="propagate") # unlike pearson kurtosis, already exclude 3
  return fisher_kurtosis