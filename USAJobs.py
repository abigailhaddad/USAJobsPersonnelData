# -*- coding: utf-8 -*-
"""

small, new version that just pulls from the updated USAJobs API
"""
import requests
import pandas as pd
import os


def connect(authorization_key):
    #passes key to the API
    headers = {'Authorization-Key': authorization_key,
 'Host': 'data.usajobs.gov',
 'User-Agent': 'abigail.haddad@gmail.com'}
    return headers

    
def historical_search(authorization_key):
    #formats url and makes request to API
    number=str(0) 
    base_url=f"https://data.usajobs.gov/api/historicjoa?PositionSeries=2210&PageNumber={number}"
    results = requests.get(base_url, headers=connect(authorization_key)).json()
    searchResultDF= pd.DataFrame.from_dict(results['data'])
    if len(searchResultDF) == 25:
            while results['data']!= 0:
                number=str(int(number)+1)      
                results = requests.get(base_url+number, headers=connect(authorization_key)).json()
                newDF=pd.DataFrame.from_dict(results['data'])
                searchResultDF=pd.concat([searchResultDF, newDF])
    return(searchResultDF)

def current_search(authorization_key, keyword="", positiontitle=""):
    #formats url and makes request to API
    number=str(0) 
    base_url=f"https://data.usajobs.gov/api/search?PositionTitle={positiontitle}&Keyword={keyword}&?WhoMayApply=All&p={number}"
    results = requests.get(base_url, headers=connect(authorization_key)).json()
    searchResultDF= pd.DataFrame.from_dict(results['SearchResult']['SearchResultItems'])
    if len(searchResultDF) == 25:
            while results['SearchResult']['SearchResultCount']!= 0:
                number=str(int(number)+1)      
                results = requests.get(base_url+number, headers=connect(authorization_key)).json()
                newDF=pd.DataFrame.from_dict(results['SearchResult']['SearchResultItems'])
                searchResultDF=pd.concat([searchResultDF, newDF])
    return(searchResultDF)


def unpackColumnDict(df, column):
    newCols=df[column].apply(pd.Series)
    if len(newCols.columns)>1:
        newDF=pd.concat([df.drop(columns=[column]), newCols], axis=1)
        return(newDF)
    else:
        return(df)

def pullFieldsFromDict(df):
    # we're unpacking the dictionaries in the returned JSON
    # we keep any column if it's filled in for at least 10% of the rows
    # only want to unpack dictionaries
    for iteration in range(0, 10):
        for column in df.columns:
            if dict in [type(i) for i in df[column].values]:
                df=unpackColumnDict(df, column)
        df=df.dropna(thresh=round(len(df)/10), axis=1)
    return(df)
     
def getLogin(directory):
    #pulls the the authorization key from a text file
    authorization_key = open(directory.replace("code","key/authorization_key.txt"), "r").read()
    return(authorization_key)

def main(keyword, positiontitle):
    directory = os.getcwd()
    authorization_key=getLogin(directory)
    df=current_search(authorization_key, keyword, positiontitle)
    dfExtended=pullFieldsFromDict(df)
    dfExtended.to_excel(os.getcwd().replace("code", "data\currentResults.xlsx"))
    return(dfExtended)

keyword=""
positiontitle="data scientist"
df=main(keyword, positiontitle)
# 2,475 seems like the max results. 
"""
directory = os.getcwd()
authorization_key=getLogin(directory)
df_old=historical_search(authorization_key)
dfExtended=pullFieldsFromDict(df_old)
"""