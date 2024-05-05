from flask import Flask, render_template
from flask_socketio import SocketIO
import random
from flask_socketio import emit
import cohere
co = cohere.Client('insert api key')
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('generate')
def make_sandwich(data):
    vegetables = ["lettuce", "tomatoes", "red onions", "cucumber", "peppers", "pickels"]
    cheese = ["cheddar", "marble", "blue cheese", "fetta"]
    meat = ["ham", "bologna", "turkey", "bacon", "chicken", "egg"]
    bread = ["white bread", "brown bread", "sourdough bread", "whole wheat bread", "rye", "baugette"]

    rand_veg = random.randrange(len(vegetables))
    rand_cheese = random.randrange(len(cheese))
    rand_meat = random.randrange(len(meat))
    rand_bread = random.randrange(len(bread))

    print(f"""Your sandwich:
        {bread[rand_bread]}
        {vegetables[rand_veg]}
        {cheese[rand_cheese]}
        {meat[rand_meat]}
        {bread[rand_bread]}\n""")
    
    # send a message with the new tough
    # socketio.emit('bread', {'data': bread[rand_bread]})
    # socketio.emit('vegetable', {'data': vegetables[rand_veg]})
    # socketio.emit('cheese', {'data': cheese[rand_cheese]})
    # socketio.emit('meat', {'data': meat[rand_meat]})
    # Emit events to send sandwich components to the client
    emit('bread', {'data': bread[rand_bread]})
    emit('vegetable', {'data': vegetables[rand_veg]})
    emit('cheese', {'data': cheese[rand_cheese]})
    emit('meat', {'data': meat[rand_meat]})

    response = co.chat(
        
        message=f"Generate an explanation of the taste and origins of a sandwich containing: {bread[rand_bread]}, {vegetables[rand_veg]}, {cheese[rand_cheese]}, and {meat[rand_meat]}. Use humour in your explanation, create wild explanations of its origins, make it understanble for kids",
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
    )
    emit('response', {'data': response.text})

    print("HH")
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
