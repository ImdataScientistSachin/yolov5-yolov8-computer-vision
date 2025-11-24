#!/usr/bin/env python
# coding: utf-8

# ## Image Stitching using Open CV


# import the libraries

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os



def is_image_suitable(img):
    """
    Check if the image has enough features for stitching.
    Returns True if sufficient keypoints are detected.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray, None)
    return len(keypoints) > 200  # Empirical threshold

def downscale_image(img, max_dim=1200):
    """
    Downscale large images for performance.
    """
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return img

def resize_images_to_minimum(images):
    """
    Resize all images to the smallest width and height among them.
    This keeps them consistent for stitching or concatenation.
    """
    min_height = min(img.shape[0] for img in images)
    min_width = min(img.shape[1] for img in images)
    resized_images = []
    for img in images:
        resized = cv2.resize(img, (min_width, min_height), interpolation=cv2.INTER_AREA)
        resized_images.append(resized)
    return resized_images

def concat_images(img1, img2, direction='horizontal'):
    """
    Concatenate two images in the specified direction.
    """
    if direction == 'horizontal':
        return cv2.hconcat([img1, img2])
    else:
        return cv2.vconcat([img1, img2])

def estimate_and_align(img1, img2, search_width=200):
    """
    Attempts to find the best horizontal overlap between img1 and img2 using template matching.
    Returns a stitched image with estimated overlap.
    """
    # Use the right edge of img1 as template
    template = img1[:, -search_width:]
    res = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    x_offset = max_loc[0]
    # Align images based on estimated offset
    img2_aligned = img2[:, x_offset:]
    result = np.hstack([img1, img2_aligned])
    return result

class StitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Stitching with OpenCV")
        self.image_paths = []
        self.panel = tk.Label(root)
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Open 2 Images", command=self.open_files).pack(pady=10)
        tk.Button(self.root, text="Stitch Images", command=self.stitch_images).pack(pady=10)
        self.panel.pack(padx=10, pady=10)

    def open_files(self):
        """
        Open a file dialog to select exactly 2 different images.
        Ensures the files are not the same and handles path normalization robustly.
        """
        files = filedialog.askopenfilenames(
            title='Select 2 Different Images',
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif")]
        )
        if len(files) != 2:
            messagebox.showerror("Error", "Please select exactly two different images.")
            return

        # Normalize and compare absolute paths (case-insensitive for Windows)
        file1 = os.path.normcase(os.path.abspath(files[0]))
        file2 = os.path.normcase(os.path.abspath(files[1]))

        if file1 == file2:
            messagebox.showerror("Error", "You have selected the same image twice. Please select two different images.")
            return

        self.image_paths = [file1, file2]
        messagebox.showinfo("Success", "Selected 2 different images.")

    def stitch_images(self):
        """
        Load, validate, resize, and stitch the selected images.
        If stitching fails due to insufficient overlap, try template matching alignment, else concatenate.
        """
        if len(self.image_paths) != 2:
            messagebox.showerror("Error", "Please select exactly two images before stitching.")
            return

        images = []
        for path in self.image_paths:
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Error", f"Could not read image {path}")
                return
            img = downscale_image(img)
            if not is_image_suitable(img):
                messagebox.showerror(
                    "Error",
                    f"Image '{os.path.basename(path)}' lacks sufficient features for stitching.\n"
                    "Try using images with more texture or detail."
                )
                return
            images.append(img)

        # Resize both images to the smallest dimensions
        images = resize_images_to_minimum(images)
        self.handle_overlap_and_stitch(images)

    def handle_overlap_and_stitch(self, images, overlap_px=100):
        """
        Try OpenCV's stitcher. If it fails, try template matching alignment. If that fails, concatenate.
        """
        try:
            stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        except AttributeError:
            stitcher = cv2.createStitcher(False)
        status, pano = stitcher.stitch(images)
        if status == cv2.Stitcher_OK:
            self.display_image(pano)
            messagebox.showinfo("Success", "Images stitched successfully.")
            return

        # If stitching fails, try estimated alignment (template matching)
        try:
            aligned = estimate_and_align(images[0], images[1], search_width=overlap_px)
            self.display_image(aligned)
            messagebox.showwarning(
                "Estimated Alignment",
                "Stitching failed (insufficient overlap/features), so images were aligned using template matching.\n"
                "For best results, use images with 30–50% overlap and rich, unique textures."
            )
            return
        except Exception as e:
            print("Estimated alignment failed:", e)

        # Fallback: Concatenation
        concat = concat_images(images[0], images[1], direction='horizontal')
        self.display_image(concat)
        messagebox.showwarning(
            "Concatenation",
            "Stitching and alignment failed. Images were concatenated as a fallback."
        )

    def display_image(self, cv_image):
        """Display the stitched or concatenated image in the Tkinter panel."""
        cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image_rgb)
        imgtk = ImageTk.PhotoImage(image=pil_image)
        self.panel.config(image=imgtk)
        self.panel.image = imgtk  # Prevent garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = StitcherApp(root)
    root.mainloop()

