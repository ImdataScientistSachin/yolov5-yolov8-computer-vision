#!/usr/bin/env python
# coding: utf-8

# ##  OpenCV-based object tracking


# #### This script allows a user to select an object tracking algorithm, then tracks a selected object in a video file or webcam stream using OpenCV's tracking APIs.




##Tracker Algorithms Overview

# BOOSTING: Based on AdaBoost algorithm, older and slower.

# MIL (Multiple Instance Learning): Robust to partial occlusions.

# KCF (Kernelized Correlation Filters): Fast and accurate, widely used.

# TLD (Tracking, Learning and Detection): Handles long-term tracking but less robust.

# MEDIANFLOW: Good for predictable motion, fails with fast movements.

# MOSSE: Very fast but less accurate.

# CSRT (Discriminative Correlation Filter with Channel and Spatial Reliability): High accuracy, slower than KCF.



# import libraries 

import cv2
print(cv2.__version__)
print(hasattr(cv2, 'TrackerKCF_create'))

import sys
import time
import cv2
import time

def is_legacy_tracker(tracker_type):
    """
    Check if the tracker type belongs to the legacy module.
    """
    legacy_trackers = {'BOOSTING', 'TLD', 'MEDIANFLOW', 'MOSSE'}
    return tracker_type in legacy_trackers

def select_tracker(tracker_type):
    """
    Create and return an OpenCV tracker object based on the tracker type.
    Handles compatibility between legacy and new tracker APIs.
    Raises ValueError for unsupported tracker types.
    """
    try:
        if is_legacy_tracker(tracker_type):
            if tracker_type == 'BOOSTING':
                return cv2.legacy.TrackerBoosting_create()
            elif tracker_type == 'TLD':
                return cv2.legacy.TrackerTLD_create()
            elif tracker_type == 'MEDIANFLOW':
                return cv2.legacy.TrackerMedianFlow_create()
            elif tracker_type == 'MOSSE':
                return cv2.legacy.TrackerMOSSE_create()
        else:
            if tracker_type == 'MIL':
                return cv2.TrackerMIL_create()
            elif tracker_type == 'KCF':
                return cv2.TrackerKCF_create()
            elif tracker_type == 'CSRT':
                return cv2.TrackerCSRT_create()
        raise ValueError(f"Unsupported tracker type: {tracker_type}")
    except AttributeError as e:
        raise RuntimeError(f"Tracker {tracker_type} is not supported in your OpenCV installation.") from e

def get_tracker_choice(tracker_types):
    """
    Display tracker options and get validated user choice.
    Returns the selected tracker type string.
    """
    while True:
        print("Select tracker type:")
        for i, t_type in enumerate(tracker_types, start=1):
            print(f"{i}. {t_type}")
        choice = input("Enter tracker number: ")
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        choice = int(choice)
        if 1 <= choice <= len(tracker_types):
            return tracker_types[choice - 1]
        else:
            print(f"Please enter a number between 1 and {len(tracker_types)}.")

def get_video_source():
    """
    Prompt user for video file path or use webcam if blank.
    Returns a cv2.VideoCapture object.
    """
    video_path = input("Enter video file path (leave blank for webcam): ").strip()
    if video_path == '':
        video = cv2.VideoCapture(0)
    else:
        video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError("Error: Could not open video source.")
    return video

def select_roi_frame(video):
    """
    Read the first frame from video and allow user to select ROI.
    Returns the frame and the bounding box.
    """
    ok, frame = video.read()
    if not ok or frame is None:
        raise IOError("Error: Could not read frame from video.")
    bbox = cv2.selectROI("Select ROI", frame, False, False)
    cv2.destroyWindow("Select ROI")
    # Improved ROI validation
    if bbox[2] <= 0 or bbox[3] <= 0:
        raise ValueError("Invalid ROI selected. Please select a valid object region.")
    return frame, bbox

def draw_tracking_info(frame, bbox, tracker_type, tracking_ok):
    """
    Draw bounding box and status text on the frame.
    """
    if tracking_ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.putText(frame, f"{tracker_type} Tracker", (50, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    cv2.putText(frame, "ESC to quit", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

def main():
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']

    try:
        tracker_type = get_tracker_choice(tracker_types)
        tracker = select_tracker(tracker_type)
        video = get_video_source()
        frame, bbox = select_roi_frame(video)

        # Debug info for ROI and frame
        print(f"Selected bbox: {bbox}")
        print(f"Frame shape: {frame.shape}")

        # Initialize tracker with first frame and bounding box
        init_ok = tracker.init(frame, bbox)
        if not init_ok:
            print("Error: Tracker initialization failed. Try selecting a clearer or larger ROI.")
            return  # Use return instead of sys.exit() for Jupyter compatibility

        fps = 0.0
        prev_time = time.time()

        while True:
            ok, frame = video.read()
            if not ok or frame is None:
                print("End of video stream or cannot read the frame.")
                break

            tracking_ok, bbox = tracker.update(frame)
            draw_tracking_info(frame, bbox, tracker_type, tracking_ok)

            current_time = time.time()
            fps = 0.9 * fps + 0.1 * (1 / (current_time - prev_time))
            prev_time = current_time
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Tracking", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                print("ESC pressed. Exiting.")
                break

    except (ValueError, IOError, RuntimeError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        if 'video' in locals():
            video.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


# For speed (real-time): Use MOSSE or KCF.

# For accuracy and robustness: Use CSRT.

# For simple, slow-moving objects: MedianFlow is very precise.

# For occlusion handling: MIL or TLD.

# 
# For legacy or compatibility: BOOSTING.
