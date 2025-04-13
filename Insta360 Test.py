import cv2
import numpy as np
import platform
import os
import AprilTag

def process_frame(tagdetector, frame):
    """
    This is where you can add your frame-by-frame processing.
    For now, we'll convert the frame to grayscale as a placeholder.
    Replace or extend this function with your own logic.
    """
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tagdetector.detect(frame, None)  # Detect tags in the grayscale image

    return frame

import platform
import os

def list_cameras():
    cameras = []
    
    if platform.system() == "Windows":
        from pygrabber.dshow_graph import FilterGraph
        graph = FilterGraph()
        devices = graph.get_input_devices()
        cameras = [(i, devices[i]) for i in range(len(devices))]
    
    elif platform.system() == "Linux":
        devices = os.popen("v4l2-ctl --list-devices").read().split("\n")
        cameras = [(i, devices[i]) for i in range(len(devices)) if devices[i]]
    
    return cameras

def list_cameras_by_index():
    index = 0
    available_cameras = []
    
    while True:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append((index, cap.getBackendName()))
            cap.release()
        else:
            break  # Stop checking when an index is not available
        index += 1
    
    return available_cameras

def main():

    print("Available Cameras:")
    for index, name in list_cameras():
        print(f"{index}: {name}")


    # Open the default video capture device (typically index 0).
    # If your Insta360 appears under a different index, change accordingly.

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open webcam device. Check your Insta360 connection and mode.")
        return

    tagDetector = AprilTag.AprilTag("tag36h11", 0.1651, None, None)

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame.")
            break

        # Apply processing to the captured frame.
        processed_frame = process_frame(tagDetector, frame)

        # Optionally, display both the original and processed frames.
        # If processed_frame is grayscale, we convert it to BGR for side-by-side display.
        # processed_colored = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
        # combined = np.hstack((frame, processed_colored))
        
        # cv2.imshow("Original (Left) | Processed (Right)", combined)
        cv2.imshow("Processed Frame", processed_frame)
        # Display the processed frame.
        # Exit loop when 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
