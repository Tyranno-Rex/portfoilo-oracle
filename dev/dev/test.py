import os
import pandas as pd
import tiktoken
import openai

# OpenAI API 키 설정
openai.api_key = 'your-api-key'

def remove_newlines(text):
    return text.replace('\n', ' ').replace('\r', '')

texts = []

directory = './fastapi/data/repo'
for file in os.listdir(directory):
    if file.endswith(".txt"):
        with open(os.path.join(directory, file), "r", encoding="UTF-8") as f:
            text = f.read()
            file_name = file[:-4] 
            texts.append((file_name, text))

df = pd.DataFrame(texts, columns=['title', 'text'])
df['text'] = df['title'] + ". " + remove_newlines(df['text'])

df.to_csv('./fastapi/processed_texts.csv', index=False)
print(df.head())

tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('./fastapi/processed_texts.csv')
df.columns = ['title', 'text']

df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))
df['n_tokens'].hist()

def split_into_many(text, max_token = 500):
    sentences = text.split(". ")

    n_tokens = [len(tokenizer.encode(" "+ sentence)) for sentence in sentences]

    chunks = []
    token_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if token_so_far + token > max_token:
            chunks.append(" ".join(chunk) + ".")
            chunk = []
            token_so_far = 0

        if token > max_token:
            continue

        chunk.append(sentence)
        token_so_far += token + 1
    
    if chunk:
        chunks.append(" ".join(chunk) + ".")
    
    return chunks

shortened = []

for row in df.iterrows():
    title = row[1]['title']
    
    if row[1]['text'] is None:
        continue

    if row[1]['n_tokens'] > 500:
        chunks = split_into_many(row[1]['text'])
        shortened.extend([(title, chunk) for chunk in chunks])
    else:
        shortened.append((title, row[1]['text']))

df = pd.DataFrame(shortened, columns=['title', 'text'])
df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))
df['n_tokens'].hist()

df.to_csv('./fastapi/processed_texts_shortened.csv', index=False)

# 'embedding' 컬럼 추가
# df['embedding'] = df['text'].apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
