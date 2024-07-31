import openai
from openai.embeddings_utils import distances_from_embeddings

def create_contexts(question, df, max_len=1800, size='ada', openai_key=""):

    openai.api_key = openai_key
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
    max_tokens=500,
    stop_sequence=None,
    openai_key=""):

    openai.api_key = openai_key
    context= create_contexts(question, df, max_len, size, openai_key)
    try :
        response = openai.Completion.create(
            prompt = f"""
                        Answer the question based on the context below.
                        This is Jeongeunseong's portfolio prompt Ai.
                        But you are Ice Bear from We Bare Bears.
                        Answer all questions in third person, starting with 'Ice Bear'.
                        If the question is in Korean, answer in Korean. If the question is in English, answer in English. Here are some examples:
                        1. "아이스베어가 정은성의 포트폴리오를 찾아본 바로는 ~이야."
                        2. "아이스베어가 추천하는 정은성의 포트폴리오는 ~이야."
                        3. "Ice Bear thinks that Jeongeunseong's portfolio is ~."
                        4. "Ice Bear recommends Jeongeunseong's portfolio is ~."
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
            