from node_config import *
import digitalio
import board

led_blue = None
led_red = None

# ------------Damper control-----------#
# Parallax Standard Servo (https://www.parallax.com/product/parallax-standard-servo/)
SERVO_ACTUATION_RANGE = 180  # degrees
SERVO_MIN_PULSE = 750  # us, for PWM control
SERVO_MAX_PULSE = 2250  # us, for PWM control

if node_type != NODE_TYPE_SIMULATED:
    # Damper initialization - use pins A0, A1, and A2 for zones 1, 2, and 3 respectively
    # TODO: damper initialization
    pass


# Set the damper for the given zone to the given percent (0 means closed, 100 means fully open)
def set_damper(zone, percent):
    # TODO: damper control
    pass


# ------------End damper control-----------#

# ------------Heat/cool control-----------#
# TODO: pin configuration
if node_type == NODE_TYPE_SIMULATED and board.board_id == "unexpectedmaker_feathers2":
    # Initialize digital outputs for heating, cooling, and the circulation fan
    # Use pins D13 for heat, D9 and D6 for cooling, and D12 for the fan

    led_red = digitalio.DigitalInOut(board.D13)
    led_blue = digitalio.DigitalInOut(board.D9)

    led_red.direction = digitalio.Direction.OUTPUT
    led_blue.direction = digitalio.Direction.OUTPUT

    pass
else:
    pass


# Control the heater (turn on by passing in True, off by passing in False)
def set_heating(value: bool):
    led_red.value = value


# Control the cooler (turn on by passing in True, off by passing in False)
def set_cooling(value: bool):
    led_blue.value = value


# Control the circulation fan (turn on by passing in True, off by passing in False)
def set_circulating(value: bool):
    # TODO: circulation fan control
    pass


# ------------End heat/cool control-----------#
