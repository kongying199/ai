import openai

response = openai.Completion.create(
    model="text-davinci-003",
    temperature=0.5,
    max_tokens=100,
    prompt="请写一篇关于爱情的诗")

print(response.choices[0].text.strip())

