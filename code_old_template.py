from node_config import *
import networking
import simulation

# List of functions that will be run each iteration of the main program loop
functions = []

# Simulation object, if applicable
sim = None

# Set up simulation
if node_type == NODE_TYPE_SIMULATED:
    # Use get_instance() to get the singleton simulation instance
    sim = simulation.get_instance()
    functions.append(sim.loop)

# There are three modules corresponding to the three node types (primary, secondary, temperature).
# We want to import the module corresponding to the type of this node, and add its loop() function
# to our list of functions to run. For a simulated node, we initialize and run all three node types.
if node_type == NODE_TYPE_PRIMARY or node_type == NODE_TYPE_SIMULATED:
    import primary_control_node
    functions.append(primary_control_node.loop)
if node_type == NODE_TYPE_SECONDARY or node_type == NODE_TYPE_SIMULATED:
    import secondary_control_node
    functions.append(secondary_control_node.loop)
if node_type == NODE_TYPE_TEMPERATURE or node_type == NODE_TYPE_SIMULATED:
    import temperature_measurement_node
    functions.append(temperature_measurement_node.loop)

# We also need to run the networking module's loop.
functions.append(networking.loop)

# This is the main application loop. It goes round-robin through the loop() functions of the modules we have chosen.
while True:
    for f in functions:
        f()
