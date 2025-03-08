# This example requires the 'message_content' privileged intent to function.
import random
import discord
import time
import random
import asyncio
import random
from openai import OpenAI
import requests
# 記得key不要洩漏出去
api_key = 'api_key'
openai_client = OpenAI(api_key = api_key)
token = 'discord_token'

class MyClient(discord.Client):
    async def check_time(self):
        while True:
            await asyncio.sleep(60)
            now = time.localtime()
            print(now)
            
    async def hand(self):
        while True:
            s = input()
            if s == "send":
                a = input()
                a = int(a)
                b = input()
                channel = discord.utils.get(client.get_all_channels(), id = a)
                channel.send(b)

            print("reset")

    async def on_ready(self):
        global channel1 
        global channel2
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await self.check_time()

    async def on_message(self, message: discord.Message):
        print(message.content)
        # we do not want the bot to reply to itself
        if message.guild.id == 949332399416811680:
            return
        if message.author.id == self.user.id:
            return
        if message.content.startswith('$send'):
            
            mes = message.content
            tmp = mes.split()
            await message.delete()
            await message.channel.send(tmp[1])
        if message.content.startswith('$ask'):
            mes = message.content
            tmp = mes[5:]
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "assistant", "content": "回答這個問題，不要超過 1000 個字元"},
                    {"role": "user", "content": tmp}
                ]
            )
            print(completion.choices[0].message)
            await message.channel.send(completion.choices[0].message.content)
        if message.content.startswith('$generate'):
            mes = message.content
            tmp = mes[9:]
            my_messages = [
                {"role": "assistant", "content": "generate a competitive programming problem, do not exceed 1500 characters."},
                {"role": "user", "content": tmp}
            ]
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages = my_messages
            )
            print(completion.choices[0].message.content)
            await message.channel.send(completion.choices[0].message.content)
            my_messages.clear
            my_messages.append({"role": "user", "content": 'solve this problem generate by you with code, do not exceed 1500 characters. '})
            my_messages.append({"role": "user", "content": completion.choices[0].message.content})
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages = my_messages
            )
            print(completion.choices[0].message)
            await message.channel.send(completion.choices[0].message.content)
            print(my_messages)
        if message.content.startswith('$problem'):
            mes = message.content
            tmp = mes.split()
            print(tmp)
            str1 = 'https://codeforces.com/api/problemset.problems?tags='
            str2 = ''
            url = str1 + (tmp[1]) + str2  
            file = requests.get(url).json()
            length = len(file['result']['problems'])
            if length == 0:
                await message.channel.send('tags not found')
                return 
            #print(file['result']['problems'][random.randint(1, length+1)])
            str3 = 'https://codeforces.com/contest/'
            str4 = '/problem/'
            rnd = 0
            while(True):
                rnd = random.randint(0, length)
                ptr = 0
                try:
                    ptr = file['result']['problems'][rnd]['rating']
                except:
                    ptr = 0
                print(tmp[2])
                print(ptr)
                if((int)(ptr) == (int)(tmp[2])):
                    break
            round = str(file['result']['problems'][rnd]['contestId'])
            mes1 = str3+round+str4+file['result']['problems'][rnd]['index']+'\n('
            flag = 0
            for tags in file['result']['problems'][rnd]['tags']:
                if flag == 1:
                    mes1 += ', '
                mes1 += tags
                flag = 1
            mes1+=', '
            mes1+=(str)(file['result']['problems'][rnd]['rating'])
            mes1+=')'
            await message.channel.send(mes1)
        if message.content.startswith('$analysis'):
            mes = message.content
            tmp = mes.split()
            print(tmp)
            str1 = 'https://codeforces.com/api/contest.standings?contestId='
            str2 = '&from=1&count=5&participantTypes=CONTESTANT&handles='
            url = str1 + (tmp[2]) + str2 + tmp[1]
            file = requests.get(url) 
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "assistant", "content": "Analysis this scoreboard of Codeforces round. I will give you the scoreboard and a codeforces handle, please analysis his performance. Don't answer exceed 1500 characters. Point out what kind of problems(tags) the contestant should improved. If you don't found the contestant with the handle, print 'handle does not found'."},
                    {"role": "user", "content": "Handle:"+tmp[1]+"\nScoreboard: "+file.text}
                ]
            )
            print(completion.choices[0].message)
            await message.channel.send(completion.choices[0].message.content)
        if message.content.startswith('$cf-predict'):
            mes = message.content
            tmp = mes.split()
            f = open("cf-data/round"+tmp[1]+".txt", "r")
            #print(f.read())
            #print(f.read())
            #The score in codeforces round is calculate by the formula. In a contest with duration of d minutes, the score you get by solving a problem with initial score x at t-th minute with wincorrect submissions is: max(0.3⋅x,x-⌊120x⋅t/250d⌋-50w).  Don't need to output the scoreboard right now, just output the final scoreboard you predict with score, solving time(in minutes). Output with English. 
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "assistant", "content": "以下是一個 codeforces 比賽的記分板，目前只有經過一個小時，請預測在比賽結束時(再經過一個小時)的記分板。每一題的原始分數已被放在題號旁邊，你需要用公式(後面提供)去計算選手拿到的分數。你需要猜測一個最有可能的最終記分板，猜測每個人會在甚麼時候解出剩餘的題目，並進行分數的計算排名，請使用好看的排版，用 | 去隔開每一項數字，用 ``` 把記分板包起來。Output with English. You must calculate the score by this formula. In a contest with duration of d minutes, the score you get by solving a problem with initial score x at t-th minute with wincorrect submissions is: max(0.3⋅x,x-⌊120x⋅t/250d⌋-50w). The contest is last for 2 hours (d=120). You must calculate the score by this formula. 你需要用這個公式去計算分數。輸出整個記分板的排名，不一定要輸出這麼多解釋，輸出你認為重要的就好。記分板中的資訊就是正確的，你只需要在參賽者還沒作答的題目中預測就好。Analysis the scoreboard you predict, and output some words like the problems will solved by how many contestants. You need to output the scoreboard you predict and your analysis. You need to calculate the problem by "},
                    {"role": "user", "content": f.read()}
                ]
            )
            
            print(completion.choices[0].message.content)
            word_length = len(completion.choices[0].message.content)
            for i in (0, int(word_length/1950)):
                a = i*1950
                b = min((i+1)*1950, word_length)
                #print(f'{a} {b} {i}')
                #print(f'hello')
                await message.channel.send(completion.choices[0].message.content[int(a):int(b)])
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)