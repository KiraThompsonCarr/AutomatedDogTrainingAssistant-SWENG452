import cv2
import threading 
import tkinter as tk
from PIL import Image, ImageTk

class AutoTrainerUI:
    def __init__(self, capture, tracker):

        self.capture = capture
        self.tracker = tracker  # Store reference to the tracker
        self.window=tk.Tk()
        self.window.title("Automated Dog Trainer")

        self.video_label = tk.Label(self.window)
        self.video_label.pack()

        # Inset dog image in UI
        self.image = Image.open("dog.JPG")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.window,image=self.photo)
        self.image_label.pack()

        #init monitoring flag
        self.monitoring = False
        self.tracking_thread = None

        #start button
        self.monitor_button = tk.Button(
            self.window, 
            text="Start Monitoring", 
            command=self.toggle_monitoring,
            width=20,
            height=2
            )
        self.monitor_button.pack(padx=10, pady=10)


    def toggle_monitoring(self):
        #toggle state
        self.monitoring = not self.monitoring

        if self.monitoring:
            self.monitor_button.config(text="Stop Monitoring")
            print("Monitoring dog now!")

            # Start check_couch in a separate thread
            self.tracking_thread = threading.Thread(target=self.tracker.check_couch, daemon=True)
            self.tracking_thread.start()

            self.update_frame()
        else:
            self.monitor_button.config(text="Start Monitoring")
            print("Monitoring stopped.")
            
            # Stop tracking
            self.tracker.stop_tracking()


    def update_frame(self):
        if self.monitoring:
            ret, frame = self.capture.read()
            if ret:
                # Draw the 2/3 line for debugging
                frame_height, frame_width = frame.shape[:2]
                two_thirds_y = int(frame_height * 2 / 3)
                cv2.line(frame, (0, two_thirds_y), (frame_width, two_thirds_y), (255, 0, 0), 2)

                # Use detection results from the tracker
                detection = self.tracker.detection_result  # Access shared detection results
                if detection:
                    x_start, y_start, x_end, y_end, confidence = detection
                    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                    cv2.putText(frame, f"Dog: {confidence:.2f}",
                                (x_start, y_start - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Convert the frame to RGB for Tkinter display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(image)

                self.video_label.config(image=photo)
                self.video_label.image = photo

            self.window.after(10, self.update_frame)

    def run(self):
        self.window.mainloop() # listens for clicks, keys, etc
