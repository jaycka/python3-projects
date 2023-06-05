from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
DIRECTION = 180


class CarManager:
    def __init__(self):
        self.cars = []
        self.speed = STARTING_MOVE_DISTANCE

    def make_car(self):
        if random.randint(1, 6) == 1:
            new_car = Turtle()
            new_car.penup()
            new_car.shape('square')
            new_car.shapesize(stretch_len=2, stretch_wid=1)
            new_car.setheading(DIRECTION)
            new_car.color(random.choice(COLORS))
            new_car.goto(300, random.randint(-250, 250))
            self.cars.append(new_car)

    def move_cars(self):
        for i in self.cars:
            i.forward(self.speed)

    def remove_cars(self):
        for car in self.cars:
            if car.xcor() < -320:
                self.cars.remove(car)

    def speed_up(self):
        self.speed += MOVE_INCREMENT
