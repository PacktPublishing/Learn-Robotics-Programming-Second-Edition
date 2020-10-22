import robot
from time import sleep

def straight(bot, seconds):
    bot.set_left(100)
    bot.set_right(100)
    sleep(seconds)

def turn_left(bot, seconds):
    bot.set_left(20)
    bot.set_right(80)
    sleep(seconds)

def turn_right(bot, seconds):
    bot.set_left(80)
    bot.set_right(20)
    sleep(seconds)

def spin_left(bot, seconds):
    bot.set_left(-100)
    bot.set_right(100)
    sleep(seconds)

bot = robot.Robot()
straight(bot, 1)
turn_right(bot, 0.6)
straight(bot, 0.6)
turn_left(bot, 0.6)
straight(bot, 0.6)
turn_left(bot, 0.6)
straight(bot, 0.3)
spin_left(bot, 1)

