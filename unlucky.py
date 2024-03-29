#!/usr/bin/env python
from psaw import PushshiftAPI                               
import datetime as dt                                       
import pandas as pd                                         
import matplotlib.pyplot as plt                             
from pprint import pprint                                   
import requests 
from pickle import TRUE
import numpy as np
import re, os
import argparse
import calendar

pd.set_option("display.max_columns", None)                  

def data_prep_posts(subreddit, term, start_time, end_time, filters, limit):
    if(len(filters) == 0):
        filters = ['id', 'author', 'created_utc', 'domain', 'url', 'title', 'num_comments']                
    
    posts = list(api.search_submissions(
        subreddit=subreddit,                                
        q=term, 
        after=start_time,                                   
        before=end_time,                                    
        filter=filters,                                    
        limit=limit,                                   
        ))
    return pd.DataFrame(posts)                              

def data_prep_comments(subreddit, term, start_time, end_time, filters, limit):
    if (len(filters) == 0):
        filters = ['id', 'author', 'created_utc', 'body', 'permalink', 'subreddit']       

    comments = list(api.search_comments(
        subreddit= subreddit,
        q=term,                                             
        after=start_time,                                   
        before=end_time,                                    
        filter=filters,                                     
        limit=limit,))                                      
    return pd.DataFrame(comments)                           

def parse_args():
    parser = argparse.ArgumentParser(description='Create a dataset.')
    parser.add_argument('-m', '--month', help='The month to grab data for', required=True, type=str)
    parser.add_argument('-y', '--year', help='The year to grab data for', required=True, type=str)
    parser.add_argument('-s', '--subreddit', help='The subeddit to grab data for', required=True, type=str, default="buttcoin")
    parser.add_argument('-o', '--out', help='Directory for outputs', required=True, type=str, default="./pushshift_data")
    args = parser.parse_args()
    return(args)
     
if __name__== "__main__" :
    args = parse_args()

    if not os.path.isdir(args.out):
        os.mkdir(args.out)

    year = args.year
    year = int (year)
    month = args.month
    month = int (month)
    m_range = calendar.monthrange(year, month)

    subreddit = args.subreddit                       
    term = 'r/' 
    start_time = int(dt.datetime(year, month, 1).timestamp())
    end_time = int(dt.datetime(year, month, m_range[1]).timestamp())
    filters = []                                           
    limit = 5000  

    # start up API
    api = PushshiftAPI()

    # Posts
    df_p = data_prep_posts(subreddit, term, start_time, end_time, filters, limit)

    # Comments
    df_c = data_prep_comments(subreddit, term, start_time, end_time, filters,limit)
    
    # dropping common bot comments
    df_c.drop(df_c[df_c['author'] == "AutoModerator"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "rBitcoinMod"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "AmputatorBot"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "NiceDoctorBeam"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "CointestAdmin"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "ccModBot"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "Spacesider"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "jwinterm"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "Cintre"].index, inplace = True)
    df_c.drop(df_c[df_c['author'] == "SnapshillBot"].index, inplace = True) 
    
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

    # output the files
    # posts
    df_p.to_csv(f'{subreddit}_posts_{year}_{month}.tsv', sep='\t', header=True, index=False)

    # comments
    df_c.to_csv(f'{subreddit}_comments_{year}_{month}.tsv', sep='\t', 
        header=True, index=False, columns=[
        'author', 'body', 'created_utc', 'subname', 'indirect' 
       ])
