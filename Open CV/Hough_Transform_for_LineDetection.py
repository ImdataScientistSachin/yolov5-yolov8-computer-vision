#!/usr/bin/env python
# coding: utf-8

# ## Hough Line Transform using Open CV
# 

# ###  The Hough Line Transform  (cv2.HoughLines)  is a feature extraction technique used to detect straight lines in images. It works by transforming points in the image space into a parameter space where lines can be identified as peaks in an accumulator matrix.
# 
# 
# #### How It Works
# 
# ##### Line Representation: Instead of using the slope-intercept form y=mx+c, which is problematic for vertical lines, the Hough Transform represents lines in polar coordinates as:  r=xcosθ+ysinθ   where  r is the perpendicular distance from the origin to the line, and  θ is the angle of the normal to the line relative to the x-axis.
#  
# ##### Accumulator Space: For each edge pixel  (x0 ,y0)  detected in the image (usually after edge detection like Canny), the transform calculates all possibl (r,θ) pairs that could represent lines passing through that point. Each pair votes in an accumulator matrix. Peaks in this matrix correspond to the most likely lines in the image.
# 
# ##### Detection: The algorithm identifies local maxima in the accumulator space, which correspond to the parameters (r,θ) of lines present in the image. From these parameters, the lines can be drawn or further processed.



# import library 

import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Scale, HORIZONTAL, messagebox
from PIL import Image, ImageTk



# ### ("Hough Transform Line Detection")


class LineDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hough Transform Line Detection")

        # Label to show instructions or status messages
        self.label = Label(root, text="Select an Image for Line Detection")
        self.label.pack(pady=10)

        # Button to open file dialog for image selection
        self.select_button = Button(root, text="Choose Image", command=self.select_image)
        self.select_button.pack(pady=10) # Adds 10 pixels vertical space above and below

        # Slider for Canny lower threshold
        self.canny_lower_scale = Scale(root, from_=50, to=150, orient=HORIZONTAL, label='Canny Lower Threshold')
        self.canny_lower_scale.set(100)
        self.canny_lower_scale.pack()

        # Slider for Canny upper threshold
        self.canny_upper_scale = Scale(root, from_=100, to=300, orient=HORIZONTAL, label='Canny Upper Threshold')
        self.canny_upper_scale.set(200)
        self.canny_upper_scale.pack()

        # Slider for Hough transform threshold (minimum votes)
        self.hough_thresh_scale = Scale(root, from_=50, to=300, orient=HORIZONTAL, label='Hough Threshold')
        self.hough_thresh_scale.set(100)
        self.hough_thresh_scale.pack()

        # Slider for aperture size used in Canny edge detection (must be odd and between 3 and 7)
        self.aperture_scale = Scale(root, from_=1, to=7, orient=HORIZONTAL, label='Canny Aperture Size (odd)')
        self.aperture_scale.set(3)
        self.aperture_scale.pack()

        # Button to trigger line detection
        self.detect_button = Button(root, text="Detect Lines", command=self.detect_lines)
        self.detect_button.pack()

        # Button to save the processed image with detected lines
        self.save_button = Button(root, text="Save Output Image", command=self.save_image, state='disabled')
        self.save_button.pack()

        # Label to display the processed image inside the GUI
        self.image_label = Label(root)
        self.image_label.pack()

        self.image_path = None  # Path of selected image
        self.processed_image = None  # Store processed image for display and saving

    def select_image(self):
        # Open file dialog to select an image file
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if self.image_path:
            self.label.config(text=f"Selected image: {self.image_path}")
            self.save_button.config(state='disabled')  # Disable save until detection is done
            self.image_label.config(image='')  # Clear displayed image
        else:
            self.label.config(text="No image selected")

    def detect_lines(self):
        if not self.image_path:
            self.label.config(text="No image selected!")
            return

        try:
            # Read the image from file
            image = cv2.imread(self.image_path)
            if image is None:
                raise ValueError("Failed to load image. Please select a valid image file.")

            # Resize image if too large for performance optimization (max width or height = 800 px)
            max_dim = 800
            height, width = image.shape[:2]
            if max(height, width) > max_dim:
                scale = max_dim / max(height, width)
                image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Get parameters from sliders
            canny_lower = self.canny_lower_scale.get()
            canny_upper = self.canny_upper_scale.get()
            # Aperture size must be odd and between 3 and 7
            aperture = self.aperture_scale.get()
            if aperture % 2 == 0:
                aperture += 1
            if aperture < 3:
                aperture = 3
            elif aperture > 7:
                aperture = 7

            # Apply Canny edge detection
            edges = cv2.Canny(gray, canny_lower, canny_upper, apertureSize=aperture)

            # Apply Standard Hough Line Transform
            lines = cv2.HoughLines(edges, 1, np.pi / 180, self.hough_thresh_scale.get())

            # Copy image to draw lines on
            output_image = image.copy()

            # Draw detected lines if any
            if lines is not None:
                for rho, theta in lines[:, 0]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))
                    cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Convert BGR to RGB for displaying in Tkinter
            rgb_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_image)

            # Convert to ImageTk PhotoImage
            imgtk = ImageTk.PhotoImage(image=pil_image)

            # Keep a reference to avoid garbage collection
            self.image_label.imgtk = imgtk

            # Update the label widget with the image
            self.image_label.config(image=imgtk)

            # Store processed image for saving
            self.processed_image = output_image

            self.label.config(text="Line detection completed.")
            self.save_button.config(state='normal')  # Enable save button

        except (cv2.error, ValueError) as e:
            # Handle OpenCV errors and invalid image errors gracefully
            messagebox.showerror("Error", f"Error processing image:\n{str(e)}")
            self.label.config(text="Error processing image. Please try another image.")
            self.processed_image = None
            self.save_button.config(state='disabled')
            self.image_label.config(image='')

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save.")
            return

        # Open file dialog to save the image
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg;*.jpeg"),
                                                            ("BMP files", "*.bmp")])
        if save_path:
            try:
                # Save the processed image to disk
                cv2.imwrite(save_path, self.processed_image)
                messagebox.showinfo("Saved", f"Image saved successfully:\n{save_path}")
            except cv2.error as e:
                messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = LineDetectionApp(root)
    root.mainloop()


