#!/usr/bin/env python
# coding: utf-8

# ## live GrayScale Converter using OpenCV

# import necessary Libraries 

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
from tkinter import filedialog


class LiveVideoApp:
    """
    Features:
        - Embeds live video feed directly in the Tkinter window.
        - Allows switching between multiple filters (None, Greyscale, Blur, Edge).
        - Handles camera access and frame retrieval errors gracefully.
        - Manages webcam resource allocation robustly.
    """

    def __init__(self, root):
        """
        Initialize the application UI and state.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Live Video Filter App")

        self.cap = None  # OpenCV VideoCapture object
        self.recording = False
        self.video_writer = None
        self.running = False  # Flag indicating if video capture is running
        self.current_filter = tk.StringVar(value="Greyscale")  # Selected filter

        self.setup_ui()

    def setup_ui(self):
        """
        Set up the GUI components: video panel, filter controls, and buttons.
        """
        # Label to display the video frames
        self.video_panel = tk.Label(self.root)
        self.video_panel.pack(padx=10, pady=10)

        # Frame for filter selection radio buttons
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(padx=10, pady=5, fill='x')
        filters = ["None", "Greyscale", "Blur", "Edge"]
        for f in filters:
            ttk.Radiobutton(filter_frame, text=f, variable=self.current_filter, value=f).pack(side='left', padx=5)

        # Frame for Start and Stop buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start_video)
        self.start_btn.pack(side='left', padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_video, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        self.record_btn = ttk.Button(btn_frame, text="Start Recording", command=self.toggle_recording, state='disabled')
        self.record_btn.pack(side='left', padx=5)

    def start_video(self):
        """
        Start video capture and display. Handles webcam access errors.
        """
        if self.running:
            return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot access webcam.")
            self.cap.release()
            self.cap = None
            return
        self.running = True
        self.record_btn.config(state='normal')
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.update_frame()

    def stop_video(self):
        """
        Stop video capture, release resources, and clear the video panel.
        """
        self.running = False
        self.stop_recording()
        self.record_btn.config(state='disabled')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_panel.config(image='')  # Clear the video display

    def toggle_recording(self):
        """
        Start or stop recording the live video. Prompts user for file location when starting.
        """
        if not self.recording:
            # Start recording
            filename = filedialog.asksaveasfilename(
                defaultextension=".avi",
                filetypes=[("AVI files", "*.avi"), ("All files", "*.*")],
                title="Save Video As"
            )
            if not filename:
                return  # User cancelled
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 20  # fallback to 20 if FPS is 0
            self.video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
            self.recording = True
            self.record_btn.config(text="Stop Recording")
            messagebox.showinfo("Recording", f"Recording started.\nSaving to: {filename}")
        else:
            # Stop recording
            self.stop_recording()

    def stop_recording(self):
        """
        Stop recording and release the video writer if active.
        """
        if self.recording and self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            self.recording = False
            self.record_btn.config(text="Start Recording")
            messagebox.showinfo("Recording", "Recording stopped and saved.")

    def apply_filter(self, frame):
        """
        Apply the selected filter to the input frame.

        Args:
            frame (np.ndarray): The input BGR frame from OpenCV.

        Returns:
            np.ndarray: The processed frame.
        """
        filter_type = self.current_filter.get()
        if filter_type == "Greyscale":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "Blur":
            frame = cv2.GaussianBlur(frame, (15, 15), 0)
        elif filter_type == "Edge":
            frame = cv2.Canny(frame, 100, 200)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        # "None" returns the original frame
        return frame

    def update_frame(self):
        """
        Capture a frame from the webcam, apply the selected filter, and update the video panel.
        Handles frame retrieval errors.
        """
        if not self.running or not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.stop_video()
            messagebox.showerror("Error", "Failed to retrieve frame from webcam.")
            return

        if self.recording and self.video_writer:
            self.video_writer.write(frame)

        frame = self.apply_filter(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert for PIL
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_panel.imgtk = imgtk  # Prevent garbage collection
        self.video_panel.config(image=imgtk)
        self.root.after(15, self.update_frame)  # Schedule next frame update

    def on_closing(self):
        """
        Handle application exit: stop video and close the window.
        """
        self.stop_video()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Only ONE root window
    app = LiveVideoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
