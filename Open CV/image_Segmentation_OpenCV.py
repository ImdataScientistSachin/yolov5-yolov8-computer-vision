#!/usr/bin/env python
# coding: utf-8

# ## Image Segmentation using OpenCV
# 
# 
# ##### This script is an interactive image segmentation tool that lets users select an image file through a GUI, then processes the image using OpenCV's watershed segmentation algorithm, and finally displays the segmented image.



# import libraaries 

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import  Button, Label, Scale, HORIZONTAL, OptionMenu, StringVar
from PIL import Image, ImageTk
import threading



# Globals to hold parameters and image

threshold_factor = 0.7
kernel_size = 3
original_image = None
segmented_img = None


def select_image():
    global original_image, segmented_img
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    # Load image and convert to RGB
    original_image = cv2.imread(filepath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # Perform initial segmentation and display
    update_segmentation()

# core image processing function performing segmentation.
def segment_image(image, thresh_factor, k_size):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #Converts the RGB image to grayscale, simplifying the image to one channel for thresholding.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((k_size, k_size), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, thresh_factor * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]
    return image

def display_segmented_image_tk(image):
    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=im)
    if hasattr(display_segmented_image_tk, "img_label"):
        display_segmented_image_tk.img_label.configure(image=imgtk)
        display_segmented_image_tk.img_label.image = imgtk
    else:
        display_segmented_image_tk.img_label = Label(app, image=imgtk)
        display_segmented_image_tk.img_label.image = imgtk
        display_segmented_image_tk.img_label.pack(pady=10)

def update_segmentation(event=None):
    global segmented_img, threshold_factor, kernel_size, original_image
    if original_image is None:
        return
    # Run segmentation with current slider values
    segmented_img = segment_image(original_image.copy(), threshold_factor, kernel_size)
    display_segmented_image_tk(segmented_img)

def save_image():
    global segmented_img
    if segmented_img is None:
        messagebox.showwarning("Warning", "No segmented image to save!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if save_path:
        save_img = cv2.cvtColor(segmented_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, save_img)
        messagebox.showinfo("Success", f"Image saved to {save_path}")

def on_threshold_change(val):
    global threshold_factor
    threshold_factor = float(val)
    update_segmentation()

def on_kernel_change(val):
    global kernel_size
    kernel_size = int(val)
    update_segmentation()



# Tkinter GUI setup
app = tk.Tk()
app.title("Real-Time Image Segmentation Tool")

Label(app, text="Select an image to perform segmentation.").pack(pady=5)
Button(app, text="Select Image", command=select_image).pack(pady=5)

Label(app, text="Distance Transform Threshold Factor:").pack()
thresh_slider = Scale(app, from_=0.1, to=1.0, resolution=0.05, orient=HORIZONTAL,
                      command=on_threshold_change)
thresh_slider.set(threshold_factor)
thresh_slider.pack(pady=5)

Label(app, text="Morphological Kernel Size:").pack()
kernel_slider = Scale(app, from_=1, to=10, orient=HORIZONTAL, command=on_kernel_change)
kernel_slider.set(kernel_size)
kernel_slider.pack(pady=5)

Button(app, text="Save Segmented Image", command=save_image).pack(pady=10)

app.geometry("400x650")
app.mainloop()



# ##  advanced Image Segmentation



import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Button, Label, Scale, HORIZONTAL, OptionMenu, StringVar
from PIL import Image, ImageTk
import threading



# Global variables to store image data and processing state
original_image = None      # Stores the input image as a NumPy array
segmented_img = None       # Stores the segmented output image
processing_thread = None   # Reference to the current processing thread

# Default parameters for segmentation and GUI controls
segmentation_method = "Watershed" # Default segmentation method
threshold_factor = 0.7            # Threshold factor for Watershed/Global Threshold
kernel_size = 3                   # Kernel size for morphological operations
adaptive_block_size = 11          # Block size for Adaptive Threshold (must be odd)
adaptive_C = 2                    # Constant subtracted in Adaptive Threshold




def select_image():
    """Open a file dialog to select an image, load it, and start segmentation."""
    global original_image
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    # Load image and convert from BGR (OpenCV default) to RGB
    original_image = cv2.imread(filepath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    start_segmentation_thread()  # Start segmentation in a separate thread

def segment_image(image):
    """
    Perform segmentation on the input image based on the selected method and parameters.
    Returns the segmented image.
    """
    global segmentation_method, threshold_factor, kernel_size, adaptive_block_size, adaptive_C

    # Convert input image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    if segmentation_method == "Global Threshold":
        # Simple global thresholding using a fixed threshold value
        _, thresh = cv2.threshold(gray, int(threshold_factor * 255), 255, cv2.THRESH_BINARY)
        segmented = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    elif segmentation_method == "Adaptive Threshold":
        # Adaptive thresholding (Gaussian), block size must be odd
        block = adaptive_block_size if adaptive_block_size % 2 == 1 else adaptive_block_size + 1
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, block, adaptive_C)
        segmented = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    else:  # Watershed (default)
        # Watershed segmentation for separating touching objects
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, threshold_factor * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(image, markers)
        image[markers == -1] = [255, 0, 0]  # Mark boundaries in red
        segmented = image

    return segmented

def display_segmented_image_tk(image):
    """
    Display the segmented image inside the Tkinter window using PIL and ImageTk.
    """
    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=im)
    # If label already exists, update it; otherwise, create it
    if hasattr(display_segmented_image_tk, "img_label"):
        display_segmented_image_tk.img_label.configure(image=imgtk)
        display_segmented_image_tk.img_label.image = imgtk
    else:
        display_segmented_image_tk.img_label = Label(app, image=imgtk)
        display_segmented_image_tk.img_label.image = imgtk
        display_segmented_image_tk.img_label.pack(pady=10)

