import command

# TODO: probably want some global variables here...

# Called when a message is received over the socket
def socket_message_received(msg):
    # Parse the message as a Command
    cmd = command.Command(msg=msg)
    print(f'Command received: {cmd}, values: {cmd.values}')

    # TODO: Check the command type and take action

# TODO: Set up networking etc.

# Perform regular secondary node control tasks
def loop():
    # TODO: throttle this loop? (i.e. don't run it every time)

    #print("Executing secondary control node loop")

    # TODO: maybe? anything to do here?

    pass