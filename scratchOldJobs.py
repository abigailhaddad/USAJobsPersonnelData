# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 12:32:50 2023

@author: abiga
"""

"""
df=pullFieldsFromDict(df)

pythons=df.loc[df['MajorDuties'].astype(str).str.contains("Python")]
rs=df.loc[df['MajorDuties'].astype(str).str.contains("R,")] #nope!

# dealing with this later
def historical():
    base_url="https://data.usajobs.gov/api/historicjoa?PositionSeries=2210&HiringDepartmentCodes=AR"
    results = requests.get(base_url, headers=connect(authorization_key)).json()
    df=pd.DataFrame.from_dict(results['data'])
    # and we're back to --- have to scrape to get historical info if we want it
'https://data.usajobs.gov/api/historicjoa?PageSize=10&PageNumber=2&PositionSeries=2210&StartPositionOpenDate=10-01-2015&EndPositionOpenDate=09-30-2016'
"""