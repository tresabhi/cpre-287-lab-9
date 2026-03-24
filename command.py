# Define Command types
TYPE_NONE = 0
TYPE_DAMPER = 1
TYPE_HEAT_COOL = 2

# Define possible values for Commands of TYPE_HEAT_COOL
HEAT_COOL_OFF = 0
HEAT_COOL_COOLING = 1
HEAT_COOL_HEATING = 2

# Commands are parsed into strings before they are sent over the network
COMMAND_MAX_LENGTH = 100 # Maximum number of characters in a Command string
COMMAND_SEPARATOR = ':'  # Used to delineate the components of a Command string

# Represents a command sent from the primary control node to the secondary control node
class Command:

    # This function is run when the Command is instantiated
    def __init__(self, type=TYPE_NONE, values=None, msg=None):
        self.type = type
        self.values = values

        # If a command string is passed in, parse it to initialize this Command
        if msg is not None:
            words = msg.split(COMMAND_SEPARATOR)
            try:
                self.type = int(words[0])
            except ValueError:
                print(f'Warning: unable to convert {words[0]} to int, setting command type to NONE')
                self.type = TYPE_NONE
            if len(words) > 1:
                self.values = words[1:]

        # The values should be a list - fix it if not.
        if not isinstance(self.values, list):
            self.values = [self.values]

    # This function is called when a Command is converted to a string with str(). This is done
    # by the primary control node in order to get the message body to send over the network.
    def __str__(self):
        ret = f'{self.type}'
        for val in self.values:
            ret += f':{val}'
        return ret

