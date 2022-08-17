from pathlib import Path
import pandas as pd 
import glob, os
from datetime import datetime

# specify the subreddit you care about
subreddit = "buttcoin"

# TODO use datetime to get a list of all of the month and years between our start and end dates

list_of_years = pd.date_range('2011-07-01','2012-07-31', freq='MS').strftime("%Y").tolist()
list_of_months = pd.date_range('2011-07-01','2012-07-31', freq='MS').strftime("%m").tolist()
lst_tuple = list (zip(list_of_years,list_of_months))

for year_month in lst_tuple:
    year = year_month[0]
    year = int (year)
    month = year_month[1]
    month = int (month)
    with open ("run_api_calls.sh", "a") as o: 
        o.write (f"/Users/emilyzou/butt/unlucky.py -m {month} -y {year} -s buttcoin -o ./pushshift_data \n")

    
    
