import analogio
from node_config import *
from simulation import get_instance
from utils import c_to_f

adc_to_V = 2.57 / 51000
c_to_mV = 10
c_to_V = c_to_mV / 1000
V_to_c = 1 / c_to_V

# Only import hardware modules if we're not simulating
if node_type != NODE_TYPE_SIMULATED:
    import board

# ---------LM35 code----------#
ADC_MAX_VOLTAGE = 5.0  # Voltage range for the ADC input
ADC_MAX_VALUE = 65535  # Max value coming off the ADC
LM35_MV_PER_C = 10.0  # millivolts per degrees Celsius

_lm35_pin = None
# LM35 temperature sensor initialization
# TODO: pin configuration
if node_type == NODE_TYPE_SIMULATED:
    _lm35_pin = None
elif board.board_id == "adafruit_funhouse":
    _lm35_pin = analogio.AnalogIn(board.A0)
    print("Using A0")
elif board.board_id == "unexpectedmaker_feathers2":
    _lm35_pin = analogio.AnalogIn(board.A3)
    print("Using A3")
else:
    _lm35_pin = None


# Get a temperature reading from the LM35
def lm35_temperature_c():
    adc = _lm35_pin.value
    v = adc * adc_to_V
    T = V_to_c * v

    return T

# Get a temperature reading from the FunHouse internal temperature sensor
def funhouse_temperature_c():
    return lm35_temperature_c()


# ---------End FunHouse code----------#


# Get a temperature reading using whatever sensor is configured. zone is the zone ID of
# the zone we're getting the reading for (used when simulating)
def get_current_temperature_f(zone=0):
    if node_type == NODE_TYPE_SIMULATED:
        instance = get_instance()
        return instance.get_temperature_f(zone)

    if board.board_id == "unexpectedmaker_feathers2":
        return c_to_f(lm35_temperature_c())

    if board.board_id == "adafruit_funhouse":
        return c_to_f(funhouse_temperature_c())
