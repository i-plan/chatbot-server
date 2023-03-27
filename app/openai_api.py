"""
openai api: https://platform.openai.com/docs/api-reference/chat/create?lang=python
"""
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# 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

def chat(txt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": txt}
        ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message

if __name__ == '__main__':
    chat("hi,good monoring")