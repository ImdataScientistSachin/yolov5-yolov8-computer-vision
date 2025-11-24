# OpenCV Computer Vision Practical Tutorials

A comprehensive collection of **practical OpenCV implementations** demonstrating essential computer vision techniques. This repository contains interactive Jupyter notebooks with real-world applications, complete with GUI interfaces for easy experimentation and visualization.

---

## 📋 Project Overview

This project provides hands-on learning materials for computer vision enthusiasts and professionals. Each notebook is a **standalone, fully-documented tutorial** with practical implementations, GUI controls, and real-time parameter adjustment capabilities.

### Key Features
✅ **Interactive GUI interfaces** (Tkinter-based)  
✅ **Real-time parameter tuning** for algorithm optimization  
✅ **Sample video files** for testing and demonstration  
✅ **Well-documented code** with detailed explanations  
✅ **Production-ready implementations** with error handling  

---

## 📁 Project Structure

```
Open CV/
├── face_Detection_OpenCV.py                  # Face detection with YuNet model
├── feature_Mapping_OpenCV.py                 # Feature detection and mapping
├── Hough_Transform_for_LineDetection.py      # Line detection using Hough Transform
├── image_grayscale_converter_OpenCV.py       # Grayscale conversion techniques
├── image_Segmentation_OpenCV.py              # Watershed segmentation algorithm
├── image_Stitching_OpenCV.py                 # Image stitching and panorama creation
├── live_GrayScale_Conversion.py              # Real-time grayscale conversion
├── morphological_transformations_OpenCV.py   # Morphological operations
├── Object_trackeng_OpenCV.py                 # Object tracking in videos
├── Pencil_sketch_conversion_OpenCV.py        # Artistic pencil sketch effects
├── face_detection_settings.json              # Configuration for face detection
├── face_detection_yunet_2023mar.onnx         # Pre-trained YuNet face detection model
└── sample_files/
    ├── airport.mp4
    ├── crowd.mp4
    ├── people walking.mp4
    └── tradmil.mp4
```

---

## 🚀 Tutorials Overview

### 1. **Face Detection** (`face_Detection_OpenCV.py`)
Advanced face detection using the YuNet deep learning model with a comprehensive GUI.

**Features:**
- Image and video face detection
- Real-time parameter adjustment (confidence threshold, NMS threshold)
- Persistent settings saved to JSON
- Multi-threaded processing for responsive UI
- Visualization of detection results with bounding boxes

**Model:** YuNet ONNX Model (2023)

---

### 2. **Feature Mapping** (`feature_Mapping_OpenCV.py`)
Detect and map distinctive features across images using various descriptors.

**Features:**
- SIFT, SURF, ORB, AKAZE feature detection
- Feature matching and correspondence visualization
- Homography computation
- Support for color and grayscale images
- Interactive feature comparison tools

**Applications:** Image registration, object matching, panorama creation

---

### 3. **Hough Line Transform** (`Hough_Transform_for_LineDetection.py`)
Detect straight lines in images using the classical Hough Transform algorithm.

**Features:**
- Canny edge detection preprocessing
- HoughLines and HoughLinesP implementation
- Parameter tuning (threshold, min line length, line gap)
- Visual overlay of detected lines
- Real-time threshold adjustment

**Theory:** Line representation in polar coordinates (r, θ)

---

### 4. **Image Grayscale Conversion** (`image_grayscale_converter_OpenCV.py`)
Multiple techniques for converting color images to grayscale.

**Features:**
- OpenCV's cv2.cvtColor() method
- Custom weighted conversion formulas
- Histogram analysis
- Side-by-side comparison of different approaches

**Applications:** Preprocessing for edge detection, OCR, feature extraction

---

### 5. **Live Grayscale Conversion** (`live_GrayScale_Conversion.py`)
Real-time video stream grayscale conversion with interactive GUI.

**Features:**
- Webcam/video stream processing
- Real-time preview
- Frame-by-frame control
- Performance metrics display
- Multi-threading for smooth playback

---

### 6. **Image Segmentation** (`image_Segmentation_OpenCV.py`)
Segment images into distinct regions using watershed algorithm and other techniques.

