# 抓取 cf 比賽的資料

import os 
import requests 
str1 = 'https://codeforces.com/api/contest.standings?contestId='
str2 = '&from=1&count=15&participantTypes=CONTESTANT'
for i in range (101,2001):
    print(i)
    file_path = './cf-data/round'+(str)(i)+'.json'
    with open(file_path, 'w') as file_name:
        url = str1 + (str)(i) + str2 
        file = requests.get(url)
        #print(file.text)
        try:
            file_name.write(file.text)
        except:
            continue 
            