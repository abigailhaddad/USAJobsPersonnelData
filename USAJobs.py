# -*- coding: utf-8 -*-
"""
finding:
    
    -some but not all of the jobs in the current jobs API are also in the historical jobs API
    -there is no overlap between the field names in both APIs
    -it is possible to fetch all historical jobs by going day by day -- but the API breaks a lot
    -it is possible to fetch all current job by going agency by agency
    -it is not possible to purely use regular expressions to pull out "R" the programming language, 
    because there are multiple other contexts where it looks like " R,"
    but you can narrow down what's likely to be a data job (or just use the new data science occ code)
    and then look at that
"""
import requests
import pandas as pd
import os
from datetime import date, timedelta
from bs4 import BeautifulSoup
import time
import quarto


def connect(authorization_key):
    #passes key to the API
    headers = {'Authorization-Key': authorization_key,
 'Host': 'data.usajobs.gov',
 'User-Agent': 'abigail.haddad@gmail.com'}
    return headers
    
def historical_search(start_date, end_date):
    #formats url and makes request to API
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

def genHistoricalDataOnePull(dates):
    name=genFileName(dates)
    df=pd.DataFrame()
    for i in range(0, len(dates)-1):
        start_date=format_date(str(dates[i]))
        end_date=format_date(str(dates[i+1]))
        try:
            newDF=historical_search(start_date, end_date)
            df=pd.concat([df, newDF], axis=0)
            print(len(newDF))
        except:
            print(start_date)
    df.to_pickle(os.getcwd().replace("code", f"data\{name}"))
    df.to_excel(os.getcwd().replace("code", f"data\{name}.xlsx"))
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
    dfExtended.to_pickle(os.getcwd().replace("code", "data\currentResults"))
    dfExtended.to_excel(os.getcwd().replace("code", "data\currentResults.xlsx"))
    return(dfExtended)

def scrapeURLs(controlNumber):
    # start with just getting the text
    time.sleep(3) 
    url=f'https://www.usajobs.gov/job/{controlNumber}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soupText=soup.text.replace("\n","").replace("\r","")
    return(soupText)

def find1560HistoricalJobs():
    start_date='01-01-2020'
    end_date='02-25-2023'
    number=str(1)
    base_url=f'https://data.usajobs.gov/api/historicjoa?PageSize=1000&StartPositionOpenDate={start_date}&EndPositionOpenDate={end_date}&PositionSeries=1560&PageNumber={number}'
    results = requests.get(base_url).json()
    searchResultDF= pd.DataFrame.from_dict(results['data'])
    searchResultDF.to_excel(os.getcwd().replace("code", "data\1560Historical.xlsx"))
    searchResultDF['text']=searchResultDF['usajobsControlNumber'].astype(str).apply(scrapeURLs)
    searchResultDF.to_excel(os.getcwd().replace("code", "data\1560Historical.xlsx"))
    return(searchResultDF)

def genPattern(string):
    lower=string.lower()
    pattern = f"(?<=\s){lower}(?=[\s\W])"
    return(pattern)

def findPrograms(df):
    programs=["SPSS", "SAS", "Stata", "Python", "R", "spark", "pyspark", "git"]
    dictItem={}
    for program in programs:
        pattern=genPattern(program)
        dictItem[program]=df.loc[df['text'].str.lower().str.contains(pattern, regex=True)]
        return(dictItem)

def genFileName(dates):
    # this is for the historical data because the memory constraints are a problem, we need to write out periodically
    name=f'{str(dates[0])[0:10]+ "_to_" + str(dates[-1])[0:10]}_historical_data'
    return(name)


def genHistoricalDataMultiplePulls(first_date, last_date):
    all_dates=pd.Series(pd.date_range(first_date,last_date-timedelta(days=1),freq='d'))
    list_by_month=list(all_dates.groupby(all_dates.map(lambda x: x.month)))
    for dates in list_by_month:
        genHistoricalDataOnePull(dates[1].values)
        

dfAllAgenciesCurrent=searchAllAgenciesCurrent()   

historical1560=find1560HistoricalJobs()

first_date=date(2022, 1, 20)
last_date=date(2022, 2, 10)
genHistoricalDataMultiplePulls(first_date, last_date)

