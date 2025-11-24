#!/usr/bin/env python
# coding: utf-8

# ## GrayScale image Converter using OpenCv


import cv2
from tkinter import Tk, Frame, Label, Button, filedialog, messagebox, N, S, E, W
from PIL import Image, ImageTk



import cv2
from tkinter import Tk, Frame, Label, Button, filedialog, messagebox, N, S, E, W
from PIL import Image, ImageTk


class GrayscaleConverterApp:
    """A GUI app to convert images to grayscale and save them."""

    def __init__(self, root):
        self.root = root
        self.root.title("Image Grayscale Converter")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        # Variables to hold the current grayscale image and its Tkinter PhotoImage
        self.current_gray_image = None  # numpy array (grayscale)
        self.photo_image = None         # Tkinter PhotoImage (PIL)

        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI components with a control panel and image display."""
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.grid(sticky=N+S+E+W)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Control panel on the left
        control_frame = Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky=N+S+E+W, padx=(0, 10))
        main_frame.columnconfigure(0, weight=0)
        main_frame.rowconfigure(0, weight=1)

        label = Label(control_frame,
                      text="Select an Image to Convert to Grayscale",
                      wraplength=180, font=("Arial", 12))
        label.grid(row=0, column=0, pady=(0, 15), sticky=N)

        self.open_button = Button(control_frame,
                             text="Open Image",
                             command=self.open_file,
                             width=20)
        self.open_button.grid(row=1, column=0, pady=5)

        self.save_button = Button(control_frame,
                             text="Save Grayscale Image",
                             command=self.save_file,
                             width=20)
        self.save_button.grid(row=2, column=0, pady=5)

        # Image display frame on the right
        image_frame = Frame(main_frame, bd=2, relief="sunken", width=400, height=400)
        image_frame.grid(row=0, column=1, sticky=N+S+E+W)
        main_frame.columnconfigure(1, weight=1)

        self.image_label = Label(image_frame)
        self.image_label.pack(expand=True, fill='both')

    def open_file(self):
        """Open an image file, convert to grayscale, and display it."""
        # Disable open button to prevent multiple dialogs
        self.open_button.config(state='disabled')
        try:
            self.root.attributes('-topmost', True)  # Bring window to front
            file_path = filedialog.askopenfilename(
                parent=self.root,
                title="Select Image File",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
            )
            self.root.attributes('-topmost', False)  # Reset topmost

            if not file_path:
                return

            image = cv2.imread(file_path)
            if image is None:
                messagebox.showerror("Error", f"Failed to load image:\n{file_path}")
                return

            self.current_gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            pil_image = Image.fromarray(self.current_gray_image)
            pil_image = self._resize_image_to_fit(pil_image, max_width=400, max_height=400)
            self.photo_image = ImageTk.PhotoImage(pil_image)

            self.image_label.config(image=self.photo_image)
            self.image_label.image = self.photo_image  # Keep reference

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
        finally:
            self.open_button.config(state='normal')

    def save_file(self):
        """Save the currently displayed grayscale image to disk."""
        if self.current_gray_image is None:
            messagebox.showwarning("No Image",
                                   "No grayscale image to save. Please open an image first.")
            return

        # Disable save button while saving
        self.save_button.config(state='disabled')
        try:
            save_path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Save Grayscale Image As",
                defaultextension=".png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("BMP Image", "*.bmp"),
                    ("TIFF Image", "*.tiff")
                ]
            )
            if save_path:
                success = cv2.imwrite(save_path, self.current_gray_image)
                if success:
                    messagebox.showinfo("Success", f"Image saved successfully:\n{save_path}")
                else:
                    messagebox.showerror("Save Error", "Failed to save the image. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while saving:\n{e}")
        finally:
            self.save_button.config(state='normal')

    def _resize_image_to_fit(self, pil_image, max_width, max_height):
        """Resize PIL image to fit within max dimensions keeping aspect ratio."""
        width, height = pil_image.size
        ratio = min(max_width / width, max_height / height, 1)  # Do not upscale
        new_size = (int(width * ratio), int(height * ratio))
        return pil_image.resize(new_size, Image.Resampling.LANCZOS)


if __name__ == "__main__":
    root = Tk()
    app = GrayscaleConverterApp(root)
    root.mainloop()
