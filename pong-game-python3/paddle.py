from turtle import Turtle

UP = 90
DOWN = 270


class Paddle(Turtle):
    def __init__(self, side):
        super().__init__()
        self.penup()
        self.shape('square')
        self.color('white')
        self.turtlesize(stretch_wid=1, stretch_len=5)
        self.setheading(UP)
        if side == 'left':
            self.goto(-350, 0)
        else:
            self.goto(350, 0)

    def up(self):
        self.setheading(UP)
        self.forward(20)

    def down(self):
        self.setheading(DOWN)
        self.forward(20)


