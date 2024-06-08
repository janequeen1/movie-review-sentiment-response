from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key = openai_api_key
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_content = request.form['review']
    system_content = '영화 후기의 감정을 분석합니다. 한국인들의 언어를 분석해서 "긍정", "부정", "중립" 중 하나로 대답해주면 됩니다.'

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content},
        ]
    )

    sentiment = response.choices[0].message.content
    return render_template('result.html', review=user_content, sentiment=sentiment)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)