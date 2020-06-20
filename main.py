# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 07:27:10 2020
This pulls from the USAJobs API and then scrapes the web pages for additional text to look for 
data science/data engineering-related keywords
@author: HaddadAE
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re


def connect(authorization_key):
    #passes key to the API
    headers = {'Authorization-Key': authorization_key,
 'Host': 'data.usajobs.gov',
 'User-Agent': 'abigail.haddad@gmail.com'}
    return headers


def format_dict(results, df_fixed):
    #formats the results of current_search into a df
    for j in range(0, len(results['SearchResult']['SearchResultItems'])):
        df_fixed=df_fixed.append(pd.DataFrame.from_dict(results['SearchResult']['SearchResultItems'][j]['MatchedObjectDescriptor'], orient='index').transpose())
        df_fixed=df_fixed.apply(pd.Series)
    return(df_fixed)

def current_search(authorization_key, JobCategoryCode="", terms=""):
    #formats url and makes request to API
    number=str(1)
    base_url=f"https://data.usajobs.gov/api/search?Organization=AR&JobCategoryCode={JobCategoryCode}&Keyword={terms}&WhoMayApply=All&p="
    df_fixed=pd.DataFrame()
    results = requests.get(base_url+number, headers=connect(authorization_key)).json()
    df_fixed=format_dict(results, df_fixed)
    if len(results['SearchResult']['SearchResultItems']) == 25:
            while results['SearchResult']['SearchResultCount']!= 0 and int(number)<101:
                number=str(int(number)+1)      
                results = requests.get(base_url+number, headers=connect(authorization_key)).json()
                df_fixed=format_dict(results, df_fixed)
    return(df_fixed)

def openToPublic(df):
    #creates public/not public for whether "public" is in list of eligible hiring path
    userArea=df['UserArea'].apply(pd.Series)
    details=userArea['Details'].apply(pd.Series)
    public= details['HiringPath'].apply(lambda set_: 'public' if "public" in set_ else 'not public')
    return(public)

def getJobCat(df):
    #pulls job category name and code
    jobCat=df['JobCategory'].apply(pd.Series)
    details=jobCat[0].apply(pd.Series)
    return(details)
    
def getJobMinandMax(df):
    #pulls job salary min and max
    jobPay=df['PositionRemuneration'][0].apply(pd.Series)
    details=jobPay[0].apply(pd.Series)
    return(details)
    
def cleanInitialDF(df):
    #gets open to public, occupation, and salary range
    df['Public']=openToPublic(df)
    df[['Name', 'Code']]=getJobCat(df)
    df[['MinimumRange', 'MaximumRange', 'RateIntervalCode']]=getJobMinandMax(df)
    return(df)

def pullActualListing(url):
    #pulls all html as text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html')
    return(soup.text)

def pullTextSoup(df):
    #calls pullActualListing on whole series of URLs
    df['textSoup']=df['PositionURI'].apply(pullActualListing)
    return(df)
    
def basicKeywords():
    #we look up all listings with any of these keywords [note - phrases will be treated not as phrases]
    #but we clean that up later
    listOfRolesandSkills=["data scientist", 
                          "data engineer",
                          "python", "machine learning", "sql", 
                          "tableau", "linux", "hadoop", "azure",
                          "kafka", "nosql", "amazon web services", 
                          "hive", "scala", "qlik", "dashboards", 
                          "data visualization"]
    return(listOfRolesandSkills)

def allKeywords():
    #we look for skills that we're only interested in if we know the listing is a data listing
    listOfRoles=basicKeywords()
    listOfRoles=listOfRoles+ ["spark", "java"]
    return(listOfRoles)
    
def combineMultipleSearches(authorization_key):
    #this pulls all of the relevant listings with the basic keywords and drops dups
    dfDict={}
    for word in basicKeywords():
        try:
            dfDict[word]=current_search(authorization_key, terms=word)
        except:
            pass
    dfAll=pd.concat(dfDict.values())
    dfDedup=dfAll.drop_duplicates('PositionURI')
    return(dfDedup)
  
def cleanVarsInSoup(df):
    #this checks for both the basic and additional keywords in the full text
    varList=allKeywords()
    for keyword in varList:
        df[keyword]= df['textSoup'].str.lower().apply(lambda set_: 1 if keyword in set_ else 0)
    return(df)

def moreCleaningText(df):
     varList=allKeywords()
     df['Sum']=df[varList].sum(axis=1)
     justSelect=df.loc[df['Sum']>0]
     justSelect=justSelect.loc[:, (justSelect != 0).any(axis=0)]
     return(justSelect)
     
def getLogin(directory):
    #pulls the the authorization key from a text file
    authorization_key = open(directory+"\\login info\\authorization_key.txt", "r").read()
    return(authorization_key)
    
