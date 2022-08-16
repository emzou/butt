from psaw import PushshiftAPI                               
import datetime as dt                                       
import pandas as pd                                         
import matplotlib.pyplot as plt                             
from pprint import pprint                                   
import requests 
from pickle import TRUE
import numpy as np
import re 

pd.set_option("display.max_columns", None)                  
api = PushshiftAPI()                                       

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
    subreddit = "bitcoin"                                 #Name of the subreddit we are auditing
    term = 'r/' 
    start_time = int(dt.datetime(2020, 5, 1).timestamp())  #We define the starting date for our search
    end_time = int(dt.datetime(2020, 5, 31).timestamp())   #We define the ending date for our search
    filters = []                                           #We don´t want specific filters
    limit = 5000  
                              

# Comments
    df_c = data_prep_comments(subreddit, term, start_time,             
                         end_time, filters,limit)
    
    df_c.drop(df_c[df_c['author'] == "AutoModerator"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "rBitcoinMod"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "AmputatorBot"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "NiceDoctorBeam"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "CointestAdmin"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "ccModBot"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "Spacesider"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "jwinterm"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "Cintre"].index, inplace = True)
    
    for i in df_c['body']: 
        if 'r/' in i: 
            subname = df_c['body'].str.extract (r"(?<=r/)(.*?)(?=\W)")
            df_c['subname']= subname 
    for j in df_c['body']: 
        if '/comments/' in j:
            result = df_c['body'].str.extract (r"(?<=com)(.*?)(?=comments)")
            df_c.head()
            df_c ['indirect']= result 

#Time 
    df_c['created_utc'] = pd.to_datetime(df_c['created_utc'], unit= 's')

    df_c.to_csv(f'bitcoincomments_{start_time}_.csv', sep=',', 
        header=True, index=True, columns=[
        'author', 'body', 'created_utc', 'subname', 'indirect' 
       ])


     
if __name__== "__main__" : main()