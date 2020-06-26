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
import operator
import time

def dataStock():
    dataStockPhrases=['data and',
                      'and data',
                      'data to',
                      'of data',
                      'data for',
                      'data from',
                      'data in',
                      'data is',
                      'accurate data',
                      'pertinent data',
                      'data into',
                      'data pertaining',
                      'or data',
                      'for data',
                      'data effectively',
                      'data provide',
                      'the data',
                      'data on',
                      'data travel',
                      'data used',
                      'data this',
                      'data you',
                      'data files',
                      'needed data',
                      'data or',
                      'data such',
                      'this data',
                      'data with',
                      'data title',
                      'data which',
                      'data between']
    return(dataStockPhrases)

    
def otherWordRules(phrase):
    if "data" in phrase and "analy" in phrase:
        return("data analysis-all variations")
    elif "data" in phrase and "scien" in phrase:
        return("data science")
    else:
        return(phrase)

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
    time.sleep(.3)
    print("slept")
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
                          "data visualization", "matlab", "data mining", 
                          "excel", "vba", "visual basic", "artificial intelligence"]
    return(listOfRolesandSkills)

def allKeywords():
    #we look for skills that we're only interested in if we know the listing is a data listing
    listOfRoles=basicKeywords()
    listOfRoles=listOfRoles+ ["spark", "java"]
    return(listOfRoles)
    
def searchByKeywordList(authorization_key):
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

def main(directory):   
    #pulls from the API, cleans, pulls from the actual listings, looks for full keywords
    authorization_key=getLogin(directory)
    df=searchByKeywordList(authorization_key)
    dfClean=cleanInitialDF(df)
    dfSoup=pullTextSoup(dfClean)
    dfVars=cleanVarsInSoup(dfSoup)
    justSelect=moreCleaningText(dfVars)
    updateVars=[i for i in allKeywords() if i in justSelect.columns]
    justSelect['Sum of Keywords']=justSelect[updateVars].sum(axis=1)
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
    ax.set_title('Count of Data Listings With The Following Keyword: 6-25-2020')
    for i in range(len(keywords)):
        plt.annotate(str(list(dictKeysSort.values())[i]), xy=(list(dictKeysSort.values())[i],y_pos[i]))
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
       
def stockPhrasesDelete():
    stockPhrases=['unsaved data', 'data will','act data', 'data opens', 'https data', 'data usajobs', 'to excel', 'excel prepare']
    stockPhrasesAll=stockPhrases+dataStock()
    return(stockPhrasesAll)
    
def findNgrams(input_list, n):
  return(zip(*[input_list[m:] for m in range(n)]))   

def wordsNotWords():
    deleteStrings=["li", "n", "ul", "br", "r", "t"]
    return(deleteStrings)
def makeNgramsFromText(text, phrase, n):
    stockPhrases=stockPhrasesDelete()
    words = re.findall(r'[A-Za-z]+', text.lower())
    deleteStrings=wordsNotWords()
    cleanWords=[i for i in words if i not in deleteStrings]
    nGrams= findNgrams(cleanWords, n)
    counts = Counter(nGrams)
    selectNgrams=[" ".join(list(l[0])) for l in counts.most_common() if phrase in [l][0][0]]  
    remainingNgrams=[k for k in selectNgrams if k not in stockPhrases]
    otherWordRuleNGrams=list(set([otherWordRules(i) for i in remainingNgrams]))
    return( otherWordRuleNGrams)
    
    
def dictionaryOfGrams():
    dictOfGrams={1: "words", 2: "bigrams", 3: "trigrams"}
    return(dictOfGrams)
  
def textGrams(df, phrase, n):
    textGramOutput=pd.Series([makeNgramsFromText(i, phrase, n) for i in df['textSoup']])
    return(textGramOutput)

def keywordGraphDict(directory, outputData, thresshold, titleText):
    #count of keywords
    date=str(datetime.date(datetime.now()))
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(7,thresshold/4))
    dictKeysSort=dict(sorted(outputData.items(), key=operator.itemgetter(1), reverse=True)[:thresshold])
    y_pos = np.arange(len(dictKeysSort.keys()))
    ax.barh(y_pos, list(dictKeysSort.values()), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(dictKeysSort.keys()))
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count')
    ax.set_title(titleText)
    plt.tight_layout()
    for i in range(thresshold):
        plt.annotate(str(list(dictKeysSort.values())[i]), xy=(list(dictKeysSort.values())[i],y_pos[i]))
    plt.savefig(directory + f'\\results\\{titleText}_{date}.png')

