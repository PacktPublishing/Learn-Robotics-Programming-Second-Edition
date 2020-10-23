from robot import Robot
from time import sleep

bot = Robot()
red = (255, 0, 0)
blue = (0, 0, 255)

while True:
    print("red")
    bot.leds.set_all(red)
    bot.leds.show()
    sleep(0.5)
    print("blue")
    bot.leds.set_all(blue)
    bot.leds.show()
    sleep(0.5)
