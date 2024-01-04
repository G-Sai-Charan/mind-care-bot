from flask import Flask, render_template, request, jsonify
import openai,os
PEOPLE_FOLDER = os.path.join('static', 'img')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

openai.api_key = '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'

@app.route('/', methods=['GET', 'POST'])
def index():
    i1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image3.png')
    i2 = os.path.join(app.config['UPLOAD_FOLDER'], 'IMAGE1.png')
    i3 = os.path.join(app.config['UPLOAD_FOLDER'], 'maintenance.png')
    if request.method == 'POST':
        message = request.json.get('message')
        if message:
            response = get_bot_response(message)
        else:
            response = "Please enter a message"
        return jsonify({'response': response})
    else:
        return render_template('index.html',image3=i1,image1=i2,maintenance=i3)

@app.route('/you',methods=['GET','POST'])
def you():
    return render_template('a.html')

@app.route('/doc',methods=['GET','POST'])
def doc():
    return render_template('b.html')

def get_api_response(prompt: str) -> str:
    text: str = ''

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=['Human: ', 'AI: ']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text','')

    except Exception as e:
        print('ERROR:', e)
        text ='Something went wrong...'

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    print('2')
    print(*pl)
    prompt: str = ''.join(pl)
    print('3')
    print(prompt)
    return prompt

def get_bot_response(message: str) -> str:
    prompt_list: list[str] = ['You are a psychiatrist and should answer questions related to your profession only']
    print('1')
    print(*prompt_list)
    prompt: str = create_prompt(message, prompt_list)
    print('4')
    print(prompt)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, prompt_list)
        pos: int = bot_response.find('\nAI: ')
        
    else:
        bot_response = 'Something went wrong...'

    return str(bot_response)

if __name__ == '__main__':
    app.run(debug=True)