def start_segmentation_thread():
    """
    Start the segmentation process in a background thread to keep the GUI responsive.
    """
    global processing_thread
    if original_image is None:
        return
    disable_controls()  # Disable controls during processing
    # Start segmentation in a new thread
    processing_thread = threading.Thread(target=run_segmentation)
    processing_thread.start()

def run_segmentation():
    """
    The worker function for the background thread.
    Performs segmentation and schedules GUI update.
    """
    global segmented_img
    try:
        segmented_img = segment_image(original_image.copy())
        # Use Tkinter's after() to safely update GUI from the main thread
        app.after(0, on_segmentation_complete)
    except Exception as e:
        app.after(0, lambda: messagebox.showerror("Error", str(e)))

def on_segmentation_complete():
    """
    Callback after segmentation is done.
    Displays the result and re-enables controls.
    """
    display_segmented_image_tk(segmented_img)
    enable_controls()

def disable_controls():
    """Disable all interactive controls during processing."""
    select_button.config(state="disabled")
    save_button.config(state="disabled")
    thresh_slider.config(state="disabled")
    kernel_slider.config(state="disabled")
    adaptive_block_slider.config(state="disabled")
    adaptive_c_slider.config(state="disabled")
    method_menu.config(state="disabled")

def enable_controls():
    """Re-enable all interactive controls after processing."""
    select_button.config(state="normal")
    save_button.config(state="normal")
    thresh_slider.config(state="normal")
    kernel_slider.config(state="normal")
    adaptive_block_slider.config(state="normal")
    adaptive_c_slider.config(state="normal")
    method_menu.config(state="normal")

def save_image():
    """
    Save the segmented image to disk using a file dialog.
    """
    global segmented_img
    if segmented_img is None:
        messagebox.showwarning("Warning", "No segmented image to save!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if save_path:
        save_img = cv2.cvtColor(segmented_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, save_img)
        messagebox.showinfo("Success", f"Image saved to {save_path}")

def on_threshold_change(val):
    """Update threshold factor and re-run segmentation when slider changes."""
    global threshold_factor
    threshold_factor = float(val)
    start_segmentation_thread()

def on_kernel_change(val):
    """Update kernel size and re-run segmentation when slider changes."""
    global kernel_size
    kernel_size = int(val)
    start_segmentation_thread()

def on_adaptive_block_change(val):
    """Update adaptive block size and re-run segmentation when slider changes."""
    global adaptive_block_size
    adaptive_block_size = int(val)
    start_segmentation_thread()

def on_adaptive_c_change(val):
    """Update adaptive C value and re-run segmentation when slider changes."""
    global adaptive_C
    adaptive_C = int(val)
    start_segmentation_thread()

def on_method_change(*args):
    """
    Update the segmentation method based on dropdown selection.
    Show/hide relevant controls for the chosen method.
    """
    global segmentation_method
    segmentation_method = method_var.get()
    # Show/hide controls depending on method
    if segmentation_method == "Global Threshold":
        thresh_slider.pack(pady=5)
        kernel_slider.pack_forget()
        adaptive_block_slider.pack_forget()
        adaptive_c_slider.pack_forget()
    elif segmentation_method == "Adaptive Threshold":
        thresh_slider.pack_forget()
        kernel_slider.pack_forget()
        adaptive_block_slider.pack(pady=5)
        adaptive_c_slider.pack(pady=5)
    else:  # Watershed
        thresh_slider.pack(pady=5)
        kernel_slider.pack(pady=5)
        adaptive_block_slider.pack_forget()
        adaptive_c_slider.pack_forget()
    start_segmentation_thread()





# In[14]:


# Threshold factor slider (for Watershed and Global Threshold)
# - from_=0.1 and to=1.0 define the slider range (float values)

thresh_slider = Scale(app, from_=0.1, to=1.0, resolution=0.05, orient=HORIZONTAL,
                      label="Threshold Factor", command=on_threshold_change)
thresh_slider.set(threshold_factor)
thresh_slider.pack(pady=5)

# Kernel size slider (for Watershed)
kernel_slider = Scale(app, from_=1, to=10, orient=HORIZONTAL,
                      label="Kernel Size", command=on_kernel_change)
kernel_slider.set(kernel_size)
kernel_slider.pack(pady=5)

# Adaptive threshold block size slider (for Adaptive Threshold)
# - from_=1 to 10 allows selecting kernel sizes between 1 and 10 pixels

adaptive_block_slider = Scale(app, from_=3, to=51, resolution=2, orient=HORIZONTAL,
                              label="Adaptive Block Size (odd)", command=on_adaptive_block_change)

# Adaptive threshold C slider (for Adaptive Threshold)
adaptive_c_slider = Scale(app, from_=-10, to=10, orient=HORIZONTAL,
                         label="Adaptive C", command=on_adaptive_c_change)


# In[15]:


# Initially hide the sliders for adaptive threshold parameters
# These sliders are only relevant when "Adaptive Threshold" method is selected,
# so we keep them hidden until that method is chosen by the user.

adaptive_block_slider.pack_forget()
adaptive_c_slider.pack_forget()

# Create a button widget labeled "Save Segmented Image"
# When clicked, it will call the save_image function to save the currently segmented image to disk.
save_button = Button(app, text="Save Segmented Image", command=save_image)

# Add the save button to the GUI layout with vertical padding of 10 pixels
save_button.pack(pady=10)

# Set the size of the main application window to 450 pixels wide by 700 pixels tall
app.geometry("450x700")

# Start the Tkinter event loop to run the GUI application
# This call blocks and waits for user interaction until the window is closed.
app.mainloop()

