import math
from openai import OpenAI

# 記得key不要洩漏出去
api_key = 'api-key'
client = OpenAI(api_key = api_key)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "assistant", "content": "The score in codeforces round is calculate by the formula. In a contest with duration of d minutes, the score you get by solving a problem with initial score x at t-th minute with wincorrect submissions is: max(0.3⋅x,x-⌊120x⋅t/250d⌋-50w). "},
    {"role": "user", "content":"calculate a contestant get 1 rejected submission, and get accepted on problem C at 1:47 minutes. Problem C is valued 1500 points, calculate the points this contestant can get. The duration of the contest is 2 hours. You should calculate it step by step, but don't need to output the all process."}
    ]
)

#print(completion.choices[0].message)
print(completion.choices[0].message.content)