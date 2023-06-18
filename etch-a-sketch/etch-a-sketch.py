from turtle import Turtle, Screen


def main():
    timmy = Turtle()
    screen = Screen()

    def w():
        timmy.fd(10)

    def s():
        timmy.bk(10)

    def a():
        timmy.lt(10)

    def d():
        timmy.rt(10)

    def c():
        timmy.clear()
        timmy.penup()
        timmy.home()
        timmy.pendown()

    screen.onkeypress(key='w', fun=w)
    screen.onkeypress(key='s', fun=s)
    screen.onkeypress(key='a', fun=a)
    screen.onkeypress(key='d', fun=d)
    screen.onkey(key='c', fun=c)
    screen.listen()
    screen.exitonclick()


if __name__ == '__main__':
    main()
