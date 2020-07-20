# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:37:50 2020

@author: HaddadAE
"""

import urllib.request
from bs4 import BeautifulSoup, Comment
import time
import pandas as pd

def listDataEngineerLinks():
    #from searching "data engineer" Position Duties/Exact Match https://acpol2.army.mil/fasclass/search_fs/
    dataEngineerLinks=["https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcxGuam0buidbYOak6tQgWC7hLBpZYCelqtGlLCzjLBWdMPa2q%2BEsK6zQNiel7fUxteSdYyWleeZlcGjxg%3D%3D",
                   "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcBGuam0buidbaG2k6JQgGx4iddtaYKWmKhXdX%2FIgd9tVpLb1etds5vGgZOVnrXPz9eFwWCkZOikmbPZntc%3D",
                   "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqVYiG6CY5mZlIuflKpTgW14ZemRnIuMpeeUyHe2geeRULPUyNuOtJ%2FERsV0pcLPxuVdtA%3D%3D"]
    return(dataEngineerLinks)
    
def listDataScientistLinks():
    #from searching "data scientist" Position Duties/Exact Match https://acpol2.army.mil/fasclass/search_fs/
    dataScientistLinks=["https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYOYlaZRiGeTRtyUbYeYmqRSg2CXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYOYlaZRiGC7hLBpYISamqVGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jtMZGuam0buidbYOYl6hYg2C7hLBpYX%2BWkqhGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqZQgGqFRtyUbYeakaRRf2CXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbYCnkqtQf2uLRtyUbYeXmqNQhmCXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOYlaVXhWC7hLBpYISalKNGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOYlaVXhWC7hLBpYISalKNGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jprxGuam0buidbYCnkqtQf2yCRtyUbYeXmqhQiGCXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOZmKdRhmC7hLBpY4OYmqhGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jprxGuam0buidbYCnkqtQf2uLRtyUbYeXmqhRf2CXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbYCnkqtQf2yCRtyUbYeXmqNXhGCXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqZQf3OJRtyUbYeakaNZgGCXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpbxGuam0buidbX%2BbladVf2C7hLBkZISXlKNGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOak6pShGC7hLBpZX%2BfkaZGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZi6p6NRhXF4iddtaIOdlKRRdX%2FIgd9tVpLb1etds5vGgZOjk7fLz%2BaJwq54crelpLfL1K%2BF",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOZmqlVf2C7hLBpY4edlqhGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOYmqVZhmC7hLBpYn6Wk6RGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZi6p6JUhW94iddtZ4efmahZdX%2FIgd9tVpLb1etds5vGgZOjk7fLz%2BaJwq54crelpLfL1K%2BF",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqVYiG6CY5mZlIuflKpTgW14ZemRnIuMpeeUyHe2geeRUMHJyteOw6PFlJmCdMPayteTjJ8%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOalKRRg2C7hLBpZYGakadGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYKelqpTf2C7hLBoZIWXlaNGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorZGuam0buidbX%2BbladVf2C7hLBpZIKakqdGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOXlaJXgmC7hLBoaYCWl6lGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo7hGuam0buidbYOWmKVTh2C7hLBoaICdlKVGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp75Guam0buidbYOYmalQiGC7hLBpYYeWkahGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOXkapUhWC7hLBoaIWYmaRGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq7ZGuam0buidbYOakqpQg2C7hLBpZISck6hGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq7ZGuam0buidbYOakqpQg2C7hLBpZISck6hGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOYlaVYf2C7hLBpYISalKhGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqZQf3OHRtyUbYeakaNYh2CXltScbXSq1uaZjJ6zlNRQo7HPxuCUuK3GRsV0pcLPxuVdtA%3D%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZKuoqNRhXF4iddtaX6YmapUdX%2FIgd9tVpLb1etds5vGgZOjk7fLz%2BaJwq54crelpLfL1K%2BF",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqZTgmyCY5mZlIuflqVXgHB4ZemRnIuMpeeUyHe2geeRUMHJyteOw6PFlJmCdMPayteTjJ8%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOalKRRh2C7hLBpZYGakqJGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOalKtVgGC7hLBpZYKel6ZGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D",
                    "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOalKRRgmC7hLBpZYGZmqRGlLCzjLBWdMPa2q%2BEsK6zQOaTmbPU1duTw2CkZOikmbPZntc%3D"]
    return(dataScientistLinks)
    
def pullActualListing(url):
    #pulls all html as text; pauses because otherwise the USAJobs site will break this 
    html = urllib.request.urlopen(url).read() 
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    time.sleep(.3)
    return u" ".join(t.strip() for t in visible_texts)

def tag_visible(element):
    #get visible parts of website
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return(False)
    if isinstance(element, Comment):
        return(False)
    return(True)
    
def getLinks():
    #combines links, drops dups
    dataEngineerLinks=listDataEngineerLinks()
    dataScientistLinks=listDataScientistLinks()
    overallSetLinks=list(set(dataEngineerLinks+dataScientistLinks))
    return(overallSetLinks)
    
def extractFields(soups):
    #gets specific fields based on text setup
    df=pd.DataFrame()
    df['Job title']=[soup.split("Replaces PD#:")[1].split("Opt")[0].split("Organization Title")[0] for soup in soups]
    df['PD #']=[soup.split("PD#:")[1].split("Sequence#:")[0] for soup in soups]
    df['Sequence #']=[soup.split("Sequence#")[1].split("Replaces PD#")[0] for soup in soups]
    df['Position Duties']=[soup.split("POSITION DUTIES:")[1].split("NOTICE TO SUPERVISORS:")[0] for soup in soups]
    df['POSITION EVALUATION']=[soup.split("POSITION EVALUATION:")[1].split("***Final classification based")[0] for soup in soups]
    for col in df.columns:
        df[col]=df[col].str.strip()
    return(df)
                          
def pullFromLinks(links):
    #given links, gets text and extract fields
    soups=[pullActualListing(url) for url in links]
    df=extractFields(soups)
    return(df)
    
def main():
    #calls functions with list of links, returns DF with full text and extracted fields
    links=getLinks()
    df=pullFromLinks(links)
    return(df)

df=main()
