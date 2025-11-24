#!/usr/bin/env python
# coding: utf-8

# ## Pencil sketch Conversion using openCV


# import Libraries

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox



# Dictionary to store PIL images for display and saving

images = {"original": None, "sketch": None}


# ## CPU based processing
# 
# #### (It takes more time for processing high resolution Images)



def open_file():
    """Open an image file and process it."""
    filepath = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
    )
    if not filepath:
        return
    img = cv2.imread(filepath)
    if img is None:
        messagebox.showerror("Error", "Selected file is not a valid image.")
        return
    display_image(img, original=True)  # Show original image
    sketch_img = convert_to_sketch(img)  # Convert to sketch
    display_image(sketch_img, original=False)  # Show sketch

def color_dodge(front, back):
    """
    Perform color dodge blending between two images.
    front: grayscale image
    back: blurred inverted image
    Formula: output = min(255, (front * 255) / (255 - back + 1))
    """
    # Use cv2.divide for efficient division and scaling
    result = cv2.divide(front, 255 - back, scale=256)
    result[result > 255] = 255  # Clip values to max 255
    return result

def convert_to_sketch(img):
    """
    Convert input BGR image to a pencil sketch with enhanced details.
    Steps:
    1. Convert to grayscale.
    2. Invert grayscale image.
    3. Apply bilateral filter to smooth while preserving edges.
    4. Use color dodge blending between grayscale and blurred inverted image.
    5. Detect edges with Laplacian filter.
    6. Invert edges and blend with sketch to enhance details.
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale
    inverted_img = cv2.bitwise_not(gray_img)  # Invert grayscale

    # Bilateral filter smooths while preserving edges better than Gaussian blur
    blurred_img = cv2.bilateralFilter(inverted_img, d=9, sigmaColor=75, sigmaSpace=75)

    # Color dodge blend to create sketch effect
    sketch_img = color_dodge(gray_img, blurred_img)

    # Edge detection to enhance fine details
    edges = cv2.Laplacian(gray_img, cv2.CV_8U, ksize=5)
    edges_inv = cv2.bitwise_not(edges)  # Invert edges for white lines on black

    # Combine edges with sketch to enhance line details
    enhanced_sketch = cv2.bitwise_and(sketch_img, edges_inv)

    return enhanced_sketch

def display_image(img, original):
    """
    Display image in the Tkinter GUI label.
    If original is True, convert BGR to RGB for display.
    Resize image to fit GUI window.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)

    # Resize image to max 400x400 for GUI display
    img_pil.thumbnail((400, 400), Image.Resampling.LANCZOS)


    img_tk = ImageTk.PhotoImage(image=img_pil)

    if original:
        images["original"] = img_pil
        label = original_image_label
    else:
        images["sketch"] = img_pil
        label = sketch_image_label

    label.config(image=img_tk)
    label.image = img_tk  # Keep reference to avoid garbage collection

def save_sketch():
    """Save the currently displayed sketch image to a PNG file."""
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save.")
        return

    # Get selected format from dropdown
    file_format = selected_format.get()
    ext = file_format.lower()

    # Ask user for save location with appropriate extension and file types
    sketch_filepath = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(f"{file_format} files", f"*.{ext}"), ("All files", "*.*")]
    )
    if not sketch_filepath:
        return

    # Save the PIL image in the chosen format
    try:
        images["sketch"].save(sketch_filepath, file_format)
        messagebox.showinfo("Saved", f"Sketch saved to {sketch_filepath}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save sketch:\n{e}")




# ## Gpu based processing 
# 
# #### (It takes less time for processing high resolution Images as compared to CPU)
# 




def open_file():
    """Open an image file and process it."""
    filepath = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
    )
    if not filepath:
        return
    img = cv2.imread(filepath)
    if img is None:
        messagebox.showerror("Error", "Selected file is not a valid image.")
        return
    display_image(img, original=True)  # Show original image
    sketch_img = convert_to_sketch(img)  # Convert to sketch
    display_image(sketch_img, original=False)  # Show sketch