def getTopNgrams(series):
    flat_list = [item for sublist in series for item in sublist]
    counts = Counter(flat_list)
    return(counts)

def basicDataPull(directory, JobCategoryCode, terms, phrase, n):
    authorization_key=getLogin(directory)
    df=current_search(authorization_key, JobCategoryCode=JobCategoryCode, terms=terms)
    dfSoup=pullTextSoup(df)
    ngramOutput=textGrams(dfSoup, phrase, n)
    counts=getTopNgrams(ngramOutput)
    blanks=len(ngramOutput[~ngramOutput.astype(bool).astype(bool)])
    print(f'{blanks} blanks and {len(df)} total listings')
    return(dfSoup, ngramOutput, counts)
    
    
inputs0301={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"0301",
               "terms":"",
               "phrase":"data",
               "n":2}

inputsExcel={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"",
               "terms":"excel",
               "phrase":"excel",
               "n":2}

inputsData={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"",
               "terms":"data",
               "phrase":"data",
               "n":2}

directory=r'C:\Users\HaddadAE\Git Repos\personnel'
"""
df0301Data, df0301ngram, df0301PhraseCounts=basicDataPull(**inputs0301)
keywordGraphDict(directory, df0301PhraseCounts, 10, "Top 10 Data Bigrams From 0301 Search")

ExcelData, Excelngram, ExcelPhraseCounts=basicDataPull(**inputsExcel)
keywordGraphDict(directory, ExcelPhraseCounts, 10, "Top 10 Excel Bigrams From All Army Search")
#keywordGraphDict(directory, dataPhraseCounts, 10)

dfDataScience=main(directory)
"""
def addAsk(i, aList):
    if i in aList:
        return("*"+i)
    else:
        return(i)
        
def allTheKeys(df):
    allKeywordsReturn=allKeywords() 
    allKeywordsReturn.sort()
    absentKeywords = [i for i in allKeywords() if i not in df.columns]
    fixedList=[addAsk(i, absentKeywords) for i in allKeywordsReturn]
    return(fixedList)

dataData, datangram, DataPhraseCounts=basicDataPull(**inputsData)
keywordGraphDict(directory,  DataPhraseCounts, 20, "Top 20 Data Bigrams From Army Civilian Listings: 6-25-2020")
allDataScienceKeys=main(directory)

allKeys=allTheKeys(allDataScienceKeys)
#New=[otherWordRules(i) for i in DataPhraseCounts.keys()]
#NewDict= dict(zip(New, DataPhraseCounts.values()))
#DataPhraseCounts=NewDict
#

#keywordGraphDict(directory, counts, 10)
#excelAds=pullExcel()
#excelPhrasesDF=excelPhrases(excelAds)

#flat_list = [item for sublist in excelPhrasesDF for item in sublist]
#counts = Counter(flat_list)
#keywordGraphDict(directory, counts, 10)

#flat_list = [item for sublist in excelPhrasesDF for item in sublist]
#counts = Counter(flat_list)

#words = re.findall(r'[A-Za-z]+', excelAds['textSoup'].iloc[0].lower())
#n = 3

#def find_ngrams(input_list, n):
#  return zip(*[input_list[i:] for i in range(n)])

#zipped=find_ngrams(words , 3)
#counts = Counter(zipped)



#
#outputData=main(directory)   
#metrics(directory, outputData)

#829 


#pull agency list
#from io import StringIO
#response = requests.get("https://data.usajobs.gov/api/codelist/agencysubelements")
#jdata = json.loads(response.content)
#agencyList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
#Army=agencyList.loc[agencyList['Value'].str.contains("Army")]


#pull occ list

#response = requests.get("https://data.usajobs.gov/api/codelist/occupationalseries")
#jdata = json.loads(response.content)
#OccList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
#Ops=OccList.loc[OccList['Value'].str.contains("Operations Research")]

