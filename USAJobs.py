# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 07:27:10 2020
This pulls from the USAJobs API and then scrapes the web pages for additional text to look for 
data science/data engineering-related keywords, as well as more general 

An earlier verion was as of 6/26/2020, which was used for:
    USAJobs Army Civilian Job Listings and Mentions of Data and Data Skills 

This version is as of 7/2/2020, which adds the 0301 graph addition. There are also some minor code changes
    the most significant of this is that you can search for multiple words (like 'excel' and 'data' in ngrams to be shown on the chart)
@author: HaddadAE
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re
import operator
import time
import json
import urllib.request
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup, Comment


plt.rcParams["font.family"] = "Times New Roman"

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
                      'data between',
                      "submit data",
                      "related data",
                      "data submit",
                      "a data"]
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
    #dfArmy=df_fixed.loc[df_fixed['DepartmentName']=="Department of the Army"]
    #return(dfArmy)
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
    #pulls all html as text; pauses because otherwise the USAJobs site will break this 
    html = urllib.request.urlopen(url).read() 
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    time.sleep(.3)
    return u" ".join(t.strip() for t in visible_texts)

    
    

def tag_visible(element):
    #thank you stackexchange
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return(False)
    if isinstance(element, Comment):
        return(False)
    return(True)

def pullResponsibilities(string):
    try:
        #return(re.search('Responsibilities(.*)Travel Required', string).group(1))
        return(string.split("Responsibilities")[1].split("Travel Required")[0])
    except:
        return()
    
def pullQualifications(string):
    try:
        return( re.search('Who May Apply(.*)Background checks and security clearance', string).group(1))
    except:
        return()
        
def pullTextSoup(df):
    #calls pullActualListing on whole series of URLs
    df['textSoup']=df['PositionURI'].apply(pullActualListing)
    df['responsibilities']=df['textSoup'].apply(pullResponsibilities)
    df['qualifications']=df['textSoup'].apply(pullQualifications)
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
    #this drops blank rows (with no keywords)
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
    #pulls all phrases to drop
    stockPhrases=['unsaved data', 'data will','act data', 'data opens', 'https data', 'data usajobs', 'to excel', 'excel prepare']
    stockPhrasesAll=stockPhrases+dataStock()
    return(stockPhrasesAll)
    
def findNgrams(input_list, n):
    #converts list of word to list of ngrams of length n
  return(zip(*[input_list[m:] for m in range(n)]))   

def wordsNotWords():
    #contains strings that are typically html tags not words
    deleteStrings=["li", "n", "ul", "br", "r", "t"]
    return(deleteStrings)
    
def makeNgramsFromText(text, phrase, n):
    #gets relevant ngrams of n length from text
    stockPhrases=stockPhrasesDelete()
    words = re.findall(r'[A-Za-z]+', text.lower())
    deleteStrings=wordsNotWords()
    cleanWords=[i for i in words if i not in deleteStrings]
    nGrams= findNgrams(cleanWords, n)
    counts = Counter(nGrams)
    if len(phrase)>0:
        selectNgrams=[" ".join(list(l[0])) for l in counts.most_common() if any(item in [l][0][0] for item in phrase)]  
    else:
        selectNgrams=[" ".join(list(l[0])) for l in counts.most_common()]  
    remainingNgrams=[k for k in selectNgrams if k not in stockPhrases]
    otherWordRuleNGrams=list(set([otherWordRules(i) for i in remainingNgrams]))
    return( otherWordRuleNGrams)

        
    
    
def dictionaryOfGrams():
    #might use this later as chart title input
    dictOfGrams={1: "words", 2: "bigrams", 3: "trigrams"}
    return(dictOfGrams)
  
def textGrams(df, col, phrase, n):
    #gets series of all relevant phrases of length n with word "phrase" in them from df column 'textSoup'
    textGramOutput=pd.Series([makeNgramsFromText(i, phrase, n) for i in df[col]])
    return(textGramOutput)

