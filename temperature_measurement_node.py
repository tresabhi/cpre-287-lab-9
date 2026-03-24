import adafruit_dotstar
import board, analogio, digitalio
from node_config import *
import networking
import time
from sensing import *
from simulation import *

# Set up networking.
networking.connect_to_network()
# networking.mqtt_initialize()
# networking.mqtt_connect()

# The previously reported temperature values.
# prev_temps = [None] * num_zones

# Timing variables.
# LOOP_INTERVAL_NS = 1000000000 / 1000
# _prev_time = time.monotonic_ns()

# TEMPERATURE_LOG_THRESHOLD = 0
# last_temps = {}


# Runs periodic node tasks.
def loop():
    sim = get_instance()

    while True:
        sim.loop()
        time.sleep(0)

        temp = get_current_temperature_f()
        print(f"T = {temp:.3g}°f")

        # values = [
        #     f"t = {sim.last_t:.2f}s\t",
        #     f"Outside: {c_to_f(sim.outside_temp):.2f}°f",
        # ]

        # for zone in range(num_zones):
        #     values.append(f"{zone_names[zone]}: {get_current_temperature_f(zone):.2f}°f")

        # average()

        # print("\t".join(values))


ldo2 = digitalio.DigitalInOut(board.LDO2)
ldo2.direction = digitalio.Direction.OUTPUT


def enable_LDO2(state):
    """Set the power for the second on-board LDO to allow no current draw when not needed."""
    ldo2.value = state
    # A small delay to let the IO change state
    time.sleep(0.035)


def dotstar_color_wheel(wheel_pos):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    wheel_pos = wheel_pos % 255

    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0


absolute0 = 273.15
min_temp = -5 + absolute0
max_temp = 27 + absolute0

enable_LDO2(True)
dotstar = adafruit_dotstar.DotStar(
    board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True
)


def average():
    average = 0
    sim = get_instance()

    for zone in range(num_zones):
        temp = sim.zone_temps[zone]
        average += temp

    average /= num_zones
    average += absolute0

    x = (average - min_temp) / (max_temp - min_temp)
    r = 255 * x
    g = 0
    b = 255 * (1 - x)

    dotstar[0] = (r, g, b, 0.1)
