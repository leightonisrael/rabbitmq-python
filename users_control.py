from flask import Flask, request

chat_occurencies = []

app = Flask(__name__)

@app.route('/users')
def get_users_size():
    chat = request.args.get('chat', type=str)

    count = 0
    for item in chat_occurencies:
        if item == chat:
            count += 1

    return str(count)

@app.route('/users', methods = ['POST'])
def post_user():
    chat = str(request.data.decode("ascii"))

    chat_occurencies.append(chat)
    return "ok"
    

if __name__ == '__main__':
    app.run()