def exportOutput(directory, df1):
    #outputs all of the results with the current date
    date=str(datetime.date(datetime.now()))
    df1.to_excel(directory + f"\\results\\output_{date}.xlsx")
    #df2.to_excel(directory + f"\\results\\comparison_group_{date}.xlsx")

def countOccsOverall(authorization_key, occPresent):
    #pulls from the API all of the listings for each of the occupations in the data listings
    dfDict={}
    for occ in occPresent:
        dfDict[occ]=current_search(authorization_key, JobCategoryCode=occ)
        dfDict[occ]['JobSearched']=occ
    dfAll=pd.concat(dfDict.values())
    dfAll=cleanInitialDF(dfAll)
    print(len(dfAll))
    return(dfAll)
    
def main(directory):   
    #pulls from the API, cleans, pulls from the actual listings, looks for full keywords
    authorization_key=getLogin(directory)
    df=combineMultipleSearches(authorization_key)
    dfClean=cleanInitialDF(df)
    dfSoup=pullTextSoup(dfClean)
    dfVars=cleanVarsInSoup(dfSoup)
    justSelect=moreCleaningText(dfVars)
    updateVars=[i for i in allKeywords() if i in justSelect.columns]
    justSelect['Sum of Keywords']=justSelect[updateVars].sum(axis=1)
    #occsPresent=list(justSelect['Code'].unique())
    #print(occsPresent)
    #occsOverall=countOccsOverall(authorization_key, occsPresent)
    #print(len(occsOverall))
    exportOutput(directory, justSelect)
    return(justSelect)
    
def keywordGraph(directory, outputData):
    #count of keywords
    date=str(datetime.date(datetime.now()))
    plt.rcdefaults()
    fig, ax = plt.subplots()
    keywords = [i for i in allKeywords() if i in outputData.columns]
    counts= [outputData[i].sum() for i in keywords]
    dictKeys = {keywords[i]: counts[i] for i in range(len(keywords))} 
    dictKeysSort={k: v for k, v in sorted(dictKeys.items(), key=lambda item: item[1], reverse=True)}
    y_pos = np.arange(len(dictKeysSort.keys()))
    ax.barh(y_pos, list(dictKeysSort.values()), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(dictKeysSort.keys()))
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count')
    ax.set_title('Count of Data Listings With The Following Keyword')
    plt.tight_layout()
    plt.savefig(directory + f'\\results\\KeywordCount_{date}.png')
    
def metrics(directory, outputData):
    #metrics for paper
    print(f"There are {len(outputData)} potentially data science/engineer-type jobs.")
    zeroJobs=[i for i in allKeywords() if i not in outputData.columns]
    print(f"The following keywords appeared 0 times in data-related jobs: {zeroJobs} ")
    publicjobs=len(outputData.loc[outputData['Public']=="public"])
    print(f"{publicjobs} jobs were advertised to the public")
    keywordGraph(directory, outputData)
    
    
def pull301s(directory):
    authorization_key=getLogin(directory)
    occ301=current_search(authorization_key, JobCategoryCode="0301", terms="")
    dfSoup=pullTextSoup(occ301)
    return(dfSoup)
    

directory=r'C:\Users\HaddadAE\Git Repos\personnel'
#outputData=main(directory)   
#metrics(directory, outputData)
occ301=pull301s(directory)
def stockData():
    stockDataPhrases=['unsaved data', 'data will','act data', 'data opens', 'https data', 'data usajobs']
    return(stockDataPhrases)
    
def makeDataBigrams(text):
    stockDataPhrases=stockData()
    words = re.findall(r'[A-Za-z]+', text.lower())
    bigrams = zip(words, words[1:])
    counts = Counter(bigrams)
    data=[" ".join(list(i[0])) for i in counts.most_common() if [i][0][0][0]=="data" or[i][0][0][1]=="data"]  
    noStockData=[i for i in data if i not in stockDataPhrases]
    return(noStockData)
    
def makeAllDataBigrams(series):
    output=series.apply(makeDataBigrams)    
    return(output)
    
occ301['dataBigrams']= makeAllDataBigrams(occ301['textSoup'])
flat_list = [item for sublist in occ301['dataBigrams'] for item in sublist]
counts = Counter(flat_list)

#   

"""
#829 


#pull agency list
from io import StringIO
response = requests.get("https://data.usajobs.gov/api/codelist/agencysubelements")
jdata = json.loads(response.content)
agencyList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
Army=agencyList.loc[agencyList['Value'].str.contains("Army")]


#pull occ list

response = requests.get("https://data.usajobs.gov/api/codelist/occupationalseries")
jdata = json.loads(response.content)
OccList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
Ops=OccList.loc[OccList['Value'].str.contains("Operations Research")]
"""

