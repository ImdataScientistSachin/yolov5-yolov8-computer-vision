#!/usr/bin/env python
# coding: utf-8

# ## Face detection using Open CV

# ### advanced face detection using a graphical user interface (GUI) built with Tkinter and OpenCV. The application supports both image and video face detection, allows parameter tuning, and persists user settings in a JSON fil


# --- 1. SETTING THE STAGE ---
# Let's bring in the heavy lifters. 
# OpenCV does the computer vision magic, Tkinter builds the window, 
# and PIL helps us show those OpenCV images inside the Tkinter window.

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import json
import threading # We need this so the video loop doesn't freeze the buttons
import os

# --- 2. CONFIGURATION ---
# Pointing to the "brain" of the operation. 
# This ONNX file contains the pre-trained neural network we need.
YUNET_MODEL_PATH = "face_detection_yunet_2023mar.onnx"
YUNET_INPUT_SIZE = (320, 320)  # The model was trained on this size, so it likes this default.

class FaceDetectionApp:
    def __init__(self, root):
        # Setting up the main window frame
        self.root = root
        self.root.title("YuNet Face Detection App")
        self.root.geometry("800x900") # A nice tall window

        # Making it look a bit modern with the 'clam' theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # --- IMPORTANT: CONNECTING VARIABLES ---
        # We define these Tkinter variables here so the UI inputs (sliders/entries)
        # stay in sync with the actual values we use for detection.
        self.conf_threshold = tk.DoubleVar(value=0.9) # How sure does the AI need to be? (90%)
        self.nms_threshold = tk.DoubleVar(value=0.3)  # How much overlap is allowed?
        self.top_k = tk.IntVar(value=5000)            # Max faces to keep
        # ------------------------------------------------------------

        # Creating the tabs so the UI isn't cluttered
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Creating the three "pages" of our app
        self.image_tab = ttk.Frame(self.notebook)
        self.video_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.image_tab, text="Image Processing")
        self.notebook.add(self.video_tab, text="Video Processing")
        self.notebook.add(self.settings_tab, text="Settings")

        # Calling helper functions to draw the buttons on each tab
        self.setup_image_tab()
        self.setup_video_tab()
        self.setup_settings_tab()

        # Placeholders for our data
        self.image = None
        self.orig_image = None
        self.video_capture = None
        self.is_processing_video = False

        # --- SAFETY CHECKS ---
        # Before we start, let's make sure the user actually has the model file.
        # If not, crash gracefully and tell them where to get it.
        if not os.path.isfile(YUNET_MODEL_PATH):
            messagebox.showerror("Model Error", f"YuNet model not found at {YUNET_MODEL_PATH}.\n"
                                                "Download from OpenCV Zoo and place in this directory.")
            self.root.destroy()
            return

        # Making sure OpenCV is new enough to handle this specific AI model
        if not hasattr(cv2, "FaceDetectorYN"):
            messagebox.showerror("OpenCV Error", "Your OpenCV version does not support FaceDetectorYN. "
                                                 "Please upgrade to OpenCV >= 4.5.4.")
            self.root.destroy()
            return

        # If we passed the checks, let's wake up the AI detector!
        self.face_detector = cv2.FaceDetectorYN.create(
            YUNET_MODEL_PATH, "",
            YUNET_INPUT_SIZE,
            self.conf_threshold.get(),
            self.nms_threshold.get(),
            self.top_k.get()
        )
        
        # Try to load previous user preferences if they exist
        self.load_settings()

    def setup_image_tab(self):
        # Just setting up the buttons for the first tab. 
        # Notice we disable 'Detect' and 'Save' until an image is actually uploaded.
        self.upload_button = ttk.Button(self.image_tab, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.detect_button = ttk.Button(self.image_tab, text="Detect Faces", command=self.detect_faces,
                                        state=tk.DISABLED)
        self.detect_button.pack(pady=10)

        self.save_button = ttk.Button(self.image_tab, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.display_label = ttk.Label(self.image_tab)
        self.display_label.pack(expand=True)

    def setup_video_tab(self):
        # Setup for the webcam/video tab. 
        # Default source is "0" (the primary webcam).
        self.video_source = tk.StringVar(value="0")
        self.video_source_entry = ttk.Entry(self.video_tab, textvariable=self.video_source)
        self.video_source_entry.pack(pady=10)

        self.start_video_button = ttk.Button(self.video_tab, text="Start Video Processing",
                                             command=self.start_video_processing)
        self.start_video_button.pack(pady=10)

        self.stop_video_button = ttk.Button(self.video_tab, text="Stop Video Processing",
                                            command=self.stop_video_processing, state=tk.DISABLED)
        self.stop_video_button.pack(pady=10)

        self.video_label = ttk.Label(self.video_tab)
        self.video_label.pack(expand=True)

    def setup_settings_tab(self):
        # A simple grid layout for tweaking the AI parameters.
        ttk.Label(self.settings_tab, text="Confidence Threshold (0.0-1.0):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.settings_tab, textvariable=self.conf_threshold).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.settings_tab, text="NMS Threshold (0.0-1.0):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.settings_tab, textvariable=self.nms_threshold).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.settings_tab, text="Top K:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.settings_tab, textvariable=self.top_k).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.settings_tab, text="Save Settings", command=self.save_settings).grid(row=3, column=0,
                                                                                             columnspan=2, padx=5,
                                                                                             pady=5)

    def upload_image(self):
        # Open file explorer -> User picks image -> We load it into memory
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            # Keep a clean copy in case we want to reset or re-detect later
            self.orig_image = self.image.copy()
            self.show_image(self.image)
            # Now that we have an image, we can enable the other buttons
            self.detect_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.DISABLED)

    def detect_faces(self):
        # The main logic for static images.
        if self.image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        # Always work on a fresh copy of the original so we don't draw boxes over boxes
        img = self.orig_image.copy()
        height, width = img.shape[:2]
        
        # We have to tell the AI the size of the image every time, 
        # just in case the new image is different from the last one.
        self.face_detector.setInputSize((width, height))
        
        # Run the detection!
        _, faces = self.face_detector.detect(img)
        
        if faces is not None:
            # Loop through every face found
            for face in faces:
                # Get the coordinates for the box (x, y, width, height)
                x1, y1, w, h = face[:4].astype(int)
                # Draw the blue box
                cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
                
                # Draw the 5 facial landmarks (eyes, nose, mouth corners)
                # Loop 5 times, grab coordinates, draw green dots.
                for i in range(5):
                    lx, ly = int(face[4 + i * 2]), int(face[4 + i * 2 + 1])
                    cv2.circle(img, (lx, ly), 2, (0, 255, 0), -1)
        
        # Update the variable and refresh the display
        self.image = img
        self.show_image(self.image)
        self.save_button.config(state=tk.NORMAL)

    def show_image(self, cv_img):
        # OpenCV uses BGR colors, but Tkinter/PIL likes RGB. We have to swap them.
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(cv_img_rgb)
        
        # Resize it so it fits nicely in our GUI window
        img_pil = img_pil.resize((600, 600), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        # Important hack: We have to keep a reference (.imgtk) or garbage collection eats the image
        self.display_label.imgtk = img_tk
        self.display_label.configure(image=img_tk)

    def save_image(self):
        if self.image is None:
            messagebox.showwarning("Warning", "No processed image to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, self.image)
            messagebox.showinfo("Success", "Image saved successfully!")

    def start_video_processing(self):
        # Check if user typed a number (webcam index) or a file path string
        try:
            source = int(self.video_source.get())
        except ValueError:
            source = self.video_source.get()

        self.video_capture = cv2.VideoCapture(source)
        if not self.video_capture.isOpened():
            messagebox.showerror("Error", "Could not open video source")
            return

        self.is_processing_video = True
        
        # Swap button states so user can't click 'Start' twice
        self.start_video_button.config(state=tk.DISABLED)
        self.stop_video_button.config(state=tk.NORMAL)

        # --- THREADING EXPLAINED ---
        # If we run the video loop in the main thread, the GUI will freeze 
        # and become unresponsive. So, we send the video work to a background thread.
        threading.Thread(target=self.process_video, daemon=True).start()

    def stop_video_processing(self):
        # Kill the loop flag
        self.is_processing_video = False
        # Release the camera so other apps can use it
        if self.video_capture:
            self.video_capture.release()
        
        # Reset buttons
        self.start_video_button.config(state=tk.NORMAL)
        self.stop_video_button.config(state=tk.DISABLED)

    def process_video(self):
        # This loop runs in the background thread
        while self.is_processing_video:
            ret, frame = self.video_capture.read()
            if not ret:
                break # Stop if the video ends or camera disconnects
            
            # Similar logic to static image detection
            height, width = frame.shape[:2]
            self.face_detector.setInputSize((width, height))
            _, faces = self.face_detector.detect(frame)
            
            if faces is not None:
                for face in faces:
                    x1, y1, w, h = face[:4].astype(int)
                    cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
                    for i in range(5):
                        lx, ly = int(face[4 + i * 2]), int(face[4 + i * 2 + 1])
                        cv2.circle(frame, (lx, ly), 2, (0, 255, 0), -1)
            
            # Send the processed frame to the GUI
            self.show_video_frame(frame)
        
        # Cleanup the label when done
        self.video_label.configure(image=None)

    def show_video_frame(self, frame):
        # Same logic as show_image, but for video frames
        cv_img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(cv_img_rgb)
        img_pil = img_pil.resize((600, 600), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        self.video_label.imgtk = img_tk
        self.video_label.configure(image=img_tk)

    def save_settings(self):
        # Bundle up the values into a dictionary
        settings = {
            "conf_threshold": self.conf_threshold.get(),
            "nms_threshold": self.nms_threshold.get(),
            "top_k": self.top_k.get()
        }
        # Dump it to a JSON file so we remember it next time
        with open("face_detection_settings.json", "w") as f:
            json.dump(settings, f)
        messagebox.showinfo("Success", "Settings saved successfully!")
        
        # Don't forget to update the running detector with the new values immediately!
        self.face_detector = cv2.FaceDetectorYN.create(
            YUNET_MODEL_PATH, "",
            YUNET_INPUT_SIZE,
            self.conf_threshold.get(),
            self.nms_threshold.get(),
            self.top_k.get()
        )

    def load_settings(self):
        try:
            # Try to read the file. If it doesn't exist, just ignore and use defaults.
            with open("face_detection_settings.json", "r") as f:
                settings = json.load(f)
            # Use .get() to provide a fallback value if the key is missing in the file
            self.conf_threshold.set(settings.get("conf_threshold", 0.9))
            self.nms_threshold.set(settings.get("nms_threshold", 0.3))
            self.top_k.set(settings.get("top_k", 5000))
        except FileNotFoundError:
            pass # No settings file? No problem.

def main():
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop() # Start the event loop (wait for clicks)

if __name__ == "__main__":
    main()