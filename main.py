import cv2
from ui import AutoTrainerUI
from behavior_tracker import DogBehaviorTracker
from dog_detector import DogDetector
from motor_control import StepperMotor

import os
import psutil



def main():

    # Set the priority of the current process (Linux/Unix)
    if os.name != 'nt':
        p = psutil.Process(os.getpid())
        p.nice(5)  # Higher priority on Linux/Unix (the lower the number, the higher the priority)
        
    # initialize
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Error -- could not open webcam")
        return
    

    # Create DogDetector here
    detector = DogDetector(
        "MobileNetSSD_deploy.caffemodel",
        "MobileNetSSD_deploy.prototxt",
        ["background", "aeroplane", "bicycle", "bird", "boat",
         "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
         "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
         "sofa", "train", "tvmonitor"]
    )

    # Pass both webcam and detector to DogBehaviorTracker
    tracker = DogBehaviorTracker(webcam, detector)

    ui = AutoTrainerUI(webcam, tracker)

    try:
        # Run UI or tracking logic
        ui.run()  # UI invokes tracker.check_couch()
    finally:
        # Cleanup
        tracker.stop_tracking()  # Gracefully stop the tracking thread        
        webcam.release()
        cv2.destroyAllWindows()


# makes it so main gets run automatically if script is run directly
if __name__ == "__main__":
    main()