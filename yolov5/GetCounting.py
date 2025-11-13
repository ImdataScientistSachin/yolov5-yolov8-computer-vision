# Import necessary libraries
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO

# --- Centroid Tracker Class (Helper) ---
# A robust tracker that assigns a unique ID to each detected object
# and tracks it across multiple frames based on its centroid.
class CentroidTracker:
    def __init__(self, maxDisappeared=50):
        """
        Initializes the centroid tracker.
        maxDisappeared: The maximum number of consecutive frames an object is allowed to be missing
                        before it is deregistered. A higher value is good for videos with occlusion or fast movement.
        """
        self.nextObjectID = 0  # The next unique ID to be assigned to a new object
        self.objects = {}      # A dictionary to store tracked objects: {ID: {'centroid': (x,y), 'rect': [x1,y1,x2,y2]}}
        self.disappeared = {}  # A dictionary to count consecutive disappeared frames for each object
        self.maxDisappeared = maxDisappeared

    def register(self, centroid, rect):
        """Registers a new object with a new ID."""
        self.objects[self.nextObjectID] = {'centroid': centroid, 'rect': rect}
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        """Deregisters an object ID when it disappears."""
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        """
        Updates the tracker with new detection rectangles from the current frame.
        rects: A list of bounding box rectangles in [x1, y1, x2, y2] format.
        """
        if len(rects) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects

        # Initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        # If no objects are currently being tracked, register all new input centroids
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i], rects[i])
        else:
            # Match existing objects to new input centroids
            objectIDs = list(self.objects.keys())
            objectCentroids = [obj['centroid'] for obj in self.objects.values()]

            # Compute the distance between each pair of existing object centroids and new input centroids
            D = np.array([[np.linalg.norm(np.array(pA) - np.array(pB)) for pB in inputCentroids] for pA in objectCentroids])

            # Find the smallest value in each row (closest new object for each existing one)
            rows = D.min(axis=1).argsort()

            # Find the index of the column with the minimum value for each row
            cols = D.argmin(axis=1)[rows]

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue

                objectID = objectIDs[row]
                self.objects[objectID]['centroid'] = inputCentroids[col]
                self.objects[objectID]['rect'] = rects[col]
                self.disappeared[objectID] = 0

                usedRows.add(row)
                usedCols.add(col)

            # Check for objects that have not been matched
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # Deregister objects that have disappeared
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
            else:
                # Register new objects that were not matched
                for col in unusedCols:
                    self.register(inputCentroids[col], rects[col])

        return self.objects

# --- Main Application Logic ---

# Hide the main tkinter window to show only the file dialog
root = tk.Tk()
root.withdraw()

# Open file dialog to select a video file
video_file_path = filedialog.askopenfilename(
    title="Select a Video File",
    filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
)

# Exit if no file is selected
if not video_file_path:
    print("No video file selected. Exiting.")
    exit()

# Initialize the video capture object with the selected file path
cap = cv2.VideoCapture(video_file_path)

if not cap.isOpened():
    print("Error: Could not open the selected video file.")
    exit()

# Load the YOLOv8 model. 'yolov8n.pt' is the nano version, fast and efficient.
# You can use 'yolov8s.pt' (small) for more accuracy at a slightly slower speed.
model = YOLO('yolov8n.pt')

# Initialize the Centroid Tracker with a higher maxDisappeared value for better tracking
ct = CentroidTracker(maxDisappeared=100)
total_people = 0

# Loop through each frame of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if the video has ended

    # Resize the frame for consistent processing and display
    frame = cv2.resize(frame, (640, 480))

    # Perform object detection using YOLOv8
    # 'verbose=False' to suppress the output of YOLO in the terminal
    results = model(frame, verbose=False)

    rects = []
    # Loop through the detection results
    for r in results:
        # Extract bounding box coordinates, class IDs, and confidence scores
        boxes = r.boxes.xyxy.cpu().numpy().astype(int)
        classes = r.boxes.cls.cpu().numpy()
        confidences = r.boxes.conf.cpu().numpy()
        
        for i in range(len(boxes)):
            cls = classes[i]
            confidence = confidences[i]
            
            # The class for "person" in YOLO's default model is 0
            if cls == 0:
                x1, y1, x2, y2 = boxes[i]
                w, h = x2 - x1, y2 - y1

                # Apply confidence and size filters for more reliable detections
                # You can adjust these values to suit your video's conditions
                if confidence > 0.3 and w * h > 500:
                    rects.append([x1, y1, x2, y2])
    
    # Update the centroid tracker with the filtered detections
    objects = ct.update(rects)

    # Count the number of people currently being tracked
    total_people = len(objects)

    # Loop over the tracked objects to draw bounding boxes and IDs
    for objectID in list(objects.keys()):
        obj_data = objects[objectID]
        centroid = obj_data['centroid']
        rect = obj_data['rect']
        (x, y, x2, y2) = rect
        w = x2 - x
        h = y2 - y
        
        # Draw the bounding box and object ID on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {objectID}", (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the total count of people
    cv2.putText(frame, f'Total People: {total_people}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Show the output frame 
    cv2.imshow("People Counter", frame)
    
    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Wait for a key press to keep the final window open
# This is useful for short videos, allowing you to see the final result.
cv2.waitKey(0)