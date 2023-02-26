# -*- coding: utf-8 -*-
"""

small, new version that just pulls from the updated USAJobs API
"""
import requests
import pandas as pd
import os
from datetime import date, timedelta


def connect(authorization_key):
    #passes key to the API
    headers = {'Authorization-Key': authorization_key,
 'Host': 'data.usajobs.gov',
 'User-Agent': 'abigail.haddad@gmail.com'}
    return headers
    
def historical_search(start_date, end_date):
    #formats url and makes request to API
    # this will just get 1,000
    number=str(1) 
    base_url=f'https://data.usajobs.gov/api/historicjoa?PageSize=1000&StartPositionOpenDate={start_date}&EndPositionOpenDate={end_date}&PageNumber={number}'
    results = requests.get(base_url).json()
    searchResultDF= pd.DataFrame.from_dict(results['data'])
    while results['paging']['next']!=None:
        nextURL='https://data.usajobs.gov'+ results['paging']['next']
        results = requests.get(nextURL).json()
        newDF=pd.DataFrame.from_dict(results['data'])
        searchResultDF=pd.concat([searchResultDF, newDF])
    return(searchResultDF)

def current_search(authorization_key, keyword="", positiontitle="", organization=""):
    #formats url and makes request to API
    print(organization)
    number=str(0) 
    base_url=f"https://data.usajobs.gov/api/Search?Organization={organization}&PositionTitle={positiontitle}&Keyword={keyword}&p={number}"
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
    for iteration in range(0, 10):
        for column in df.columns:
            if dict in [type(i) for i in df[column].values]:
                df=unpackColumnDict(df, column)
        df=df.dropna(how='all', axis=1)
    return(df)
     
def getLogin(directory):
    #pulls the the authorization key from a text file
    authorization_key = open(directory.replace("code","key/authorization_key.txt"), "r").read()
    return(authorization_key)

def makeListsDups(df):
    # this might be dropping not actual dups if we pulled columns that we're dropping because they were 
    # mostly empty
    # we might or might not actually want to do this
    df=df.reset_index(drop=True)
    for column in df.columns:
        if list in [type(i) for i in df[column].values]:
            df[column]=df[column].str.join(",")
    print(len(df))
    dfNoDups=df.drop_duplicates()
    print(len(dfNoDups))
    return(dfNoDups)

def current_search_all_steps(keyword, positiontitle, organization):
    directory = os.getcwd()
    authorization_key=getLogin(directory)
    df=current_search(authorization_key, keyword, positiontitle, organization)
    dfExtended=pullFieldsFromDict(df)
    dfNoDups=makeListsDups(dfExtended)
    dfNoDups.to_excel(os.getcwd().replace("code", "data\currentResults.xlsx"))
    return(dfNoDups)

def format_date(string):
    return(string[5:7]+"-"+string[8:10]+"-"+string[0:4])

def genHistoricalData():
    df=pd.DataFrame()
    dates=pd.date_range(date(2023,1,1),date(2023,1,5)-timedelta(days=1),freq='d')
    for i in range(0, len(dates)-1):
        start_date=format_date(str(dates[i]))
        end_date=format_date(str(dates[i+1]))
        try:
            newDF=historical_search(start_date, end_date)
            df=pd.concat([df, newDF], axis=0)
            print(len(newDF))
        except:
            print(start_date)
    return(df)

def getAgencies():
    base_url='https://data.usajobs.gov/api/codelist/agencysubelements'
    results = requests.get(base_url).json()
    agencies=pd.DataFrame(results['CodeList'][0]['ValidValue'])
    activeAgencies=agencies.loc[agencies['IsDisabled']=="No"]
    return(activeAgencies)

def searchAllAgenciesCurrent():
    directory = os.getcwd()
    authorization_key=getLogin(directory)
    agencies=getAgencies()
    codes=list(agencies['Code'])
    dfs=[current_search(authorization_key, organization=i) for i in codes]
    df=pd.concat(dfs, axis=0)
    dfExtended=pullFieldsFromDict(df)
    dfExtended.to_excel(os.getcwd().replace("code", "data\currentResults.xlsx"))
    return(dfExtended)
    
dfAllAgenciesCurrent=searchAllAgenciesCurrent()   

historicalData=genHistoricalData()

    
