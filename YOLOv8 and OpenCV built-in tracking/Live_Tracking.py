#!/usr/bin/env python
# coding: utf-8

# ## YOLOv8 Security Tracker
# 
# 
# #### Tracking Suspicious Individuals Near a Home at Night with YOLOv8
# 
# ###### This tutorial demonstrates how to build an advanced security system using YOLOv8's object tracking capabilities. The system will detect people in a night-time video feed, track their movements, and trigger an alert if a person loiters for too long within a predefined "alert zone" (e.g., a driveway or porch).

# In[23]:


# install dependencies 

# ! pip install ultralytics opencv-python numpy ipywidgets


# ### Gpu configuration
# 


#  Imports and GPU Configuration

import cv2
import numpy as np
import torch
from ultralytics import YOLO
from collections import defaultdict
import time

# --- GPU Check and Device Configuration ---
# If a GPU is available, use it (device='cuda:0' or device=0), otherwise use 'cpu'

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {DEVICE}")



# ### Model Loading and Zone Configuration


#  Configuration
# Load the YOLOv8 model (using 'n' for speed, consider 's' or 'm' for better night accuracy)
# We specify the device to ensure the GPU is utilized for tracking
model = YOLO('yolov8n.pt')

# Path to your night-time video file
VIDEO_PATH = 'C:/Users/demog/Videos/Captures/'

# --- Define the Alert Zone Polygon ---
# IMPORTANT: Adjust these [x, y] coordinates to fit your video's perspective.
# This example defines a rectangular area for a driveway.

ALERT_ZONE_POLYGON = np.array([
    [100, 500], [800, 500], [850, 250], [50, 250]
], np.int32)

# Time in seconds a person can be in the zone before an alert is triggered
LOITERING_THRESHOLD_SECONDS = 5.0

# Dictionaries to store tracking data
# Stores the time a person FIRST entered the zone
loitering_timers = {}

# Stores the IDs of individuals who have triggered an alert
alert_triggered_ids = set()



# ### Main Tracking Loop and Alert Logic


#  Main Loop for Tracking, Zone Monitoring, and Alerts

# 🔧 PATH FIX: Using the direct path you provided.
cap = cv2.VideoCapture('C:/Users/demog/Videos/Captures/people walking.mp4')

# Check if video opened successfully
if not cap.isOpened():
    # 🔧 FIX: Correctly reference the specific path used by cap.read() here for the error message
    print(f"Error: Could not open video file at C:/Users/demog/Videos/Captures/people walking.mp4")
    # Instead of breaking, return if running in a notebook cell.
    # If this fails, go back and check the file path and codec.
    # return 

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run YOLOv8 tracking, explicitly using the set device (GPU)
    # The '0' class filter ensures we only track 'person' (COCO class ID 0)
    # 🔧 GMC FIX: We are relying on the user having set gmc: False in their bytetrack.yaml 
    # OR running the simplified call without explicitly referencing the tracker file.
    results = model.track(frame, persist=True, classes=0, device=DEVICE, verbose=False)

    # 🟢 CRITICAL SAFETY CHECK: Check if any tracks were detected in the current frame.
    # This prevents crashes when trying to access missing 'id' or 'xyxy' attributes.
    if results[0].boxes.id is None:
        # If no tracks were found, display the empty frame and continue to the next iteration.
        annotated_frame = results[0].plot()
        cv2.imshow("Suspicious Activity Tracker", annotated_frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
        continue # Skip the rest of the loitering logic and go to the next frame

    # Get the bounding boxes (xyxy format) and track IDs
    # Convert to CPU for OpenCV/Numpy processing if results are on GPU
    boxes_xyxy = results[0].boxes.xyxy.cpu().tolist()
    track_ids = results[0].boxes.id.int().cpu().tolist()

    # Create a temporary structure to hold current tracks for efficient access
    current_tracks = {}
    for box, track_id in zip(boxes_xyxy, track_ids):
        # x_min, y_min, x_max, y_max
        x1, y1, x2, y2 = [int(i) for i in box]

        # Use the center of the bottom edge (the person's "feet") for the zone check
        center_x = int((x1 + x2) / 2)
        center_y_feet = y2
        center_point = (center_x, center_y_feet)

        current_tracks[track_id] = {
            'box_xyxy': box,
            'center_point': center_point
        }

    # --- Loitering Logic ---
    current_ids_in_frame = set(current_tracks.keys())
    
    # Check for people who have left the frame/zone and remove their timer/alert
    ids_to_remove = set(loitering_timers.keys()) - current_ids_in_frame
    for track_id in ids_to_remove:
        if track_id in loitering_timers:
            del loitering_timers[track_id]
        if track_id in alert_triggered_ids:
            alert_triggered_ids.remove(track_id)

    for track_id, data in current_tracks.items():
        center_point = data['center_point']

        # Check if the person's 'feet' are inside the alert zone
        is_inside_zone = cv2.pointPolygonTest(ALERT_ZONE_POLYGON, center_point, False) >= 0

        if is_inside_zone:
            # 1. Start or check their timer
            if track_id not in loitering_timers:
                # First time this person is detected in the zone
                loitering_timers[track_id] = time.time()
            else:
                # Person is still in the zone, check duration
                elapsed_time = time.time() - loitering_timers[track_id]

                if elapsed_time > LOITERING_THRESHOLD_SECONDS:
                    # 2. Loitering detected! Trigger alert.
                    alert_triggered_ids.add(track_id)
        else:
            # If person leaves the zone, reset their timer
            if track_id in loitering_timers:
                del loitering_timers[track_id]


    # --- Visualization ---
    # Visualize the results using Ultralytics built-in plot function
    annotated_frame = results[0].plot()

    # Draw the alert zone polygon on the frame
    cv2.polylines(annotated_frame, [ALERT_ZONE_POLYGON], isClosed=True, color=(0, 255, 255), thickness=2)

    # Add visual alert text for tracked individuals who triggered the alert
    for track_id in alert_triggered_ids:
        
        # 🟢 KEY ERROR FIX: Check if the track ID is present in the current frame's tracks
        if track_id in current_tracks:
            # Get the latest box coordinates from the current_tracks dictionary
            x1, y1, _, _ = map(int, current_tracks[track_id]['box_xyxy'])
            
            # Draw the alert text slightly above the bounding box
            cv2.putText(annotated_frame, f"ALERT: Detected Person ID: {track_id}!", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            # If the track is lost, skip drawing the alert for this frame.
            pass


    # Display the annotated frame
    cv2.imshow("Suspicious Activity Tracker", annotated_frame)

    # ⏱️ WINDOW STABILITY FIX: Wait 50ms to keep the window open stably.
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
