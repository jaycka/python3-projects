from turtle import Turtle, Screen
import random


def main():
    screen = Screen()
    screen.setup(width=500, height=400)
    answer = screen.textinput(title='Make a bet', prompt='Choose a rainbow color to bet on: ')
    color = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

    turtles = {}
    starting_y = -100
    for i in color:
        turtles[i] = Turtle(shape='turtle')
        turtles[i].color(i)
        turtles[i].penup()
        starting_y += 30
        turtles[i].goto(x=-230, y=starting_y)

    race_on = False
    if answer:
        race_on = True
    while race_on:
        for j in turtles:
            turtles[j].fd(random.randint(0, 10))
            if turtles[j].xcor() > 230:
                race_on = False
                if j == answer:
                    print(f"You've won! The winner is {j} turtle!")
                else:
                    print(f"You've lost! The winner is {j} turtle!")
    screen.exitonclick()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