def keywordGraphDict(outputData, directory, JobCategoryCode, terms, phrase, n, ngramNumber, chartTitle):
    #this takes the full df, thresshold for the top n words/phrases, and the title to show and outputs a chart
    date=str(datetime.date(datetime.now()))
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(7,ngramNumber/4))
    dictKeysSort=dict(sorted(outputData.items(), key=operator.itemgetter(1), reverse=True)[:ngramNumber])
    y_pos = np.arange(len(dictKeysSort.keys()))
    ax.barh(y_pos, list(dictKeysSort.values()), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(dictKeysSort.keys()))
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count')
    ax.set_title(chartTitle)
    plt.tight_layout()
    for i in range(ngramNumber):
        plt.annotate(str(list(dictKeysSort.values())[i]), xy=(list(dictKeysSort.values())[i],y_pos[i]))
    plt.savefig(directory + f'\\results\\{chartTitle}_{date}.png')

def getTopNgrams(series):
    #takes list of lists of phrases, flattens, gets counts of each
    flat_list = [item for sublist in series for item in sublist]
    counts = Counter(flat_list)
    return(counts)

def basicDataPull(directory, JobCategoryCode, terms, phrase, n, ngramNumber, chartTitle):
    #this does a data pull from usajobs and gets both data from the API and scrapes the pages
    authorization_key=getLogin(directory)
    df=current_search(authorization_key, JobCategoryCode=JobCategoryCode, terms=terms)
    dfSoup=pullTextSoup(df)
    ngramOutput=textGrams(dfSoup, 'textSoup', phrase, n)
    counts=getTopNgrams(ngramOutput)
    blanks=len(ngramOutput[~ngramOutput.astype(bool).astype(bool)])
    print(f'{blanks} blanks and {len(df)} total listings')
    return(dfSoup, ngramOutput, counts)
    
def pullArmyAgencyList():
    #pull agency list from the API
    response = requests.get("https://data.usajobs.gov/api/codelist/agencysubelements")
    jdata = json.loads(response.content)
    agencyList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
    Army=agencyList.loc[agencyList['Value'].str.contains("Army")]
    return(Army)

def pullOccList():
    #pulls occ list from the API
    response = requests.get("https://data.usajobs.gov/api/codelist/occupationalseries")
    jdata = json.loads(response.content)
    OccList=pd.DataFrame.from_dict(jdata['CodeList'][0]['ValidValue'])
    return(OccList)
    
def addAsk(i, aList):
    #this takes a string and compares it to a list and if it's not  on the list appends *
    if i in aList:
        return("*"+i)
    else:
        return(i)
        
def allTheKeys(df):
    #this takes a DF and looks for columns that are also in the list of keywords, and returns for Appendix B
    allKeywordsReturn=allKeywords() 
    allKeywordsReturn.sort()
    absentKeywords = [i for i in allKeywords() if i not in df.columns]
    fixedList=[addAsk(i, absentKeywords) for i in allKeywordsReturn]
    return(fixedList)

def produceDataBigrams(**inputsData):
    #this gets all the "data" postings and cleans them for the first chart
    dataData, datangram, DataPhraseCounts=basicDataPull(**inputsData)
    keywordGraphDict(DataPhraseCounts, **inputsData)
    return(dataData, datangram, DataPhraseCounts)
    
def produceDataKeywords(directory):
    #this gets all the "data science/engineering/excel postings for the second chart
    allDataScienceKeys=main(directory)
    return(allDataScienceKeys)
    
def produceListOfKeywords(df):
    #this produces the list of keywords for appendix B, including which ones were found
    listOfKeywords=allTheKeys(df)
    return(listOfKeywords)


