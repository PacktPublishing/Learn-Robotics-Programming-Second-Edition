import robot
from time import sleep
from led_rainbow import show_rainbow

def show_left_rainbow(leds):
    led_range = range(0, leds.count // 4)
    show_rainbow(leds, led_range)

def show_right_rainbow(leds):
    led_range = range(leds.count - (leds.count // 4), leds.count)
    show_rainbow(leds, led_range)

def straight(bot, seconds):
    bot.set_left(100)
    bot.set_right(100)
    show_left_rainbow(bot.leds)
    show_right_rainbow(bot.leds)
    sleep(seconds)
    bot.leds.clear()

def turn_left(bot, seconds):
    bot.set_left(20)
    bot.set_right(80)
    show_left_rainbow(bot.leds)
    sleep(seconds)
    bot.leds.clear()

def turn_right(bot, seconds):
    bot.set_left(80)
    bot.set_right(20)
    show_right_rainbow(bot.leds)
    sleep(seconds)
    bot.leds.clear()

def spin_left(bot, seconds):
    bot.set_left(-100)
    bot.set_right(100)
    show_left_rainbow(bot.leds)
    sleep(seconds)
    bot.leds.clear()

bot = robot.Robot()
straight(bot, 1)
turn_right(bot, 0.6)
straight(bot, 0.6)
turn_left(bot, 0.6)
straight(bot, 0.6)
turn_left(bot, 0.6)
straight(bot, 0.3)
spin_left(bot, 1)