# In[ ]:





# ### Probabilistic Hough Transform Line Detection
# 
# 
# ##### Probabilistic Hough Transform Line Detection" is an optimized variant that detects line segments efficiently by sampling edge points and returning segment endpoints directly.



class LineDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Probabilistic Hough Transform Line Detection")

        # Label to show instructions or status messages
        self.label = Label(root, text="Select an Image for Line Detection")
        self.label.pack()

        # Button to open file dialog for image selection
        self.select_button = Button(root, text="Choose Image", command=self.select_image)
        self.select_button.pack(pady=10)

        # Slider for Canny lower threshold
        self.canny_lower_scale = Scale(root, from_=50, to=150, orient=HORIZONTAL, label='Canny Lower Threshold')
        self.canny_lower_scale.set(100)
        self.canny_lower_scale.pack()

        # Slider for Canny upper threshold
        self.canny_upper_scale = Scale(root, from_=100, to=300, orient=HORIZONTAL, label='Canny Upper Threshold')
        self.canny_upper_scale.set(200)
        self.canny_upper_scale.pack()

        # Slider for Hough transform threshold (minimum votes)
        self.hough_thresh_scale = Scale(root, from_=10, to=300, orient=HORIZONTAL, label='Hough Threshold')
        self.hough_thresh_scale.set(100)
        self.hough_thresh_scale.pack()

        # Slider for minimum line length (pixels)
        self.min_line_length_scale = Scale(root, from_=10, to=300, orient=HORIZONTAL, label='Min Line Length')
        self.min_line_length_scale.set(50)
        self.min_line_length_scale.pack()

        # Slider for maximum line gap (pixels)
        self.max_line_gap_scale = Scale(root, from_=1, to=50, orient=HORIZONTAL, label='Max Line Gap')
        self.max_line_gap_scale.set(10)
        self.max_line_gap_scale.pack()

        # Slider for aperture size used in Canny edge detection (must be odd and between 3 and 7)
        self.aperture_scale = Scale(root, from_=1, to=7, orient=HORIZONTAL, label='Canny Aperture Size (odd)')
        self.aperture_scale.set(3)
        self.aperture_scale.pack()

        # Button to trigger line detection
        self.detect_button = Button(root, text="Detect Lines", command=self.detect_lines)
        self.detect_button.pack(pady=10)  # Adds 10 pixels vertical space above and below
        
        # Button to save the processed image with detected lines
        self.save_button = Button(root, text="Save Output Image", command=self.save_image, state='disabled')
        self.save_button.pack(pady=10) # Adds 10 pixels vertical space above and below

        # Label to display the processed image inside the GUI
        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        self.image_path = None  # Path of selected image
        self.processed_image = None  # Store processed image for display and saving

    def select_image(self):
        # Open file dialog to select an image file
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if self.image_path:
            self.label.config(text=f"Selected image: {self.image_path}")
            self.save_button.config(state='disabled')  # Disable save until detection is done
            self.image_label.config(image='')  # Clear displayed image
        else:
            self.label.config(text="No image selected")

    def detect_lines(self):
        if not self.image_path:
            self.label.config(text="No image selected!")
            return

        try:
            # Read the image from file
            image = cv2.imread(self.image_path)
            if image is None:
                raise ValueError("Failed to load image. Please select a valid image file.")

            # Resize image if too large for performance optimization (max width or height = 800 px)
            max_dim = 800
            height, width = image.shape[:2]
            if max(height, width) > max_dim:
                scale = max_dim / max(height, width)
                image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Get parameters from sliders
            canny_lower = self.canny_lower_scale.get()
            canny_upper = self.canny_upper_scale.get()
            aperture = self.aperture_scale.get()
            if aperture % 2 == 0:
                aperture += 1
            if aperture < 3:
                aperture = 3
            elif aperture > 7:
                aperture = 7

            # Apply Canny edge detection
            edges = cv2.Canny(gray, canny_lower, canny_upper, apertureSize=aperture)

            # Get Probabilistic Hough parameters
            threshold = self.hough_thresh_scale.get()
            min_line_length = self.min_line_length_scale.get()
            max_line_gap = self.max_line_gap_scale.get()

            # Apply Probabilistic Hough Line Transform
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold,
                                    minLineLength=min_line_length,
                                    maxLineGap=max_line_gap)

            # Copy image to draw lines on
            output_image = image.copy()

            # Draw detected line segments if any
            if lines is not None:
                for x1, y1, x2, y2 in lines[:, 0]:
                    cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Convert BGR to RGB for displaying in Tkinter
            rgb_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_image)

            # Convert to ImageTk PhotoImage
            imgtk = ImageTk.PhotoImage(image=pil_image)

            # Keep a reference to avoid garbage collection
            self.image_label.imgtk = imgtk

            # Update the label widget with the image
            self.image_label.config(image=imgtk)

            # Store processed image for saving
            self.processed_image = output_image

            self.label.config(text="Line detection completed.")
            self.save_button.config(state='normal')  # Enable save button

        except (cv2.error, ValueError) as e:
            messagebox.showerror("Error", f"Error processing image:\n{str(e)}")
            self.label.config(text="Error processing image. Please try another image.")
            self.processed_image = None
            self.save_button.config(state='disabled')
            self.image_label.config(image='')

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg;*.jpeg"),
                                                            ("BMP files", "*.bmp")])
        if save_path:
            try:
                cv2.imwrite(save_path, self.processed_image)
                messagebox.showinfo("Saved", f"Image saved successfully:\n{save_path}")
            except cv2.error as e:
                messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = LineDetectionApp(root)
    root.mainloop()
