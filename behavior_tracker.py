import cv2
import simpleaudio as sa
import time
from motor_control import StepperMotor
#from dog_detector import DogDetector

class DogBehaviorTracker:
    def __init__(self, capture, detector):
        # init webcam
        self.capture = capture
        self.detector = detector
        self.frame = None
        self.detection_result = None  # Shared variable for detection
        self.running = True

        # Set capture resolution to 320x240
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # Load whistle audio
        self.whistle_audio = sa.WaveObject.from_wave_file("whistle.wav")
        self.whistle_playing = False  # To avoid multiple whistle sounds overlapping

        self.motor = StepperMotor()


    def check_couch(self):
        #print("check_couch started!")  # Debug log
        frame_skip = 5  # Number of frames to skip
        frame_count = 0

        while self.running:
            # Access the latest frame in a thread-safe way
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to read frame.")
                continue

            if frame_count % frame_skip == 0:
                detection = self.detector.detect(frame)
                self.detection_result = detection  # Store detection result

                if detection:
                    # Unpack detection result
                    x_start, y_start, x_end, y_end, confidence = detection
                    frame_height = frame.shape[0]
                    two_thirds_y = int(frame_height * 2 / 3)
                    print(f"Detection: {detection}")  # general dog detection

                    # Check if the dog is above the blue line
                    if y_end <= two_thirds_y and not self.whistle_playing:
                        print("Dog detected on couch! Playing whistle.")
                        self.whistle_playing = True  # Prevent multiple whistle sounds
                        self.play_whistle()

                # else:
                #     print("No dog detected.")

            frame_count += 1

    def play_whistle(self):
        # Play the whistle sound in a non-blocking way
        play_obj = self.whistle_audio.play()

        print("Dispensing treat...")
        self.motor.dispense_treat()

        play_obj.wait_done()  # Wait for the sound to finish
        # time.sleep(3) #give dog 3 seconds to respond
        self.whistle_playing = False


    def stop_tracking(self):
        self.running = False  # Stop the capture threads