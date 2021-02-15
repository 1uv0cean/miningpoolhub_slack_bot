import requests
import re
import pyupbit
import pprint
from slacker import Slacker
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
#매일 09시마다 실행
@sched.scheduled_job('cron', hour='09', minute='00', id='test_1')
def exec_cron():
    
    url = "https://api.upbit.com/v1/market/all"
    resp = requests.get(url)
    data = resp.json() #json
    eth_balance=float(pyupbit.get_current_price("KRW-ETH")) #Upbit에서 Ethereum 원화 시세를 가져옴

    api_key = "miningpoolhub API key" #miningpoolhub API키
    tail = "&api_key="+str(api_key)
    header = "https://ethereum.miningpoolhub.com/index.php?page=api&action="

    def get_data(apiname):
        result = requests.get(header+apiname+tail)
        return result.text
 
    balance =get_data("getuserbalance").split(",")
    balance = float(balance[2].split(":")[2])
    bal=str(round(eth_balance*balance,2))+"원"
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + bal

    slack = Slacker('슬랙봇 OAuth Token') # slack 인증코드
    slack.chat.post_message('#eth-mining',strbuf)


# 스케줄링 시작
sched.start()
