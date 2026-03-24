import time
from adafruit_motor import servo
import pwmio
import board

pwm_out = pwmio.PWMOut(board.A0, frequency=50)
servo = servo.Servo(pwm_out)

print(servo)

while True:
    servo.angle = 0 if servo.angle > 90 else 180

    print(servo.angle)

    time.sleep(1)
