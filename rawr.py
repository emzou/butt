"""
BEGIN - Script preparation
Section for importing libraries and setting up basic environment configurations
"""
from psaw import PushshiftAPI                               #Importing wrapper library for reddit(Pushshift)
import datetime as dt                                       #Importing library for date management
import pandas as pd                                         #Importing library for data manipulation in python
import matplotlib.pyplot as plt                             #Importing library for creating interactive visualizations in Python
from pprint import pprint                                   #Importing for displaying lists in the "pretty" way (Not required)
import requests 

pd.set_option("display.max_columns", None)                  #Configuration for pandas to show all columns on dataframe
api = PushshiftAPI()                                        #We create an object of the API
"""
END - Script preparation 
"""

"""
BEGIN - DATAFRAME GENERATION FUNCTIONS

Here we are going to make a request to through the API
to the selected subreddit and the results are going 
to be placed inside a pandas dataframe
"""
"""FOR POSTS"""
def data_prep_posts(subreddit, term, start_time, end_time, filters, limit):
    if(len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'domain', 'url',
                   'title', 'num_comments']                 #We set by default some columns that will be useful for data analysis

    
    posts = list(api.search_submissions(
        subreddit=subreddit,                                #We set the subreddit we want to audit
        q=term, 
        after=start_time,                                   #Start date
        before=end_time,                                    #End date
        filter=filters,                                     #Column names we want to get from reddit
        limit=limit,                                   
        ))
    return pd.DataFrame(posts)                              #Return dataframe for analysis

"""FOR COMMENTS"""
def data_prep_comments(subreddit, term, start_time, end_time, filters, limit):
    if (len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'body', 'permalink', 'subreddit']        #We set by default some columns that will be useful for data analysis

    comments = list(api.search_comments(
        subreddit= subreddit,
        q=term,                                             #We set the subreddit we want to audit
        after=start_time,                                   #Start date
        before=end_time,                                    #End date
        filter=filters,                                     #Column names we want to get from reddit
        limit=limit,))                                      
    return pd.DataFrame(comments)                           #Return dataframe for analysis

"""
END - DATAFRAME GENERATION FUNCTIONS
"""
def main():
    subreddit = "buttcoin"                                 #Name of the subreddit we are auditing
    term = 'r/' 
    start_time = int(dt.datetime(2022, 5, 1).timestamp())  #We define the starting date for our search
    end_time = int(dt.datetime(2022, 5, 31).timestamp())   #We define the ending date for our search
    filters = []                                           #We don´t want specific filters
    limit = 5000  
                              

# POSTS
    df_p = data_prep_posts(subreddit, term, start_time,
                         end_time, filters, limit)           #Call function for dataframe creation of comments

    df_p['datetime'] = df_p['created_utc'].map(
        lambda t: dt.datetime.fromtimestamp(t))
    df_p = df_p.drop('created_utc', axis=1)                #Drop the column on timestamp format
    df_p = df_p.sort_values(by='datetime')                 #Sort the Row by datetime
    df_p["datetime"] = pd.to_datetime(df_p["datetime"])    #Convert timestamp format to datetime for data analysis


    df_p.to_csv(f'dataset_{subreddit}_otherposts.csv', sep=',', # Save the dataset on a csv file for future analysis
                header=True, index=False, columns=[
            'id', 'author', 'datetime', 'domain',
            'url', 'title', 'num_comments'
        ])


    # COMMENTS
    #term = 'hello'                                        
    #limit = 20                                              
    df_c = data_prep_comments(subreddit, term, start_time,             
                         end_time, filters,limit)
    print (df_c)
    df_c.to_csv(f'dataset_{subreddit}_othercomments.csv')
  
if __name__== "__main__" : main()