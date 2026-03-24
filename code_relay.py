import digitalio
import board
import time

led_blue = digitalio.DigitalInOut(board.D13)
led_red = digitalio.DigitalInOut(board.D12)

led_blue.direction = digitalio.Direction.OUTPUT
led_red.direction = digitalio.Direction.OUTPUT

while True:
    led_red.value = led_blue.value
    led_blue.value = not led_blue.value

    print("red" if led_red.value else "blue")

    time.sleep(1)