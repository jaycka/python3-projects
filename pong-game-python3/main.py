from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.title('Pong')
screen.setup(width=800, height=600)
screen.bgcolor('black')
screen.tracer(0)

t = Turtle()
t.hideturtle()
t.penup()
t.goto(0, -300)
t.color('white')
t.pensize(5)
t.setheading(90)
while t.ycor() <= 300:
    t.pendown()
    t.forward(10)
    t.penup()
    t.forward(20)

paddle1 = Paddle('left')
paddle2 = Paddle('right')
ball = Ball()
scoreboard = ScoreBoard()

screen.listen()
screen.onkey(fun=paddle1.up, key='w')
screen.onkey(fun=paddle1.down, key='s')

screen.onkey(fun=paddle2.up, key='Up')
screen.onkey(fun=paddle2.down, key='Down')

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    if ball.ycor() >= 280 or ball.ycor() <= -280:
        ball.bounce('wall')

    if (ball.speed_x > 0 and paddle2.ycor()-50 < ball.ycor() < paddle2.ycor()+50 and 330 <= ball.xcor() <= 350) or (ball.speed_x < 0 and paddle1.ycor()-50 < ball.ycor() < paddle1.ycor()+50 and -350 <= ball.xcor() <= -330):
        ball.bounce('paddle')

    if ball.xcor() > 380 or ball.xcor() < -380:
        if ball.xcor() > 380:
            scoreboard.point1()
            ball.reset_position()
        else:
            scoreboard.point2()
            ball.reset_position()

screen.exitonclick()
