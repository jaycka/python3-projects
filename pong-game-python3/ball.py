from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('circle')
        self.speed_x = 10
        self.speed_y = 10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.speed_x
        new_y = self.ycor() + self.speed_y
        self.goto(new_x, new_y)

    def bounce(self, side):
        if side == 'wall':
            self.speed_y *= -1
        elif side == 'paddle':
            self.speed_x *= -1
            self.move_speed *= 0.9

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.1
        self.speed_x *= -1

