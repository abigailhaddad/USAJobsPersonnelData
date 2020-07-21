# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:37:50 2020
This pulls data scientist and data engineer and data analyst listings from FASCLASS

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
    
def listDataAnalystLinks():
    #from searching "data analyst" Position Duties/Exact Match https://acpol2.army.mil/fasclass/search_fs/
    dataAnalystLinks=["https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorZGuam0buidbYOWl6hYhmC7hLBpZIOalqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorZGuam0buidbYOZmatThWC7hLBpZIWdkahGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYKflaJTgWC7hLBoZYacmaZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOYk6hWiGC7hLBpYICcmKhGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbYOZlatVgGC7hLBpYoadk6ZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jorlGuam0buidbaaeorlUiG6CU6VWmbKjmqZRgGyKRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2josVGuam0buidbYGdk6dViGC7hLBnYYKalqhGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2josVGuam0buidbYOXlqZYhGC7hLBoaYGdmqdGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo7RGuam0buidbYGZmqtVgmC7hLBmZYSZmqtGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo7RGuam0buidbYOZkatQg2C7hLBpYoCWmaNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo7RGuam0buidbYOZl6lQiGC7hLBpY4CekqJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo7RGuam0buidbYOalKJRgWC7hLBpZYCfl6VGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOWl6dTh2C7hLBoZ4KZk6hGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOWl6hYhmC7hLBoZ4KbkqhGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOWl6hZiGC7hLBoZ4Kbk6tGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOWmaVTg2C7hLBoaIGflapGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOZmKpVgmC7hLBpY4OelapGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOZmKpVhGC7hLBpY4OelqJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOZmKpVhmC7hLBpY4OelqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo71Guam0buidbYOZmatThWC7hLBpY4aZkqpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo8RGuam0buidbYCcl6ZVhmC7hLBlZ4GYmaZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo8RGuam0buidbYKdlaJVhWC7hLBoY4Cck6NGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo8RGuam0buidbYOWmqtVgGC7hLBoaISWl6tGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jo8RGuam0buidbYedkqNZdaO2XapoYIOfh7eWsKaPRrelpMejxdOUsFqzjtScqcHah8RkxK67heZtlQ%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqNWh3CHRtyUbYaflqZThmCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZKslqZQgG6JRtyUbYeakaRWgWCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZSzlalVg3CKRtyUbYaZlaNZf2CXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpLlGuam0buidbZaulapUgGuHRtyUbYaalqNQhWCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpadGuam0buidbX%2BWk6ZWgmC7hLBoaICbl6lGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpbxGuam0buidbYOXl6RRh2C7hLBoaYKclaJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYGamKRYhWC7hLBmZoSYlKJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOYmqZVgmC7hLBpYn6WmaZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOak6lXhGC7hLBpZX%2BelKVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOalqNYhGC7hLBpZYaYmKRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOalqRQgWC7hLBpZYaYmqdGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOalqdYh2C7hLBpZn%2BdkqpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpb9Guam0buidbYOalqdZf2C7hLBpZn%2Bdk6RGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcBGuam0buidbYKXl6RXhWC7hLBnZYeWlqpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpclGuam0buidbYGZmapThGC7hLBmZYOXmaVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpclGuam0buidbaGWkqlTdaO2XaRnZn%2BckZhlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcxGuam0buidbYGbkqRWhmC7hLBmZ36emqlGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcxGuam0buidbYKXmKtUhmC7hLBnZn%2BZl6ZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpcxGuam0buidbYOak6hWhmC7hLBpZX%2BclapGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jprNGuam0buidbYKekqVWhGC7hLBoZH%2BZkatGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jprNGuam0buidbYKflKpYhmC7hLBoZYabkqNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jprlGuam0buidbYCZladXiGC7hLBlY4ebl6tGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpr9Guam0buidbYGdlatRhWC7hLBmaYeYlKpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpr9Guam0buidbYOXmKdUgWC7hLBoaYSYlKtGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpsNGuam0buidbYKdlqJYg2C7hLBoY4Gdl6RGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpsRGuam0buidbYOalaNXhGC7hLBpZYOXmqhGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpsZGuam0buidbX%2BWl6JVdaO2XaRgZ4OckphlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpsdGuam0buidbYGXl6lSiGC7hLBmYoeemaRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpshGuam0buidbYKckqhZgmC7hLBoYYaalKJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpshGuam0buidbYOWl6JYhGC7hLBoZ4GdlqZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpspGuam0buidbYGamahThmC7hLBmZoWdkqdGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpspGuam0buidbYKZmalZgGC7hLBnaIeel6JGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jpstGuam0buidbYKbmalTh2C7hLBoYYKck6RGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp7ZGuam0buidbX%2BZlapWg2C7hLBkYYObmqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp7ZGuam0buidbX%2BZlapWhWC7hLBkYYObmqZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp7ZGuam0buidbX%2BZlapWhmC7hLBkYYObmqdGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp71Guam0buidbX%2BZlapWg2C7hLBoZoKWmqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYGemqRYhmC7hLBnYoCcmqlGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYGfkapTgWC7hLBnYoSZkaVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYGflaZZhGC7hLBnY3%2BXlqNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYKWlaZQgmC7hLBnZIGelqVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYKZlqRWhGC7hLBnaIOWk6lGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbYKZmKZRhGC7hLBnaIWbk6hGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbZCnqrpRiGqCUKhWmbKjmqNXg26JRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbZeukqZQf2yJRtyUbYaWlKZZgWCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbZeukqpQf2uFRtyUbYaeladRgGCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jp8RGuam0buidbZeukqtQf2qHRtyUbYeWkaZQgGCXltScbXSq1uaZjJ6zlNRQkbzHzeuTw2CkZOikmbPZntc%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqLxGuam0buidbYKZlKZVhI14iddtaIWWmadSdX%2FIgd9tVpLb1etds5vGgZORnq%2FS2uWUdYyWleeZlcGjxg%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqLxGuam0buidbYKdlqhXf2C7hLBoY4KZmqhGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqMhGuam0buidbYKel6VTiGC7hLBoZIWdmalGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqapGuam0buidbYOWlahXhWC7hLBoZ3%2BfmalGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqapGuam0buidbYOZl6hQgWC7hLBpY4CblaJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqbRGuam0buidbYOYlqhUhmC7hLBpYIafkqpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqbdGuam0buidbYKdkalXhGC7hLBoYoafkaVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqbtGuam0buidbYKYlKhRhGC7hLBnZoealqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcRGuam0buidbY%2Bss6pQgmC7hLBnYYeelqNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYGdmqpVhWC7hLBnYISdkqRGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYGel6VYhGC7hLBnYYWYlKZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYKblaNWhGC7hLBoYIeakaZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOYkqJVg2C7hLBpYH6ckaJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOYkqJVg2C7hLBpYH6ckaJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcZGuam0buidbYOZl6NRgWC7hLBpY36WmatGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbX6YmatTdaO2XaZpYYSbmZhlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYCZmKZWg2C7hLBlZICdkqJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYGflKtTgmC7hLBnY36blKlGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYKdl6hVhGC7hLBoY4OcmKJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYOZkalYh2C7hLBpYn%2BflKNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYOZk6RXgGC7hLBpYoKakqJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jqcdGuam0buidbYesmKtmdaO2XadgY4admphlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq7xGuam0buidbYOYlqJQhWC7hLBpYIWckaZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbW6WkqNXgmC7hLBpY36amqdGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbYKcmaZRg2C7hLBpY3%2BYmapGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbYKfmKtViGC7hLBpY3%2BcmqtGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZi6p6JXg214iddtZ4GYmKpSdX%2FIgd9tVpLb1etds5vGgZORnq%2FS2uWUdYyWleeZlcGjxg%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZi6p6NQhmt4iddtZ4adlaZUdX%2FIgd9tVpLb1etds5vGgZORnq%2FS2uWUdYyWleeZlcGjxg%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jq8ZGuam0buidbZi6p6dRf2p4iddtaH6ZmKdQdX%2FIgd9tVpLb1etds5vGgZORnq%2FS2uWUdYyWleeZlcGjxg%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbX6XkqtVdaO2XaxjYX6WmJhlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbX6XladVdaO2XaxjYIScl5hlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYCak6RZf2C7hLBpY4aclalGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYGZkadQdaO2XaxjYX6XlJhlxZu%2BXZl0pcLfntaBw5tygeGRnMfZ1Zhyk6%2FGidijbbM%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYGfmKRUhWC7hLBpY4CYkaVGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYKZlaJXhGC7hLBpY3%2BdlKNGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYKZmKZRhGC7hLBpY4OdkahGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYKelqlShmC7hLBpY3%2Bal6JGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOWmaVUiGC7hLBpY3%2BdlqlGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOXlapXgWC7hLBpY3%2BflKJGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOXlqZTiGC7hLBpY3%2BflKpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOakahWgmC7hLBpZH6fk6pGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOalqRYgmC7hLBpZYaakatGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOalqVRh2C7hLBpZYaalqpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbYOalqpQh2C7hLBpZoCWk6tGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jrLhGuam0buidbaCXlKlQf2C7hLBpY4ablKpGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbZCnqrpRg2qCUqpWmbKjmqJVgGqFRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbZCnqrpRh2qCUaZWmbKjmqJUh3KKRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbZCnqrpRiGqCUKhWmbKjmqJUh3KCRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jsbZGuam0buidbaaeorlUiG6CU6VWmbKjmqZQiG2JRrimkbqjh7aVw7OPhNSkkW7Hz9OMyK3GRsV0pcLPxuVdtA%3D%3D",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jtMZGuam0buidbX%2BfkaRSgGC7hLBkaH6clKZGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jtMZGuam0buidbYKckatZh2C7hLBoYYWbl6VGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL",
                      "https://acpol2.army.mil/fasclass/search_fs/search_fs_output.asp?fcp=zutpk3eFRtaToL2jtMZGuam0buidbYKflKtQgGC7hLBoZYabk6dGlLCzjLBWdMPa2q%2BEsK6zQNSekbrf1OZGoX7HlNyVo4vL"]
    return(dataAnalystLinks)
    
    