**Features:**
- Watershed algorithm implementation
- Morphological operations (erosion, dilation)
- Threshold adjustment controls
- Kernel size customization
- Interactive region visualization

**Applications:** Object separation, medical imaging, quality control

---

### 7. **Image Stitching** (`image_Stitching_OpenCV.ipynb`)
Create panoramic images by stitching multiple overlapping images.

**Features:**
- Feature detection and matching (SIFT/SURF)
- Homography estimation
- Image blending and registration
- Batch processing capabilities
- Panorama creation from multiple views

---

### 8. **Morphological Transformations** (`morphological_transformations_OpenCV.py`)
Apply morphological operations to modify image structure and shape.

**Features:**
- Erosion and dilation operations
- Opening and closing transformations
- Morphological gradient computation
- Top-hat and black-hat transforms
- Kernel shape customization (rectangle, ellipse, cross)

**Applications:** Noise reduction, object separation, shape analysis

---

### 9. **Object Tracking** (`Object_trackeng_OpenCV.py`)
Track objects across video frames using various tracking algorithms.

**Features:**
- Multiple tracking algorithms (KCF, BOOSTING, MEDIANFLOW, etc.)
- Real-time tracking visualization
- Bounding box management
- Video playback control
- Performance statistics

**Sample Videos:** Airport, crowd, pedestrian, treadmill

---

### 10. **Pencil Sketch Conversion** (`Pencil_sketch_conversion_OpenCV.py`)
Transform photos into artistic pencil sketch style images.

**Features:**
- Bilateral filtering for detail preservation
- Dodge and burn technique
- Sketch intensity adjustment
- Color preservation option
- Batch processing capability

**Applications:** Artistic effects, sketch-based retrieval, creative processing

---

## 📦 Dependencies

### Core Libraries
```python
opencv-python>=4.8.0
numpy>=1.24.0
scipy>=1.10.0
```

### GUI & Image Processing
```python
tkinter  # Built-in with Python
Pillow>=10.0.0
```

### Optional Enhancements
```python
matplotlib>=3.7.0  # For advanced visualization
scikit-image>=0.21.0  # Additional image processing
```

---

## 🛠️ Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/opencv-computer-vision.git
cd opencv-computer-vision
```

### 2. **Install Dependencies**
```bash
pip install opencv-python numpy Pillow scipy scikit-image
```

### 3. **Jupyter Setup** (if running notebooks)
```bash
pip install jupyter jupyterlab
jupyter notebook
```

### 4. **Verify Installation**
```python
import cv2
print(f"OpenCV Version: {cv2.__version__}")
```

---

## 🎯 Quick Start

### Running as Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook

# Open any .ipynb file and run cells sequentially
```

### Running as Standalone Python Scripts

Extract the code from any notebook and save as a `.py` file:

```python
# Example: Face Detection Script
python face_detection.py
```

### Using the GUI Applications

Most notebooks include interactive Tkinter GUIs:

1. Launch the notebook cell containing the GUI
2. Select an image/video file via the file dialog
3. Adjust parameters using sliders and controls
4. View real-time results in the display window

---

## 📊 Sample Configurations

### Face Detection Settings (`face_detection_settings.json`)
```json
{
    "conf_threshold": 0.7,
    "nms_threshold": 0.3,
    "top_k": 5000
}
```

- **conf_threshold**: Confidence threshold for detections (0.0-1.0)
- **nms_threshold**: Non-Maximum Suppression threshold
- **top_k**: Maximum number of detections to keep

---

## 🎬 Sample Videos

The `sample_files/` directory includes test videos:

| File | Description | Use Case |
|------|-------------|----------|
| `airport.mp4` | Airport surveillance footage | Tracking, crowd analysis |
| `crowd.mp4` | Crowd movement video | Object tracking, segmentation |
| `people walking.mp4` | Pedestrian footage | Person detection, tracking |
| `tradmil.mp4` | Treadmill exercise video | Activity recognition, pose tracking |

---

## 💡 Usage Examples

### Example 1: Face Detection
```python
import cv2

# Load model
face_detector = cv2.FaceDetectorYN.create(
    "face_detection_yunet_2023mar.onnx",
    "",
    (320, 320),
    0.6,
    0.3,
    5000
)

# Detect faces in image
image = cv2.imread("photo.jpg")
results = face_detector.detect(image)
```

