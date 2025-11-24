import os
import subprocess
import torch
import sys

# --- HEADER / DOCUMENTATION ---

# It is designed to perform setup, object detection, model validation, and training.
#
# IMPORTANT: This script uses 'os.system' to run shell commands. Ensure you have 'git' and 'pip'
# available in your system's PATH.

# The original notebook's descriptive headers and images are preserved as comments below:
# -------------------------------------------------------------------------------------------------------------------
# <div align="center">
#   <a href="https://ultralytics.com/yolov5" target="_blank">
#     <img width="1024", src="https://raw.githubusercontent.com/ultralytics/assets/main/yolov5/v70/splash.png"></a>
# [中文](https://docs.ultralytics.com/zh/) | [한국어](https://docs.ultralytics.com/ko/) | [日本語](https://docs.ultralytics.com/ja/) | [Русский](https://docs.ultralytics.com/ru/) | [Deutsch](https://docs.ultralytics.com/de/) | [Français](https://docs.ultralytics.com/fr/) | [Español](https://docs.ultralytics.com/es/) | [Português](https://docs.ultralytics.com/pt/) | [العربية](https://docs.ultralytics.com/ar/)
#   <a href="https://bit.ly/yolov5-paperspace-notebook"><img src="https://assets.paperspace.io/img/gradient-badge.svg" alt="Run on Gradient"></a>
#   <a href="https://colab.research.google.com/github/ultralytics/yolov5/blob/master/tutorial.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
#   <a href="https://www.kaggle.com/models/ultralytics/yolov5"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open In Kaggle"></a>
# This YOLOv5 🚀 notebook by Ultralytics presents simple train, validate and predict examples to help start your AI adventure.
# We hope that the resources in this notebook will help you get the most out of YOLOv5. Please browse the YOLOv5 Docs for details, raise an issue on GitHub for support, and join our Discord community for questions and discussions!
# </div>
# -------------------------------------------------------------------------------------------------------------------

# --- Setup ---
print("--- Starting Setup ---")

# Clone the YOLOv5 GitHub repository.
# This is equivalent to the notebook command: !git clone https://github.com/ultralytics/yolov5
print("1. Cloning YOLOv5 repository...")
os.system('git clone https://github.com/ultralytics/yolov5')

# Change the current working directory to the cloned 'yolov5' folder.
# This is equivalent to the notebook command: %cd yolov5
print("2. Changing directory to yolov5...")
try:
    os.chdir('yolov5')
except FileNotFoundError:
    print("Error: 'yolov5' directory not found. Cloning may have failed.")
    sys.exit(1)

# Install required Python dependencies from requirements.txt, including 'comet_ml'.
# This is equivalent to the notebook command: %pip install -qr requirements.txt comet_ml
print("3. Installing dependencies...")
# Using os.system for simplicity, matching the notebook's shell command style.
os.system(f'{sys.executable} -m pip install -qr requirements.txt comet_ml')

# Import necessary libraries and run notebook initialization checks.
# This checks for PyTorch, CUDA, and other system configurations.
print("4. Running setup checks...")
import utils
display = utils.notebook_init() # checks

print("--- Setup Complete ---")

# -------------------------------------------------------------------------------------------------------------------
# 1. Detect (Inference)
# Run YOLOv5 inference using detect.py on sample data. Results are saved to 'runs/detect'.

print("\n--- 1. Running Detection (Inference) ---")

# The original notebook detailed various sources for detection:
# python detect.py --source 0 # webcam
# img.jpg # image
# vid.mp4 # video
# screen # screenshot
# path/ # directory
# 'path/*.jpg' # glob
# 'https://youtu.be/LNwODJXcvt4' # YouTube
# 'rtsp://example.com/media.mp4' # RTSP, RTMP, HTTP stream

# Run detection using the small model ('yolov5s.pt') on default images in 'data/images'.
# Image size is set to 640 and confidence threshold to 0.25.
# This is equivalent to: !python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images
os.system('python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images')

# The following lines were for image display in the notebook and are commented out:
# display.Image(filename='runs/detect/exp/zidane.jpg', width=600)
# <img align="left" src="https://user-images.githubusercontent.com/26833433/127574988-6a558aa1-d268-44b9-bf6b-62d4c605cc72.jpg" width="600">

