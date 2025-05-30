import RPi.GPIO as GPIO
import time


class StepperMotor:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.IN1, self.IN2, self.IN3, self.IN4 = 17, 18, 27, 22
        GPIO.setup([self.IN1, self.IN2, self.IN3, self.IN4], GPIO.OUT)

        # Basic step sequence to rotate the motor
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]

    def dispense_treat(self):
        try:
            for _ in range(500):  # full rotation
                for step in self.step_sequence:
                    for pin, val in zip([self.IN1, self.IN2, self.IN3, self.IN4], step):
                        GPIO.output(pin, val)
                    time.sleep(0.001)
        except KeyboardInterrupt:
            GPIO.cleanup()  # Cleanup on interrupt


    def cleanup(self):
        GPIO.cleanup()