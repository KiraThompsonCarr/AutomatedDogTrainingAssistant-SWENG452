ABSTRACT
This project explores a proof of concept for automated dog training as a supplement to traditional training methods. It focuses on teaching a dog to stay off the couch using monitoring, behavior correction, and rewards. The system employs a webcam to detect the dog on the couch, an audio whistle to summon the dog, and a treat dispenser to reinforce desired behavior.
The main hardware elements are a Raspberry Pi, USB webcam, and motor-driven treat dispenser. The software integrates image recognition and a user interface to view and interact with data. While the original design aimed for more complex functionality, necessary adjustments simplified the system and improved performance.
The system operates by monitoring the couch area at regular intervals. When the dog is detected on the couch, it plays a whistle sound and dispenses a treat simultaneously to guide the dog to the dispenser. While setbacks occurred—such as imprecise image recognition and treat dispenser alignment issues—the system successfully demonstrated its intended function.
Though it cannot replace an owner’s direct involvement, this automated trainer serves as an effective tool for reinforcing training. Future improvements could enhance image recognition accuracy and robustness, making it a more reliable assistant.

1.0	INTRODUCTION
Many people believe it is possible for any dog – regardless of breed, age, or background – to learn how to be well behaved. Though training with an owner can strengthen the bond between pet and owner, it isn’t practical for an owner to give 100% of their attention to the pet every day. This project is to serve as a proof of concept for automated dog training, which can be supplemental to direct training from the owner. The original plan for this project – automated recognition and rewarding for several kinds of tricks – proved to be ambitious, the scaled-down project still kept the main goal in mind. This project helps dogs learn to stay off the couch by monitoring, correcting, and rewarding the dog.
Early stages of dog training is highly dependent on the use of luring and rewards. As such, the system offers the dog positive incentive for good behavior to train him to stay off the couch. This program, when launched, will monitor the living room area via webcam; when it recognizes undesired behavior (i.e. the dog is detected on the couch), the system will summon the dog and dispense a treat for him to reward his obedience.

2.0	FUNCTIONAL SPECIFICATION
Though the goal of the system is not complicated, it is important to introduce the intended behavior and the setup of the system in order to understand design choices described later.

2.1 Typical Use Case
The main players in this system will be the user (i.e. the owner) and the dog. The user is responsible only for starting and terminating the program, as the program is intended to monitor the dog’s behavior indefinitely. The dog’s actions – namely, getting on and off the couch – are what will most impact the system’s behavior (i.e. summoning the dog, dispensing a treat, etc.)
 When the program is run, the user activates the automated trainer by selecting the “Start Monitoring” button and the system begins monitoring the dog’s behavior. An image is sampled from the camera and processed on regular intervals. When the dog is detected on the couch, the system will play an audio recording of the dog’s familiar whistle call to lure him from the couch and toward the treat dispenser. 
The initial plan was to start a three second timer after the whistle call before taking image samples again to ensure the dog has left the couch before dispensing a treat, playing the whistle call again if the dog still hadn’t left the couch. In testing, however, the dog was confused at the sound of the whistle, as both owners were already in the room, and he didn’t understand where he needed to go. To address this confusion, an adjustment was made to the program so it would dispense the treats at the same time the whistle call played, so the dog knew to leave the couch and approach the treat dispenser to claim his reward.
In both the theoretical and actual designs, however, the system would resume monitoring the couch after dispensing a treat, checking for the dog on regular intervals until the user terminated the program.

2.2 System Hardware and Setup
The hardware used in the system is fairly straightforward; a USB-driven webcam captured video footage of the living room for the system to process, and a reservoir for treats was mounted on a box, with slits cut in the lid of the treat dispenser that would align with the base to allow a treat to fall through. Within the box, a stepper motor was secured on the underside of the box lid to drive the rotation of the treat dispenser base. A motor driver and an external power source – in addition to the GPIO pins of the Raspberry Pi – were required to facilitate the motor rotation.
 
3.0	SOFTWARE DESIGN
Like most large projects, some of the original plans were not feasible in practice. This system’s design changed over time, and elements had to be added in order to increase the effectiveness and performance of the system.

3.1 Comparing Original Plan and Final System Behavior
In the initial design, the system is activated by the user selecting “start”, and the program begins in an “Idle” state, checking for the dog on an interval that should be between 100 and 250 ms. When the dog is detected, it is required that the system transition to the “Whistle” state within 100 ms in order to react quickly in response to the dog’s behavior. The “Whistle” state immediately transitions to waiting for the dog to approach the camera and treat dispenser. Depending on how successful the dog’s behavior is, the “Wait” state may transition to either repeating the “Whistle” or to “GiveReward”. After a reward is given, the system returns to its Idle state unless interrupted by the user pressing “exit”.
As mentioned in previous sections, however, the original design featured additional steps and states that were adjusted or removed in the final system. The final system combined the Whistle, Wait, and GiveReward states into a “CallDog” state and simplified transitions. In the final design, once the system enters its active state, the user can select to “start monitoring”, where images are checked on an interval that should be between 100 and 250 ms. In implementation, this requirement is most likely met. The webcam used takes 30 frames per second (fps). To reduce processing lag, the system was set up to monitor every fifth frame, or 6 fps. This would take about 167 ms without processing or other delays, putting it safely within the timing requirement shown in the diagram.
When the dog is detected on the couch, the system transitions from Monitoring to CallDog, where it remains for about 3 seconds. The original plan was to use a timer to hold this state for 3 seconds to prevent repeated calls, but using the sleep() function introduced other timing issues, so this was temporarily resolved by using a recording that was 3 seconds long – i.e. the whistle and then silence – and using a built in wait_done() function available through simpleaudio [1]. After the audio played and the treat was dispensed, the system returned to the monitoring state until the user terminated the program.

