from node_config import num_zones, zone_k
import time
import math
from utils import c_to_f
import actuation
from math import sin, pi

# define some values?

SIM_SPEED = 1

TEMP_RANGE = 10
TEMP_AVG = 0

TEMPERATURE_THRESHOLD = 2

# k is the volume of the room divided by the surface area exposed to the outside
# so we need to divide it by some constant to get a reasonable coefficient
# for the derivative of the temperatures respect to time
TARGET_TEMP = 25
START_TEMP = TEMP_AVG

# The Simulation(R)
_sim = None


# We only want ONE Simulation object, and we want to share it between all of the modules. We can accomplish this
# using the singleton design pattern. This function is a key part of that pattern. It returns the singleton instance.
# Call "simulation.get_instance()" to get a Simulation, instead of instantiating a Simulation directly.
def get_instance():
    global _sim

    if _sim is None:
        _sim = Simulation(num_zones)

    return _sim


# A class that simulates the physical environment for the system.
class Simulation:
    initial_time = time.monotonic()
    zone_temps = {}
    outside_temp = 0

    xs = [0] * num_zones
    angles = [0] * num_zones

    heating = False
    cooling = False

    # Initializes the simulation.
    def __init__(self, num_zones):
        # initialize additional class variables. These are probably variables that represent the state of the physical system.

        for id in range(num_zones):
            self.zone_temps[id] = START_TEMP

    # Returns the current temperature in the zone specified by zone_id
    def get_temperature_f(self, zone_id):
        # implement
        return c_to_f(self.zone_temps[zone_id])

    # Sets the damper(s) for the zone specified by zone_id to the percentage
    # specified by percent. 0 is closed, 100 is fully open.
    def set_damper(self, type, zone_id, percent):
        print("set damper")
        # implement

    # Update the temperatures of the zones, given that elapsed_time_ms milliseconds
    # have elapsed since this was previously called.
    last_t = 0

    def _update_temps(self, t):
        dt = t - self.last_t
        t_days = t / 60 / 60 / 24 + 0.5

        if self.last_t == t:
            return

        self.last_t = t
        self.outside_temp = TEMP_RANGE * sin(2 * pi * (t_days - 0.25)) + TEMP_AVG

        ac_speed = 0

        if self.heating:
            ac_speed += 1

        if self.cooling:
            ac_speed -= 1

        # Update all temps
        for id in range(num_zones):
            T = self.zone_temps[id]
            k = zone_k[id]

            servos = actuation.zone_servos[id]
            angle = 0

            for servo in servos:
                # DO NOT REMOVE LOC BELOW. it magically makes servo.angle work
                dir(servo)
                angle += servo.angle

            angle /= len(servos)
            x = (angle - actuation.SERVO_MIN) / actuation.SERVO_RANGE

            self.angles[id] = angle
            self.xs[id] = x

            # print(x)

            # units for dT/dt = (1 / s) * kelvin = kelvin / s
            dT_dt = -k * (T - self.outside_temp) + ac_speed * x
            # units for dT = kelvin / s * s = kelvin
            # yay! units work out cleanly
            dT = dT_dt * dt

            self.zone_temps[id] += dT

    def _update_dampers(self):
        # for zone in range(num_zones):
        #     zone_temp = self.zone_temps[zone]
        #     cooling = min(1, max(0, zone_temp - TARGET_TEMP)) * 100
        #     heating = min(1, max(0, TARGET_TEMP - zone_temp)) * 100

        #     self.set_damper("cooling", zone, cooling)
        #     self.set_damper("heating", zone, heating)

        zone_id = 0
        average_temp = 0

        for zone in range(num_zones):
            zone_temp = self.zone_temps[zone]
            average_temp += zone_temp

            percentage = (TARGET_TEMP - zone_temp) / 25
            percentage = math.pow(abs(percentage), 1 / 3)
            percentage = min(1, max(0, percentage))
            percentage *= 100

            actuation.set_damper(zone, percentage)

            zone_id += 1

        average_temp /= num_zones

        self.heating = average_temp < TARGET_TEMP
        self.cooling = average_temp > TARGET_TEMP

        # if self.heating:
        #     # heater is already on; keep it on till we go well over the target temperature
        #     self.heating = average_temp < TARGET_TEMP + TEMPERATURE_THRESHOLD
        # else:
        #     # heating is off right now, turn it on if we get too cold
        #     self.heating = average_temp < TARGET_TEMP

        # # same logic as above but for cooling
        # if self.cooling:
        #     self.cooling = average_temp > TARGET_TEMP - TEMPERATURE_THRESHOLD
        # else:
        #     self.cooling = average_temp > TARGET_TEMP

    # Runs periodic simulation actions.
    def loop(self):
        # Calculate the amount of time elapsed since this last time this function was run. See CircuitPython's time module documentation
        # at http://docs.circuitpython.org/en/latest/shared-bindings/time/index.html. We recommend time.monotonic_ns(). Also note that
        # temperature_measurement_node.py has an elapsed time calculation, and you may be able to use a similar approach here.

        # pass in the actual elapsed time.
        self._update_dampers()
        self._update_temps(SIM_SPEED * (time.monotonic() - self.initial_time))

        actuation.set_heating(self.heating)
        actuation.set_cooling(self.cooling)
