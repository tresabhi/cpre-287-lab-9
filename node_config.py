# Define possible node types
NODE_TYPE_SIMULATED = 0
NODE_TYPE_PRIMARY = 1
NODE_TYPE_SECONDARY = 2
NODE_TYPE_TEMPERATURE = 3
NODE_TYPE_RAW = 4

# Node's type, used to determine what code is run.
node_type = NODE_TYPE_SIMULATED

# Total number of zones in the system
num_zones = 3

inch_to_meter = 1 / 39.37
iphone = 5.94 * inch_to_meter

# Volumes of the model rooms are measured in iphone 11s and inches because we
# didn't have any calculators haha.
room_a_width = room_b_width = 1 * iphone
room_a_length = room_b_length = 2 * iphone
room_a_height = room_b_height = 1 * iphone

room_c_width = 1 * iphone
room_c_height = 2 * iphone
room_c_length = 4 * iphone + 2 * inch_to_meter

volume_a = room_a_width * room_a_height * room_a_length
volume_b = room_b_width * room_b_height * room_b_length
volume_c = room_c_width * room_c_height * room_c_length

area_a = room_a_width * room_a_height + room_a_width * room_a_length
area_b = area_a + room_b_length * room_b_height + room_b_width * room_b_length
area_c = (
    2 * room_c_width * room_c_height
    + room_c_length * room_c_height
    + room_c_width * room_c_length
)

U = 2.6
rho = 1.225
c_p = 1005

# the units work out, see comments in simulation._update_temps
zone_k = {
    0: (U * area_a) / (rho * volume_a * c_p),
    1: (U * area_b) / (rho * volume_b * c_p),
    2: (U * area_c) / (rho * volume_c * c_p),
}

zone_names = ["A", "B", "C"]

# Zone that the node is located in, starting at 0. Only relevant for temp measurement nodes.
zone_id = 0
