import json
import heapq
import requests
from datetime import datetime

def get_analysis(ticker,ticker_range):
    res={}
    for ticker in ticker.split(','):
        url='https://query1.finance.yahoo.com/v7/finance/chart/{}?range={}&interval=1d&indicators=quote&includeTimestamps=true'.format(ticker,ticker_range)
        data=requests.get(url,headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
        data=data.text
        res_json=json.loads(data)
        adjclose=res_json['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        timestamp=res_json['chart']['result'][0]['timestamp']

        #calculate top 5 days
        move=[]
        abs_move=[]
        #print(type(adjclose))
        for i in range(len(adjclose)):
            if i ==0:
                move.append(0)
                abs_move.append(0)
            else:
                m=(adjclose[i]/adjclose[i-1]-1)*100
                move.append(m)
                abs_move.append(abs(m))

        move_max_index=list(map(abs_move.index,heapq.nlargest(5,abs_move)))
        #print(move_max_index)
        #print(abs_move)
        res_output=[]
        for i in move_max_index:
            res_output.append({'date':datetime.fromtimestamp(timestamp[i]).date().strftime('%Y-%m-%d'),'move:':move[i]})

        res[ticker]=res_output
    return res

 
    
get_analysis('MSFT,F,CMG','3mo')


