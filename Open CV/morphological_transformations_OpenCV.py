#!/usr/bin/env python
# coding: utf-8

# ## morphological transformations to an image using OpenCV and Tkinter



# import Libraries

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, HORIZONTAL, Button, OptionMenu
from PIL import Image, ImageTk



# Initialize main Tkinter window
root = tk.Tk()
root.title("Morphological Transformations")

# Global variables to hold images
img = None          # Original loaded image
img_display = None  # Transformed image to display
img_tk = None       # ImageTk object for Tkinter display


# List of morphological operations supported
OPTIONS = [
    "Erosion",
    "Dilation",
    "Opening",
    "Closing",
    "Gradient",
    "Top Hat",
    "Black Hat"
]

# List of image modes for processing
MODES = [
    "Color",      # Original color image
    "Grayscale",  # Convert to grayscale
    "Binary"      # Convert to binary image via thresholding
]

# List of kernel shapes for structuring element
KERNEL_SHAPES = [
    "Rectangle",  # Square/rectangular kernel
    "Ellipse",    # Elliptical kernel
    "Cross"       # Cross-shaped kernel
]

# Tkinter variables for dropdown selections
var_operation = tk.StringVar(root)
var_operation.set(OPTIONS[0])  # Default morphological operation

var_mode = tk.StringVar(root)
var_mode.set(MODES[0])          # Default image mode: Color

var_kernel_shape = tk.StringVar(root)
var_kernel_shape.set(KERNEL_SHAPES[0])  # Default kernel shape: Rectangle

# Label widget to display images inside the Tkinter window
img_label = tk.Label(root)
img_label.pack()



def load_image():
    global img
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    loaded_img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if loaded_img is None:
        print("Failed to load image.")
        return

    mode = var_mode.get()
    if mode == "Grayscale":
        img = cv2.cvtColor(loaded_img, cv2.COLOR_BGR2GRAY)
    elif mode == "Binary":
        gray = cv2.cvtColor(loaded_img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    else:
        img = loaded_img

    apply_transformations()

def apply_transformations(*args):
    global img, img_display, img_tk

    if img is None:
        return

    kernel_size = kernel_scale.get()
    operation = var_operation.get()
    kernel_shape_name = var_kernel_shape.get()

    shape_dict = {
        "Rectangle": cv2.MORPH_RECT,
        "Ellipse": cv2.MORPH_ELLIPSE,
        "Cross": cv2.MORPH_CROSS
    }
    kernel_shape = shape_dict.get(kernel_shape_name, cv2.MORPH_RECT)
    # MORPH_RECT — Rectangular kernel (square or rectangle),
    # MORPH_ELLIPSE — Elliptical kernel,
    # cv2.MORPH_CROSS — Cross-shaped kernel

    kernel = cv2.getStructuringElement(kernel_shape, (kernel_size, kernel_size))

    # Apply the selected morphological operation based on the user's choice
    # Erosion shrinks bright regions by eroding boundaries of foreground objects.
    if operation == "Erosion":
        transformed_img = cv2.erode(img, kernel, iterations=1)

    # Dilation expands bright regions by adding pixels to the boundaries of objects.
    elif operation == "Dilation":
        transformed_img = cv2.dilate(img, kernel, iterations=1)
        
    # It removes small objects or noise from the foreground while preserving the shape and size of larger objects.
    elif operation == "Opening":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # It fills small holes or gaps in the foreground objects, useful for closing small black spots inside white regions.
    elif operation == "Closing":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # Morphological gradient is the difference between dilation and erosion of an image.
    elif operation == "Gradient":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    # It extracts small bright elements or details smaller than the structuring element.
    elif operation == "Top Hat":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    
    # It extracts small dark elements or details on a bright background.   
    elif operation == "Black Hat":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    else:
        transformed_img = img.copy()  # No operation fallback

    img_display = transformed_img

    # Prepare image for Tkinter display
    mode = var_mode.get()
    if mode == "Color":
        # Convert BGR (OpenCV) to RGB (PIL)
        img_rgb = cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
    else:
        # Grayscale or binary images can be directly converted
        img_pil = Image.fromarray(img_display)

    # Convert PIL image to ImageTk format
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Update label with new image
    img_label.config(image=img_tk)
    img_label.image = img_tk  # Keep reference to avoid garbage collection




# --- GUI Widgets ---

# Dropdown menu for morphological operations
operation_menu = OptionMenu(root, var_operation, *OPTIONS)
operation_menu.pack(pady=5)

# Dropdown menu for image mode selection (Color, Grayscale, Binary)
mode_menu = OptionMenu(root, var_mode, *MODES)
mode_menu.pack(pady=5)

# Dropdown menu for kernel shape selection (Rectangle, Ellipse, Cross)
kernel_shape_menu = OptionMenu(root, var_kernel_shape, *KERNEL_SHAPES)
kernel_shape_menu.pack(pady=5)

# Slider to select kernel size (1 to 20)
kernel_scale = Scale(root, from_=1, to=20, orient=HORIZONTAL, label="Kernel Size")
kernel_scale.set(5)  # Default kernel size
kernel_scale.pack(pady=5)

# Button to load image from file
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)

# Bind events to update image

kernel_scale.bind("<ButtonRelease-1>", lambda event: apply_transformations())
var_operation.trace("w", lambda *args: apply_transformations())
var_kernel_shape.trace("w", lambda *args: apply_transformations())

# IMPORTANT: Do NOT call load_image on var_mode change directly,
# instead bind mode change to a function that reloads the image only if one is loaded
def on_mode_change(*args):
    global img
    if img is not None:
        load_image()

var_mode.trace("w", on_mode_change)

root.mainloop()

