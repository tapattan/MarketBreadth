import requests
from enum import Enum
import pandas as pd

__headers__ = {
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.set.or.th/th/market/product/stock/quote/dusit/factsheet',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# class syntax
class indexType(Enum):
    set50 = 'set50'
    set50ff = 'set50ff'
    set100 = 'set100'
    set100ff = 'set100ff'
    setesg = 'setesg'
    sethd = 'sethd'
    sSET = 'sset'
    setwd = 'setwb'
    setclmv = 'setclmv'
    set_index = 'set_index'

def get_member_of_index(indexType):
    params = {
        'lang': 'th'
    }
    session = requests.Session()
    session.get(f"https://www.set.or.th/th/market/product/stock/quote/dusit/factsheet")
    
    if(indexType.value=='set_index'):
      url = f'https://www.set.or.th/api/set/stock/list'  
    else:
      url = f'https://www.set.or.th/api/set/index/{indexType.value}/composition?lang=th'

    

        
    response = session.get(
        #'https://www.set.or.th/api/set/factsheet/dusit/financialstatement',
        url,
        #'https://www.set.or.th/api/set/factsheet/dusit/financialstatement',
        params=params,
        headers=__headers__)

    response.raise_for_status()
    data = response.json()

    #df= pd.DataFrame(data['majorShareholders'],columns=['name','numberOfShare','percentOfShare'])
    #df['name'] = df['name'].str.replace('  ',' ') 
    
    if(indexType.value=='set_index'):
      df = pd.DataFrame(data['securitySymbols'])   
    else:
      df = pd.DataFrame(data['composition']['stockInfos'])
    #df = df[['symbol','buyVolume','sellVolume','totalVolume','netVolume']]
    return df