3.2 Improving Performance with Priorities and Threading
One of the major obstacles in the development process was that the introduction of image recognition introduced significant latency to the system. The video feedback lagged by several seconds, and a few measures had to be taken to reduce that difference.
First, frame rates were reduced from 30 fps to 6 fps, as mentioned above. Threading was also introduced into the system to reduce delays checkCouch would introduce to the system overall. Using threads, however, led to issues with the UI, specifically that the boundaries weren’t being drawn because they were overwritten or those functions weren’t given CPU time. To resolve that issue, I used psutil [2] to modify the priority of the process to ensure the UI functions were sufficiently high priority. Once those changes were made, the lag was reduced to fall within 1 second or so, allowing the system to function correctly.

4.0	RESULTS
Although several adjustments had to be made during the development process, many of the original expectations were met to some degree.

4.1 UI and Image Recognition
The initial screen, created using tkinter toolkit [3] and pillow library [4], featured an image of a dog and a button to start the monitoring process.
Once the monitoring began, the camera’s video data was displayed within the window with the help of OpenCV [5]. There is a blue line printed across the video display that serves as an indicator for the couch threshold, allowing the user to ensure the camera is properly aligned, as it was not permanently fastened in any particular position. For image recognition, a model from MobileNet-SSD-RealSense [6] was used, which provided boundaries of the suspected dog which could be shown in green, as well as a confidence level that could be printed above the box.
There were some setbacks within the UI and image recognition modules of the project. For example, sometimes frames would fail to read or wouldn’t recognize the dog. Although different camera distances and different backdrop colors were used in an effort to increase contrast, the root cause of these failures were never identified. Occasionally, the dog would be identified, but the boundaries given were imprecise, and part of the bounds would fall outside of the couch threshold, and the dog would not be recognized as being on a couch. A potential remedy for this imprecision in later versions would be to use a percentage of the boundaries (e.g. if 90% of the boundary is above the blue line, assume the dog is on the couch).

4.2 Treat Dispenser
As shown with the hardware earlier in the report, the Raspberry Pi’s GPIO pins controlled the rotation of the stepper motor to control the treat dispenser. In response to the program, the base of the dispenser would rotate, temporarily aligning spaces so treats can fall through the gap.
Though the treat dispenser was perhaps the most consistently functional element of the system, there were initial setbacks where the entire reservoir would rotate with the base rather than remaining fixed, which didn’t allow treats to fall through. This could easily be remedied with a more secure setup, but it was loosely placed to facilitate opening and closing the box to fix wire connections during the debugging process. In most circumstances, however, when the dog was detected on the couch and the whistle sounded, the base would rotate and treats could be dispensed.

6.0	CONCLUSIONS
With its current functionality, this system cannot replace an owner working with and training the dog, but it may be a supplemental tool when teaching a dog to stay off furniture. Perhaps with more sophisticated image recognition or allowing for a margin of error in the recognition boundaries, the system could be further improved. Despite unanticipated setbacks, the system did ultimately perform according to its design and intention with some success. Given the scope and timeline of the course during which this project was developed, however, the Automated Dog Trainer can be an effective training assistant by encouraging the dog to stay off the couch.
 
APPENDIX/ATTACHMENTS
This project could not have been accomplished without existing open-source packages, modules, libraries, and models. The following were used to fulfill the needs of the system
•	simpleaudio: Python3 package providing asynchronous audio playback [1]
•	psutil: Python library used to monitor processes [2]
•	Tkinter: Python package to interface with GUI toolkit [3]
•	Pillow: Python imaging library [4]
•	OpenCV2: Python wrapper package for image recognition [5]
•	MobileNet-SSD-RealSense: image recognition model [6]
•	RPi.GPIO: Python module to control Raspberry Pi GPIO [7]
 
REFERENCES
[1] “Simpleaudio,” PyPI, https://pypi.org/project/simpleaudio/ (accessed Dec. 13, 2024). 
[2] “psutil,” PyPI, https://pypi.org/project/psutil/ (accessed Dec. 13, 2024). 
[3] “Tkinter - Python interface to TCL/TK,” Python documentation, https://docs.python.org/3/library/tkinter.html (accessed Dec. 13, 2024). 
[4] “Pillow,” PyPI, https://pypi.org/project/pillow/ (accessed Dec. 13, 2024). 
[5] “openCV-python,” PyPI, https://pypi.org/project/opencv-python/ (accessed Dec. 13, 2024).
[6] “MobileNet-SSD-RealSense,” GitHub, https://github.com/PINTO0309/MobileNet-SSD-RealSense/tree/master (accessed Dec. 13, 2024).
[7] “RPi.GPIO,” PyPI, https://pypi.org/project/RPi.GPIO/ (accessed Dec. 13, 2024). 