def pullActualListing(url):
    #pulls all html as text; pauses because otherwise the USAJobs site will break this 
    html = urllib.request.urlopen(url).read() 
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    time.sleep(.05)
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
    dataAnalystLinks=listDataAnalystLinks()
    overallSetLinks=list(set(dataEngineerLinks+dataScientistLinks+dataAnalystLinks))
    return(overallSetLinks)
    
def replace(str1, str2):
    #deletes str2 in str1 with ""
    return str1.replace(str2, '')

def cleanTitleMore(string):
    #cleans the title field
    if "   " in string:
        string=(string.split("   ")[-2]+ string.split("   ")[-1])
    if "-" in string:
        string=string.split("-")[0]
        string=" ".join(string.split(" ")[0:-1])
        return(string)
        
def extractFields(soups):
    #gets specific fields based on text setup
    df=pd.DataFrame()
    df['Job title']=[soup.split("Replaces PD#:")[1].split("Opt")[0].split("Organization Title")[0] for soup in soups]
    df['PD #']=[soup.split("PD#:")[1].split("Sequence#:")[0] for soup in soups]
    df['Sequence #']=[soup.split("Sequence#")[1].split("Replaces PD#")[0] for soup in soups]
    df['Position Duties']=[soup.split("POSITION DUTIES:")[1].split("NOTICE TO SUPERVISORS:")[0] for soup in soups]
    df['POSITION EVALUATION']=[soup.split("POSITION EVALUATION:")[1].split("***Final classification based")[0] for soup in soups]
    df['Job title']=df.apply(lambda row: replace(row['Job title'], row['PD #']), axis=1)
    df['Job title']=df['Job title'].apply(cleanTitleMore)
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
df.to_excel("Data Scientist and Engineer PDs.xlsx")