from node_config import num_zones, zone_k
import time
import math
from utils import c_to_f
import actuation
from math import sin, pi

# define some values?

SIM_SPEED = 1

TEMP_RANGE = 10
TEMP_AVG = 30

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
    cooling_dampers = [0] * num_zones
    heating_dampers = [0] * num_zones

    xs = [0] * num_zones

    heating = True
    cooling = True

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

        if type == "cooling":
            self.cooling_dampers[zone_id] = percent
        elif type == "heating":
            self.heating_dampers[zone_id] = percent
        else:
            raise Exception(f"Invalid damper type: {type}")

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

        # Update all temps
        for id in range(num_zones):
            T = self.zone_temps[id]
            k = zone_k[id]

            servos = actuation.zone_servos[id]
            angle = 0

            for servo in servos:
                dir(servo)
                angle += servo.angle

            angle /= len(servos)
            x = -(angle - actuation.SERVO_MIN - actuation.SERVO_RANGE / 2) / (
                actuation.SERVO_RANGE / 2
            )
            self.xs[id] = x

            ac_speed = 1

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

            percent = (TARGET_TEMP - zone_temp) / 25
            percent = math.copysign(math.pow(abs(percent), 1 / 3), percent)
            percent += 0.5
            percent *= 100

            actuation.set_damper(zone, percent)

            zone_id += 1

        # self.heating = (
        #     (
        #         # heater is already on; wait till desired temp is reached
        #         average_temp
        #         >= TARGET_TEMP + TEMPERATURE_THRESHOLD
        #     )
        #     if self.heating
        #     else (
        #         # heater is off; turn it on only if temp falls beyond the threshold
        #         average_temp
        #         < TARGET_TEMP - TEMPERATURE_THRESHOLD
        #     )
        # )
        # self.cooling = (
        #     (average_temp <= TARGET_TEMP)
        #     if self.cooling
        #     else (average_temp > TARGET_TEMP + TEMPERATURE_THRESHOLD)
        # )

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
