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

    def rotate_steps(self, steps):
        try:
            for _ in range(steps):
                for step in self.step_sequence:
                    for pin, val in zip([self.IN1, self.IN2, self.IN3, self.IN4], step):
                        GPIO.output(pin, val)
                    time.sleep(0.001)  # Adjust for speed
        finally:
            self.cleanup()

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    motor = StepperMotor()
    # Rotate approximately 1/4 turn
    steps_for_quarter_turn = 125  # Adjust if necessary based on your motor's step count
    motor.rotate_steps(steps_for_quarter_turn)
    print("Motor alignment complete.")
