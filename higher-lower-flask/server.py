from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def home():
    global number
    number = random.randint(0, 9)
    return '<div style="text-align:center">' \
           '<h1>Guess a number between 0 and 9</h1>' \
           '<img src="https://media.giphy.com/media/3o6YfTUIfDYjPdnk52/giphy.gif">' \
           '</div>'


@app.route('/<int:input_num>')
def high_low(input_num):
    if input_num > number:
        return '<div style="text-align:center">' \
               '<h1 style="color:red">Too high, try again!</h1>' \
               '<img src="https://media.giphy.com/media/2IodIF8KIFaM0/giphy.gif">' \
               '</div>'
    elif input_num < number:
        return '<div style="text-align:center">' \
               '<h1 style="color:blue">Too low, try again!</h1>' \
               '<img src="https://media.giphy.com/media/TgmiJ4AZ3HSiIqpOj6/giphy.gif">' \
               '</div>'
    else:
        return '<div style="text-align:center">' \
               '<h1 style="color:green">You found me!</h1>' \
               '<img src="https://media.giphy.com/media/l3q2umc327t2nzSOQ/giphy-downsized-large.gif">' \
               '</div>'


if __name__ == '__main__':
    app.run(debug=True)
