import cv2

class DogDetector:
    def __init__(self, model_path, config_path, class_labels):
        # Load the pre-trained model
        try:
            self.net = cv2.dnn.readNetFromCaffe(config_path, model_path)
            #print("Model loaded successfully!")  # Debug log
        except Exception as e:
            print(f"Failed to load model: {e}")  # Log errors
        self.class_labels = class_labels

    def detect(self, frame):
        #print("Detecting...")
        height, width = frame.shape[:2]
        # Prepare the image for the neural network
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (160, 120), 127.5)  # Smaller input size
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                idx = int(detections[0, 0, i, 1])
                label = self.class_labels[idx]
                if label == "dog":  # Check for a dog
                    box = detections[0, 0, i, 3:7] * [width, height, width, height]
                    x_start, y_start, x_end, y_end = box.astype("int")
                    return (x_start, y_start, x_end, y_end, confidence)

        return None  # No dog detected
