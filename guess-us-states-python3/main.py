from turtle import Turtle, Screen
import pandas as pd

IMAGE_PATH = './blank_states_img.gif'
DATA_PATH = './50_states.csv'

data = pd.read_csv(DATA_PATH)

screen = Screen()
screen.title('U.S. States Game')
screen.setup(width=725, height=491)
screen.bgpic(IMAGE_PATH)

timmy = Turtle()
timmy.penup()
timmy.hideturtle()

guessed_states = []
while len(guessed_states) < 50:
    if len(guessed_states) == 0:
        answer = screen.textinput(title='Guess the State', prompt="What's another state's name?").title()
    else:
        answer = screen.textinput(title=f'{len(guessed_states)}/50 States Correct',
                                  prompt="What's another state's name?").title()
    if answer == 'Exit':
        break

    if sum(data.state == answer) and answer not in guessed_states:
        timmy.goto(x=data[data.state == answer].iloc[0, 1], y=data[data.state == answer].iloc[0, 2])
        timmy.write(answer, align='center', font=('Arial', 8, 'normal'))
        guessed_states.append(answer)

states_to_learn = pd.DataFrame(list(set(data.state) - set(guessed_states)), columns=['Missing States'])
states_to_learn.to_csv('states_to_learn.csv')