### Example 2: Image Segmentation
```python
import cv2
import numpy as np

# Load and preprocess image
image = cv2.imread("image.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply watershed segmentation
# ... (see notebook for complete implementation)
```

### Example 3: Hough Line Detection
```python
import cv2

image = cv2.imread("lines.jpg", 0)
edges = cv2.Canny(image, 50, 150)

# Detect lines
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
```

---

## 🔍 Key Concepts Covered

### Image Processing Fundamentals
- Color space conversions (RGB, BGR, Grayscale, HSV)
- Filtering and blur techniques
- Edge detection (Canny, Sobel, Laplacian)
- Histogram analysis and equalization

### Feature Detection
- SIFT, SURF, ORB descriptors
- Corner detection (Harris, Shi-Tomasi)
- Feature matching and correspondence
- Homography and perspective transforms

### Advanced Techniques
- Deep learning models (YuNet for face detection)
- Watershed segmentation
- Morphological operations
- Hough transforms (lines and circles)
- Image stitching and panorama creation
- Real-time object tracking

### GUI Development
- Tkinter interface design
- Image display and canvas management
- Real-time parameter adjustment
- Threading for responsive UI
- File dialog integration

---

## 📈 Performance Optimization

### Tips for Better Results

1. **Face Detection:**
   - Adjust confidence threshold for sensitivity
   - Increase input image resolution for better accuracy
   - Use GPU acceleration for real-time processing

2. **Feature Matching:**
   - Use SIFT for complex scenes
   - Use ORB for mobile/embedded systems
   - Filter matches using Lowe's ratio test

3. **Segmentation:**
   - Preprocess with morphological operations
   - Adjust kernel size for different object scales
   - Use bilateral filtering to preserve edges

4. **Video Processing:**
   - Reduce frame resolution for speed
   - Skip frames for real-time processing
   - Use multi-threading to prevent UI freezing

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Model file not found | Ensure `face_detection_yunet_2023mar.onnx` is in the project root |
| Tkinter not available | Install `python-tk` package: `apt-get install python3-tk` |
| Out of memory on video | Reduce video resolution or resize frames |
| GUI not responding | Check if processing is running in main thread |

---

## 📚 Learning Resources

### Official Documentation
- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Python API Reference](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### Related Topics
- [Digital Image Processing](https://en.wikipedia.org/wiki/Digital_image_processing)
- [Hough Transform](https://en.wikipedia.org/wiki/Hough_transform)
- [Watershed Algorithm](https://en.wikipedia.org/wiki/Watershed_%28image_processing%29)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Your Name** - Computer Vision & AI Enthusiast

- 📧 Email: your.email@example.com
- 🔗 LinkedIn: [LinkedIn Profile](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)

---

## 🌟 Acknowledgments

- **OpenCV Community** for the amazing computer vision library
- **Deep Learning Models** providers for pre-trained YuNet face detector
- **Sample Videos** and resources for testing
- All contributors and users for feedback and improvements

---

## 📞 Support & Feedback

Have questions or suggestions? Feel free to:
- Open an [Issue](https://github.com/yourusername/opencv-computer-vision/issues)
- Start a [Discussion](https://github.com/yourusername/opencv-computer-vision/discussions)
- Contact via email

---

## 📊 Project Statistics

- **Total Notebooks:** 10
- **Code Lines:** 3000+
- **Documented Functions:** 50+
- **Sample Videos:** 4
- **Key Algorithms:** 20+

---

## 🚀 Future Enhancements

- [ ] Add GPU acceleration support (CUDA)
- [ ] Implement deep learning models (YOLO, Mask R-CNN)
- [ ] Add web interface (Flask/Streamlit)
- [ ] Performance benchmarking suite
- [ ] Extended video codec support
- [ ] Real-time streaming capabilities
- [ ] Advanced 3D reconstruction
- [ ] Machine learning integration

---

**Last Updated:** November 2025  
**OpenCV Version:** 4.8.0+  
**Python Version:** 3.8+

---

## ⭐ Show Your Support

If you find this project helpful, please give it a star! ⭐

```
Your support motivates continued development and improvement of these tutorials.
```

---

