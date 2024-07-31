import os
import pandas as pd
import tiktoken
import openai
from openai.embeddings_utils import distances_from_embeddings
from ast import literal_eval
import numpy as np

openai.api_key = ''
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
    sentences = text.split("\n")

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
    
    if row[1]['text'] is None:
        continue

    if row[1]['n_tokens'] > 500:
        shortened += split_into_many(row[1]['text'])
    else:
        shortened.append(row[1]['text'])


df = pd.DataFrame(shortened, columns=['text'])
df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))
df['embeddings'] = df['text'].apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

df.to_csv('./fastapi/processed_texts_embeddings.csv', index=False)
df.head()

df = pd.read_csv('./fastapi/processed_texts_embeddings.csv')
df['embeddings'] = df['embeddings'].apply(literal_eval).apply(np.array)
df.head()

def create_contexts(question, df, max_len=1800, size='ada'):

    q_embeddings = openai.Embedding.create(input=question, engine=f'text-embedding-{size}-002')['data'][0]['embedding']
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    for i, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break

        returns.append(row['text'])
    
    return "\n\n###\n\n".join(returns)

def answer_question(df,
    model="gpt-3.5-turbo-instruct",
    question="Who is the Jeongeuneong?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None):

    context= create_contexts(question, df, max_len, size)

    if debug:
        print("Context:\n" + context)
        print("\n\n")
    
    try :
        response = openai.Completion.create(
            prompt = f"""
                        Answer the question based on the context below. This is Jeongeunseong's portfolio prompt Ai. But you are Ice Bear from We Bare Bears. Answer all questions in third person, starting with 'Ice Bear'. If the question is in Korean, answer in Korean. If the question is in English, answer in English. Here are some examples:
                        1. "아이스베어가 정은성의 포트폴리오를 찾아본 바로는 ~이야."
                        2. "아이스베어는 지금 정은성의 포폴을 그렇게 생각안해."
                        3. "Ice Bear thinks that Jeongeunseong's portfolio is ~."
                        4. "Ice Bear doesn't think Jeongeunseong's portfolio is ~."
                        """ + "\n\n" + "Context:\n" + context + "\n\n" + "Question: " + question + "\n\n" + "Answer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(e)
        return "Ice Bear does not know."
            

print(answer_question(df, question="What is 3D data processing?", debug=True))

                        

