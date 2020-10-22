import ledshim


class Leds: 
    @property
    def count(self):
        return ledshim.width

    def set_one(self, led_number, color):
        ledshim.set_pixel(led_number, *color)

    def set_range(self, led_range, color):
        for pixel in led_range:
            ledshim.set_pixel(pixel, *color)

    def set_all(self, color):
        ledshim.set_all(*color)

    def clear(self):
        ledshim.clear()

    def show(self):
        ledshim.show()
