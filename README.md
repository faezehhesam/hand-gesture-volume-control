# Hand Gesture Volume Control

This Python script allows users to control their system volume using hand gestures detected by a webcam. It leverages the `pycaw` library for audio control and a custom `HandTrackingmodule` for hand gesture detection.

## Features

- **Hand Gesture Detection**: Detects hand gestures to control the system volume.
- **Volume Adjustment**: Adjusts system volume based on the distance between the thumb and index finger.
- **Real-time Feedback**: Displays current volume level and gesture status on a live video feed.
- **Performance Monitoring**: Shows frame rate (FPS) for real-time performance tracking.

## Prerequisites


Ensure the following dependencies are installed:

- `opencv-python` for video capture and image processing.
- `numpy` for numerical operations.
- `HandTrackingmodule` for hand detection and gesture recognition (ensure this module is implemented or available).
- `pycaw` for system audio control.
- `psutil` (optional) for system resource monitoring.

Install the required packages using pip:

```bash
pip install opencv-python numpy pycaw psutil comtypes


```
## Usage

1. **Setup**: Ensure your webcam is connected and functioning correctly.

2. **Run the Script**: Execute the script using Python:

    ```bash
    python hand_gesture_volume_control.py
    ```

3. **Control Volume**: Position your hand in front of the webcam and adjust the distance between your thumb and index finger to change the system volume. The current volume level and status will be displayed on the video feed.

4. **Exit**: Press 'q' to quit the program.

## Code Overview

### Initialization

1. **Camera Setup**:
    - Set the resolution of the webcam.
    - Initialize video capture.

2. **Hand Detector**:
    - Initialize the hand detector with a confidence level and maximum number of hands.

3. **Audio Control**:
    - Use `pycaw` to access the audio endpoint and control volume.
    - Retrieve volume range and set initial volume values.

### Main Loop

1. **Capture Frame**:
    - Read frames from the webcam.

2. **Hand Detection**:
    - Detect hand landmarks and bounding box.
    - Calculate the bounding box area.

3. **Gesture Interpretation**:
    - Compute the distance between the thumb and index finger.
    - Map this distance to the volume range and smooth adjustments.

4. **Volume Control**:
    - Check if the pinky finger is down to set the volume.
    - Update the system volume.

5. **Visualization**:
    - Draw volume bar and percentage on the video feed.
    - Display current FPS.

6. **Exit Condition**:
    - Press 'q' to break the loop and exit.

### Cleanup

- Release video capture and close all OpenCV windows.

## Troubleshooting

- **Hand Not Detected**: Ensure proper lighting and position your hand clearly within the camera's view.
- **Volume Not Changing**: Verify audio endpoint settings and ensure no other applications are interfering with volume control.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- **HandTrackingmodule**: Ensure this custom module for hand detection is implemented and available.
- **pycaw**: For providing an interface to control system audio.

Feel free to contribute or open issues if you encounter problems or have suggestions for improvements.