# -------------------------------------------------------------------------------------------------------------------
# 2. Validate (Evaluation)
# Validate the 'yolov5s' model's accuracy on the COCO validation dataset.

print("\n--- 2. Running Validation (Evaluation) ---")

# Download the COCO 2017 validation dataset (780MB, 5000 images).
# The path is set relative to the YOLOv5 root directory (the current working directory).
print("Downloading COCO val dataset...")
torch.hub.download_url_to_file('https://github.com/ultralytics/assets/releases/download/v0.0.0/coco2017val.zip', 'tmp.zip')

# Unzip the dataset to the parent directory ('../datasets') and remove the temporary zip file.
print("Unzipping dataset...")
os.system('unzip -q tmp.zip -d ../datasets && rm tmp.zip')

# Run validation. '--half' uses half-precision (FP16) for potentially faster evaluation.
# This is equivalent to: !python val.py --weights yolov5s.pt --data coco.yaml --img 640 --half
os.system('python val.py --weights yolov5s.pt --data coco.yaml --img 640 --half')

# -------------------------------------------------------------------------------------------------------------------
# 3. Train
# Train a YOLOv5s model on the small COCO128 dataset for a short period.

print("\n--- 3. Training the Model ---")

# Original documentation for training/datasets/loggers is preserved as comments.
# ... (Visual and link documentation for Ultralytics HUB and Roboflow) ...

# Train a YOLOv5s model on COCO128 for 3 epochs.
# --img 640: input image size.
# --batch 16: batch size.
# --epochs 3: number of training epochs.
# --data coco128.yaml: dataset configuration file.
# --weights yolov5s.pt: initial weights from a pre-trained model.
# --cache: enable data caching to speed up training.
# Training results are saved to 'runs/train/'.

# The original notebook used a cell for logger selection: #@title Select YOLOv5 🚀 logger {run: 'auto'}
logger = 'Comet' # Configuration: change to 'ClearML' or 'TensorBoard' as needed

if logger == 'Comet':
    # Setup for Comet logging: installs the library and initializes it.
    print("--- Setting up Comet logging ---")
    os.system('pip install -q comet_ml')
    import comet_ml; comet_ml.init()
elif logger == 'ClearML':
    # Setup for ClearML logging: installs the library and prompts for browser login.
    print("--- Setting up ClearML logging ---")
    os.system('pip install -q clearml')
    import clearml; clearml.browser_login()
elif logger == 'TensorBoard':
    # TensorBoard logs are generated automatically. Instructions are provided on how to launch it manually.
    print("--- Note: TensorBoard logs will be generated. To view, run the command below in your terminal AFTER training: ---")
    print("tensorboard --logdir runs/train")
    # Original notebook magic commands (commented out):
    # %load_ext tensorboard
    # %tensorboard --logdir runs/train
    pass

# Execute the training command.
os.system('python train.py --img 640 --batch 16 --epochs 3 --data coco128.yaml --weights yolov5s.pt --cache')

# -------------------------------------------------------------------------------------------------------------------
# 4. Visualize (Local Logging)
# Section documenting the local logging results and alternative platforms.

print("\n--- 4. Visualization & Next Steps ---")
# The image placeholder and extensive logging documentation is kept as comments.
# <img alt="Local logging results" src="https://user-images.githubusercontent.com/26833433/183222430-e1abd1b7-782c-4cde-b04d-ad52926bf818.jpg" width="1280"/>

# -------------------------------------------------------------------------------------------------------------------
# Appendix - YOLOv5 PyTorch HUB Inference
# Example of using YOLOv5 directly via PyTorch Hub without running 'detect.py'.

print("\n--- Appendix: PyTorch HUB Inference ---")

# Load the 'yolov5s' model directly from the Ultralytics repository using torch.hub.
# 'force_reload=True' ensures the latest version is downloaded.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True, trust_repo=True) # or yolov5n - yolov5x6 or custom

# Define the image source (a URL in this case).
im = 'https://ultralytics.com/images/zidane.jpg' # file, Path, PIL.Image, OpenCV, nparray, list

# Perform inference.
results = model(im) # inference

# Print the detection results (bounding boxes, classes, confidence scores).
results.print() # or .show(), .save(), .crop(), .pandas(), etc.

print("\n--- Script Finished ---")