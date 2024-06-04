import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a creative AI."},
        {"role": "user", "content": "请写一篇关于爱情的诗"},
    ],
    temperature=0.8,
    max_tokens=60
)
print(response['choices'][0]['message']['content'])