def paperFirstDraft():
    inputsData={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"",
               "terms":"data",
               "phrase":["data"],
               "n":2,
               "ngramNumber": 20,
               "chartTitle": "Top 20 Data Bigrams from Army Civilian Listings"}
    
    directory=r'C:\Users\HaddadAE\Git Repos\personnel'
    dataData, datangram, DataPhraseCounts=produceDataBigrams(**inputsData)
    allDataScienceKeys=produceDataKeywords(directory)
    keywordGraph(directory, allDataScienceKeys)
    keywords=produceListOfKeywords(allDataScienceKeys)
    print(keywords)
    
def paper0301Addition():
    Data301={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"0301",
               "terms":"",
               "phrase":["data", "excel"],
               "n":2,
               "ngramNumber": 20,
               "chartTitle": "Top 20 Data Bigrams from Army 0301 Civilian Listings: 7-2-2020"}
    
    results301, ngram301, DataPhraseCounts301=produceDataBigrams(**Data301)
    print(len(results301))
     
    
def differentExperiment():
    dataORSA={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"1515"}
    authorization_key=getLogin(dataORSA['directory'])
    df=current_search(authorization_key, JobCategoryCode=dataORSA['JobCategoryCode'])
    dfSoup=pullTextSoup(df)
    return(dfSoup)


def getAllGrams(text, n):
    stockPhrases=stockPhrasesDelete()
    words = re.findall(r'[A-Za-z]+', text.lower())
    deleteStrings=wordsNotWords()
    cleanWords=[i for i in words if i not in deleteStrings]
    nGrams= findNgrams(cleanWords, n)
    counts = Counter(nGrams)
    selectNgrams=[" ".join(list(l[0])) for l in counts.most_common()]  
    remainingNgrams=[k for k in selectNgrams if k not in stockPhrases]
    otherWordRuleNGrams=list(set([otherWordRules(i) for i in remainingNgrams]))
    return( otherWordRuleNGrams)
    
def allTextGrams(df,  n):
    #gets series of all relevant phrases of length n with word "phrase" in them from df column 'textSoup'
    textGramOutput=pd.Series([getAllGrams(i, n) for i in df['textSoup']])
    return(textGramOutput)



def worldCloud(freqDict, title):
    wordcloud = WordCloud(width=1600, height=800, background_color='white', colormap='summer')
    wordcloud.generate_from_frequencies(frequencies=freqDict)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wordcloud.to_file(title+".png")
    
def exceptIn(dict1, dict2):
    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    dict1Except=[i for i in dict1.keys() if i not in dict2.keys()]
    newDict=dictfilt(dict1, dict1Except)
    return(newDict)
    
def controlGroup():
    control={"directory":r'C:\Users\HaddadAE\Git Repos\personnel', 
               "JobCategoryCode":"0081;0185;0640;0950;1035;1152;1601;1910;2003;2161;2604;5048",         
               "terms":"",
               "phrase":[],
               "n":1,
               "ngramNumber": 20,
               "chartTitle": "Top 20 Control Bigrams"}
    
    resultsControl, ngramControl, phraseCountscontrol=basicDataPull(**control)
    return(resultsControl, ngramControl, phraseCountscontrol)
    
def makeWordCloud(df, column, phrase, gramNum, totalNum, title, exclusions=[]):
    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    ngramOutput=textGrams(df, column, phrase,gramNum)
    counts=getTopNgrams(ngramOutput)
    dict1Except=[i for i in counts.keys() if i not in STOPWORDS and i not in exclusions]
    newDict=dictfilt(counts, dict1Except)
    dictKeysSort={k: v for k, v in sorted(newDict.items(), key=lambda item: item[1], reverse=True)[:totalNum]}
    worldCloud(dictKeysSort, title)
"""
paper0301Addition()
paperFirstDraft()
orsas=differentExperiment()
resultsControl, ngramControl, phraseCountscontrol=controlGroup()


makeWordCloud(orsas, 'responsibilities', "", 1, 100, "100 ORSA Responsibily Phrases")
makeWordCloud(orsas, 'qualifications', "", 1, 100, "100 ORSA Qualifications Phrases",  phraseCountscontrol.keys())
"""