from pickle import TRUE
import pandas as pd
import re 
# cleans up columns 
df = pd.read_csv("/Users/emilyzou/othercoms1.csv", usecols= ['author', 'body', 'created_utc'])
    #got rid of automod data 
    #df.drop(df[df['author'] == "AutoModerator"].index, inplace = True)
# if column contains 'r/' then create new column with the text right after it 
for i in df['body']: 
    if 'r/' in i: 
        subname = df['body'].str.split('r/').str[1]
        subname = subname.str.split(' ').str[0]
df["subname"]= subname 
# print (subname)
# convert epoch time to readable time 
df['created_utc'] = pd.to_datetime(df['created_utc'], unit= 's')
# print (df['created_utc'])
#saves onto new csv file, made othercoms3.csv 
    #df.to_csv(f'othercoms3.csv', sep=',', # Save the dataset on a csv file for future analysis
                #header=True, index=False, columns=[
            #'author', 'body', 'created_utc', 'subname'
        #])
# start using othercoms3 now 
df_n = pd.read_csv ("/Users/emilyzou/othercoms3.csv", usecols= ['author', 'body', 'created_utc', 'subname'])
df_n['subnamec'] = df_n['subname']
#df_n.to_csv(f'godplease.csv', sep=',', # Save the dataset on a csv file for future analysis
            #header=True, index=True, columns=[
            #'author', 'body', 'created_utc', 'subname', 'subnamec'
        #])
df_g= pd.read_csv ("/Users/emilyzou/godplease.csv", usecols = ('author', 'body', 'created_utc', 'subname', 'subnamec'))
for i in df_g['subname']: 
    if '?' in str(i): 
        subnamec = df_g['subname'].str.split('?').str[0]
df_g['subnamec'] = subnamec 
for i in df_g['subname']: 
    if '/' in str(i): 
        subnamec = df_g['subname'].str.split('/').str[0]
df_g['subnamec'] = subnamec 
for i in df_g['subname']: 
    if ',' in str(i): 
        subnamec = df_g['subname'].str.split(',').str[0]
df_g['subnamec'] = subnamec 
for i in df_g['subname']: 
    if '!' in str(i): 
        subnamec = df_g['subname'].str.split('!').str[0]
df1= pd.DataFrame (df_g['subname'])
df2= pd.DataFrame (subnamec)
df1.update(df2)
print (df_g['subname'])
# df_g.to_csv(f'godlmao2.csv',sep=',', header = True, index= True, columns= ['author', 'body', 'created_utc', 'subname', 'subnamec'])
#, sep= ',' header=True, index= True 
# #columns = ['author', 'body', 'created_utc', 'subname', 'subnamec']
# get summary statistics 
    # print (df['subname'].value_counts(ascending =False))
    # df_s = df ['subname'].value_counts(ascending =False)
    # df_s.to_csv(f'summary.csv', sep=',', header= True,index=True)
    # print (df['subname'].value_counts(normalize=True))