def color_dodge(front, back):
    """
    Perform color dodge blending between two images.
    front: grayscale image
    back: blurred inverted image
    Formula: output = min(255, (front * 255) / (255 - back + 1))
    """
    # Use cv2.divide for efficient division and scaling
    result = cv2.divide(front, 255 - back, scale=256)
    result[result > 255] = 255  # Clip values to max 255
    return result


def convert_to_sketch_gpu(img):
    """
    Convert BGR image to pencil sketch using OpenCV CUDA functions.
    Assumes OpenCV is built with CUDA support.
    """
    # Upload image to GPU
    gpu_img = cv2.cuda_GpuMat()
    gpu_img.upload(img)

    # Convert to grayscale on GPU
    gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)

    # Invert grayscale image on GPU
    gpu_inverted = cv2.cuda.bitwise_not(gpu_gray)

    # Bilateral filter on GPU (preserves edges)
    bilateral_filter = cv2.cuda.createBilateralFilter(cv2.CV_8UC1, d=9, sigmaColor=75, sigmaSpace=75)
    gpu_blurred = bilateral_filter.apply(gpu_inverted)

    # Download images to CPU for color dodge blending (no direct CUDA color dodge)
    gray = gpu_gray.download()
    blurred = gpu_blurred.download()

    # Color dodge blend on CPU
    sketch = cv2.divide(gray, 255 - blurred, scale=256)

    # Edge detection on CPU (Laplacian not available on CUDA module)
    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
    edges_inv = cv2.bitwise_not(edges)

    # Combine edges with sketch on CPU
    enhanced_sketch = cv2.bitwise_and(sketch, edges_inv)

    return enhanced_sketch


def display_image(img, original):
    """
    Display image in the Tkinter GUI label.
    If original is True, convert BGR to RGB for display.
    Resize image to fit GUI window.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)

    # Resize image to max 400x400 for GUI display
    img_pil.thumbnail((400, 400), Image.Resampling.LANCZOS)


    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Store PIL image for saving later
    if original:
        images["original"] = img_pil
        label = original_image_label
    else:
        images["sketch"] = img_pil
        label = sketch_image_label

    label.config(image=img_tk)
    label.image = img_tk  # Keep reference to avoid garbage collection

def save_sketch():
    """Save the currently displayed sketch image to selected format from dropdown."""
    file_format = selected_format.get()
    ext = file_format.lower()

    # Ask user for save location with appropriate extension and file types
    sketch_filepath = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(f"{file_format} files", f"*.{ext}"), ("All files", "*.*")]
    )
    if not sketch_filepath:
        return

    # Save the PIL image in the chosen format
    try:
        images["sketch"].save(sketch_filepath, file_format)
        messagebox.showinfo("Saved", f"Sketch saved to {sketch_filepath}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save sketch:\n{e}")





# Tkinter GUI setup
app = tk.Tk()
app.title('Enhanced Pencil Sketch Converter')

frame = tk.Frame(app)
frame.pack(pady=10, padx=10)

# Labels to display original and sketch images
original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

# Text labels under images
label_original = tk.Label(frame, text="Original Image")
label_original.grid(row=1, column=0)
label_sketch = tk.Label(frame, text="Enhanced Sketch")
label_sketch.grid(row=1, column=1)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

# Buttons to open image and save sketch
open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

# Label for the format selection dropdown
format_label = tk.Label(btn_frame, text="Select your desired Format:")
format_label.grid(row=0, column=2, padx=(10, 2), pady=5, sticky="e")

# Dropdown menu for selecting save format
selected_format = tk.StringVar(value="PNG")  # Default format
format_options = ["PNG", "JPEG", "BMP", "TIFF"]
format_menu = tk.OptionMenu(btn_frame, selected_format, *format_options)
format_menu.grid(row=0, column=3, padx=5, pady=5, sticky="w")


app.mainloop()