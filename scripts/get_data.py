import requests
import pandas
import json

def getStockOverview():
    # Get stock tickers from i3investor and then upload to the google spreadsheet: "Bursa stock list" sheet
    # start scraping stock list from i3investor
    url = "https://klse.i3investor.com/wapi/web/stock/listing/datatables"
    data = {"dtDraw":1,"start":0,"order":[{"column":1,"dir":"asc"}],"page":0,"size":100,"marketList":[],"sectorList":[],"subsectorList":[],"type":"","stockType":""}
    retries = 2

    session = requests.Session()
    response = session.post(url, json=data)

    df_stock_list = pandas.DataFrame()

    #for idx in range(0,11,1):
    while len(response.json()["data"]) != 0:
      try:
        response = session.post(url, json=data)
      
      except requests.exceptions.HTTPError as err:
        code = err.response.status_code

        if code in [429,500,502,503,504]:
          continue
        
        else:
          for retry in range(0,retries,1):
            response = session.post(url, json=data)
            print(response.raise_for_status())
        
      finally:
        df_stock_list= pandas.DataFrame(json.loads(response.text)["data"]) if df_stock_list.empty else pandas.concat((df_stock_list, pandas.DataFrame(json.loads(response.text)["data"])), axis=0)
        #workSheet.append_rows(df_stock_list_values, value_input_option='RAW', table_range ="A1")

        data["dtDraw"] +=1
        data["start"] +=100
        data["page"]+=1

    # data cleaning for this stock ticker table, e.g., drop unwanted columns and reordering them
    clean_df_stock_list = df_stock_list.drop([0,1,8,11], axis=1) # drop unwanted columns
    clean_df_stock_list = clean_df_stock_list[[12,13,10,14,9, 2,3,4,5,6,7]] # reordering the columns
    clean_df_stock_list.columns = ["STOCK SYMBOL","STOCK CODE","SECTOR","SUBSECTOR", "MKT", "OPEN","LAST","CHG%","CHG","VOL","MKT CAP"] #rename the columns

    clean_df_stock_list[["OPEN","LAST","CHG%","CHG","VOL","MKT CAP"]] \
    = clean_df_stock_list[["OPEN","LAST","CHG%","CHG","VOL","MKT CAP"]].replace(
                {"<((\s|\w|[='-/])+)>":"",
                            "K": "E+03",
                            "M": "E+06",
                            "B": "E+09",}, regex=True)

    clean_df_stock_list["MKT CAP"] = clean_df_stock_list["MKT CAP"].str.replace(" ","") #.map(pandas.eval).astype(float) # convert string (e.g., 897 M)
    clean_df_stock_list["VOL"] = clean_df_stock_list["VOL"].str.replace(" ","") #.map(pandas.eval).astype(int)
    clean_df_stock_list= clean_df_stock_list.apply(pandas.to_numeric, errors="ignore") 
    print(clean_df_stock_list.dtypes)
    return clean_df_stock_list.sort_values("MKT CAP",ascending=False)
    
def getStockTicker(clean_df_stock_list: pandas.core.frame.DataFrame):
    # update stock code list that need to scrape
    stock_list = clean_df_stock_list["STOCK CODE"]
    full_stock_list = ["^KLSE"]
    full_stock_list.extend(stock_list)
    return full_stock_list
    