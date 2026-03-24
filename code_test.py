import time
import board
import analogio
from node_config import *
import sensing
import temperature_measurement_node

if node_type == NODE_TYPE_RAW:
    while True:
        adc = sensing._lm35_pin.value
        v = adc * sensing.adc_to_V
        T = sensing.V_to_c * v

        print(f"adc = {adc}\tv = {v:.3g}V\tT = {T:.3g}deg")

        time.sleep(0.1)

elif node_type == NODE_TYPE_TEMPERATURE:
    temperature_measurement_node.loop()