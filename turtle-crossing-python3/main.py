from turtle import Screen
from car_manager import CarManager
from player import Player
from scoreboard import Scoreboard
import time


def main():
    screen = Screen()
    screen.title('Turtle Crossing')
    screen.setup(width=600, height=600)
    screen.tracer(0)

    carmanager = CarManager()
    player = Player()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkeypress(fun=player.up, key='Up')

    game_is_on = True
    while game_is_on:
        time.sleep(0.1)
        screen.update()

        carmanager.make_car()
        carmanager.move_cars()
        carmanager.remove_cars()

        for car in carmanager.cars:
            if car.xcor()-30 < player.xcor() < car.xcor()+30 and car.ycor() - 20 < player.ycor() < car.ycor() + 20 and car.distance(player) < 20:
                scoreboard.game_over()
                game_is_on = False

        if player.ycor() > player.finish_line_y:
            player.reset_position()
            scoreboard.level_up()
            carmanager.speed_up()
    screen.exitonclick()


if __name__ == '__main__':
    main()
