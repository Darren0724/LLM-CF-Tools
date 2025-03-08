import json
for round in range(1001,1051):
    with open('cf-data/round'+(str)(round)+'.txt', 'w') as output:
        print(round)
        try:
            with open('cf-data/round'+(str)(round)+'.json', 'r') as f:
                data = json.load(f)
        except:
            print('failed')
            continue 
        
        problem = 0
        try:
            problems = [problem for problem in data['result']['problems']]
        except:
            print('failed')
            continue 
        print('problem ',end="",file=output)
        for i in range (0,len(problems)):
            point = 0
            try:
                point = (int)(problems[i]['points'])
            except:
                point = 1
            print((str)(problems[i]['index']+'/'+(str)(point)),end=" ",file=output) 
            #print(problems[i])
        #output.write(' '.join(header),end=' total\n')
        #print(''.join(header),end=' total\n',file=output)
        print(file=output)
        # 假設的結束時間
        end_time = 60

        # 處理每個選手的資料
        contestant = list()

        for row in data['result']['rows']:
            rank = f"rank{row['rank']}"
            handle = row['party']['members'][0]['handle']
            scores = [int(problem['points']) for problem in row['problemResults']]
            
            print(f"{handle} ",end="",file=output)
            #output.write(f"{handle} ",end="")
            sz = len(scores)
            tot = 0
            for i in range (0,sz):
                if scores[i] == 0:
                    print(f"{scores[i]}/0 ",end="",file=output)
                    #output.write(f"{scores[i]}/0 ",end="")
                else:
                    submission_time = (int)(row['problemResults'][i]['bestSubmissionTimeSeconds']/60)
                    if submission_time <= end_time:
                        print(f"{scores[i]}/{submission_time} ",end="",file=output)
                        #output.write(f"{scores[i]}/{submission_time} ",end="")
                        tot += scores[i]
                    else:
                        print("0/0 ",end="",file=output)
                        #output.write("0/0 ",end="")
            print(f"{tot}",file=output)
            #output.write(f"{tot}")