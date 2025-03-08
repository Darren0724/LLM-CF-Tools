import json

with open('cf-data/round101.json', 'r') as f:
    data = json.load(f)


problems = [problem['index'] for problem in data['result']['problems']]

header = ['problem'] + problems
print(' '.join(header),end=' total\n')

# 假設的結束時間
end_time = 60

# 處理每個選手的資料
for row in data['result']['rows']:
    rank = f"rank{row['rank']}"
    handle = row['party']['members'][0]['handle']
    scores = [int(problem['points']) for problem in row['problemResults']]
    
    print(f"{rank} {handle}",end="")
    print(len(scores))
    sz = len(scores)
    for i in range (0,sz):
        if scores[i] == 0:
            print(f"{scores[i]}/0 ",end="")
        else:
            submission_time = (int)(row['problemResults'][i]['bestSubmissionTimeSeconds']/60)
            print(f"{scores[i]}/{submission_time} ",end="")
    print(f"{(int)(row['points'])}")