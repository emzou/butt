from pathlib import Path
import glob, os
from datetime import datetime

# specify the subreddit you care about
subreddit = "buttcoin"

# figure out when the subreddit 
# make sure to update this accordingly
start_m = 7
start_y = 2011

end_m = 7
end_y = 2022

# TODO use datetime to get a list of all of the month and years between our start and end dates

list_of_year_month_combos = [] # (2011, 7), (2011, 8), (2011, 9) ... (2022, 7)

for year_month in list_of_year_month_combos:
    year = year_month[0]
    month = year_month[1]

    print("python unlucky.py -m {} -y {} -s {} -o {}")#TODO arg for printing to file
    