#!/usr/bin/env python
# coding: utf-8



# ## Feature mapping on Image using OpenCV

import cv2
import numpy as np
from tkinter import Tk, filedialog, StringVar, Button, Label, messagebox, IntVar, OptionMenu, Scale, HORIZONTAL
from PIL import Image, ImageTk  # We need Pillow because Tkinter doesn't understand OpenCV images natively

def show_image_on_label(img_cv, label_widget, maxsize=(250, 250)):
    """
    Helper to get an OpenCV image onto a Tkinter Label.
    It handles the color conversion and resizing so the GUI doesn't look messy.
    """
    if img_cv is None:
        label_widget.config(image='', text='No Image')
        return

    # OpenCV uses BGR by default, but the rest of the world (and Tkinter) likes RGB.
    # If we don't convert this, blue things will look red and vice versa.
    if len(img_cv.shape) == 2:  # It's grayscale
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
    else:  # It's color
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # Convert to a PIL image first, then to a Tkinter-compatible photo
    img_pil = Image.fromarray(img_cv)
    img_pil.thumbnail(maxsize)  # Keep thumbnails small for the UI
    img_tk = ImageTk.PhotoImage(img_pil)

    # !!! CRITICAL !!! 
    # We have to attach the image object to the widget (label_widget.img_tk = img_tk).
    # If we don't do this, Python's garbage collector will delete the image from memory
    # immediately, and you'll just see a blank grey box.
    label_widget.img_tk = img_tk  
    label_widget.config(image=img_tk, text='')

def select_image(label, is_first=True):
    # Using globals isn't usually "best practice," but for a simple script like this,
    # it saves us from passing a state object around everywhere.
    global img1, img2, file_path1, file_path2
    
    file_path = filedialog.askopenfilename()
    if not file_path:
        # User hit cancel, so let's just do nothing.
        return
    try:
        # Load based on the user's dropdown choice (Color or Grayscale)
        mode = cv2.IMREAD_COLOR if color_var.get() == "Color" else cv2.IMREAD_GRAYSCALE
        img = cv2.imread(file_path, mode)
        
        if img is None:
            raise ValueError("File is not a valid image.")
            
        # Figure out if we are setting the left image or the right image
        if is_first:
            img1 = img
            file_path1 = file_path
        else:
            img2 = img
            file_path2 = file_path
            
        # Update the GUI to show the user what they picked
        label.config(text=f"Image: {file_path.split('/')[-1]}")
        show_image_on_label(img, label)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

def resize_cv_image(img, max_width=900, max_height=700):
    """
    Prevents the final result window from being larger than your monitor 
    if you use high-res photos.
    """
    h, w = img.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def feature_matching():
    # Can't match if we don't have two images!
    if img1 is None or img2 is None:
        messagebox.showwarning("Input Error", "Please select both images first.")
        return

    detector_type = detector_var.get()
    nfeatures = orb_features_var.get()
    
    try:
        # Initialize the detector based on user choice.
        if detector_type == 'ORB':
            # ORB is free to use and fast.
            detector = cv2.ORB_create(nfeatures=nfeatures)
            norm_type = cv2.NORM_HAMMING # ORB uses binary descriptors, so we need Hamming distance
        elif detector_type == 'SIFT':
            # SIFT is more accurate but mathematically heavier.
            detector = cv2.SIFT_create(nfeatures=nfeatures)
            norm_type = cv2.NORM_L2 # SIFT uses floating point descriptors, so we need Euclidean (L2) distance
        else:
            raise ValueError("Unknown detector selected.")

        # The heavy lifting: Find the keypoints and compute descriptors
        keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
        keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
        
        if descriptors1 is None or descriptors2 is None:
            raise ValueError("No features found in one or both images.")

        # Create the Matcher. 
        # crossCheck=True means: match A->B and B->A, and only keep it if they agree. 
        # This filters out a lot of garbage matches.
        bf = cv2.BFMatcher(norm_type, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        
        if not matches:
            raise ValueError("No matches found between images.")

        # Sort matches by distance (smaller distance = better match)
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Draw the top 50 matches. 
        # We don't draw all of them because if there are 2000 matches, the image just looks like a mess of green lines.
        img_matches = cv2.drawMatches(
            img1, keypoints1, img2, keypoints2, matches[:50], None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        # Resize the result so it fits on the screen
        img_matches = resize_cv_image(img_matches)
        
        # Pop up the result in a standard OpenCV window
        cv2.imshow('Feature Matching', img_matches)
        cv2.waitKey(0) # Wait until the user presses a key to close the window
        cv2.destroyAllWindows()
        
    except Exception as e:
        messagebox.showerror("Feature Matching Error", f"Failed to match features: {e}")

# --- GUI SETUP ---
root = Tk()
root.title('Feature Matching')

# Initialize global placeholders
img1 = img2 = None
file_path1 = file_path2 = None

# Dropdown to choose between ORB (Fast) and SIFT (Accurate)
detector_options = ['ORB', 'SIFT']
detector_var = StringVar(root)
detector_var.set('ORB')
Label(root, text="Feature Detector:").pack()
OptionMenu(root, detector_var, *detector_options).pack()

# Slider to control how many features to look for. 
# More features = more matches, but slower.
Label(root, text="Number of Features:").pack()
orb_features_var = IntVar(value=500)
Scale(root, from_=100, to=2000, orient=HORIZONTAL, variable=orb_features_var).pack()

# Option to switch between processing in Color or Grayscale
color_var = StringVar(root)
color_var.set("Grayscale")
Label(root, text="Image Mode:").pack()
OptionMenu(root, color_var, "Grayscale", "Color").pack()

# UI elements for Image 1
label_img1 = Label(root, text="Image 1: Not selected")
label_img1.pack()
btn_select_image1 = Button(root, text="Select Image 1", command=lambda: select_image(label_img1, is_first=True))
btn_select_image1.pack()

# UI elements for Image 2
label_img2 = Label(root, text="Image 2: Not selected")
label_img2.pack()
btn_select_image2 = Button(root, text="Select Image 2", command=lambda: select_image(label_img2, is_first=False))
btn_select_image2.pack()

# The "Go" button
btn_match_features = Button(root, text="Match Features", command=feature_matching)
btn_match_features.pack()

root.mainloop()