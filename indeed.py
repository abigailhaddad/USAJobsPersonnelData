# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:58:57 2020

@author: HaddadAE
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from bs4.element import Comment


def getLinks(soup):
    linkList=[]
    for link in soup.find_all('a', href=True):
        link=link['href']
        if "clk?jk" in link:
            linkList.append(link)
    return(linkList)

def searchPhrase(phrase):
    #site=f'https://www.indeed.com/jobs?as_and&as_phr=%22data%20science%22&as_any&as_not&as_ttl=Army&as_cmp&jt=all&st&as_src&salary&radius=25&l&fromage=any&limit=10&sort&psf=advsrch&from=advancedsearch&vjk=d5f711c261371e64'
    site=f'https://www.indeed.com/jobs?as_and={phrase}&as_phr=&as_any=&as_not=&as_ttl=Army&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch'
    soup=makeRequest(site)
    linkLists=getLinks(soup)
    return(linkLists)
    
def makeRequest(site):
    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    resp = urllib.request.urlopen(site)
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    return(soup)
    
def allWithPhrase(phrase):
    print(phrase)
    linkLists=searchPhrase(phrase)
    firstPart=r'https://www.indeed.com'
    fullLinks=[firstPart+i for i in  linkLists]
    #fullSoup=[makeRequest(i) for i in fullLinks]
    #print(fullLinks)
    #fullText=[text_from_html(urllib.request.urlopen(i).read()) for i in fullLinks]
    return(fullLinks)
    
def getSoups(fullLinks):
    fullSoup=[makeRequest(i) for i in fullLinks]
    return(fullSoup)
    
def getText(link):
    print(link)
    htmls = [urllib.request.urlopen(i).read() for i in link]
    texts=[text_from_html(html) for html in htmls]
    return(texts)
    
def doAllPhrases(keywords):
    cleanPhrases=[i.replace(" ", "+") for i in keywords]
    print("cleaned")
    allTheLinks=[allWithPhrase(i) for i in cleanPhrases]
    allTheSoups=[getSoups(i) for i in allTheLinks]
    allTheTexts=[getText(i) for i in allTheLinks]
    print("allT")
    flat_list = [item for sublist in allTheSoups for item in sublist]
    print("flat_list")
    flat_list_text=[item for sublist in  allTheTexts for item in sublist]
    return(flat_list_text, flat_list)
#will import this later

def getTitle(soupBowl):
    try:
        return(soupBowl.title.string)
    except:
        return()
        
def getOrg(soupBowl):
    try:
        return(soupBowl.find('b',text='Organization'))
    except:
        return()
    
def findOrg(soup):
    try:
        listPhrases=(soup.text).split(r'"')
        org=[i for i in listPhrases if "Get job updates from" in i][0]
        cleanOrg=org.replace("Get job updates from ", "")
        return(cleanOrg)
    except:
        return("")
    
def takeSoupMakeDF(soups, texts):
    titles=[getTitle(i) for i in soups]
    orgs=[findOrg(i) for i in soups]
    soupText=[i.text for i in soups]
    df= pd.DataFrame(list(zip(titles, orgs, texts, soupText)), 
               columns =['Job Title', 'Employer', 'textSoup', 'all text']) 
    return(df)
    
    
def tag_visible(element):
    #thank you stackexchange
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    #thank you stackexchange
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

keywords=allKeywords()    
#allText, allSoup=doAllPhrases(keywords)

df=takeSoupMakeDF(allSoup, allText)
dfDeduped=df.drop_duplicates(subset="textSoup")

dfTest=cleanVarsInSoup(dfDeduped)
justSelect=moreCleaningText(dfTest)
updateVars=[i for i in allKeywords() if i in justSelect.columns]
justSelect['Sum of Keywords']=justSelect[updateVars].sum(axis=1)

keywordGraph(directory, justSelect)


topValue=dfTest['Job Title'].value_counts().head(1).index[0]
dfTest.loc[dfTest['Job Title']==topValue]