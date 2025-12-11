# 👁️ YOLOv8 & OpenCV Computer Vision Suite

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange?style=for-the-badge&logo=ultralytics&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

## 🚀 Overview

Welcome to the **YOLOv8 & OpenCV Computer Vision Suite**. This repository houses a professional collection of computer vision implementations, bridging the gap between classical image processing techniques and state-of-the-art deep learning detection models.

From **real-time security monitoring systems** capable of detecting loitering in restricted zones, to **interactive facial analysis tools** and comprehensive **object tracking benchmarks**, this suite serves as both a practical toolkit and an advanced educational resource.

---

## 🌟 Key Features

### 1. 🚨 YOLOv8 Night-Time Security Tracker
*Located in: `YOLOv8 and OpenCV built-in tracking/`*

A robust surveillance system designed for low-light environments.
*   **Real-time Person Detection**: Leverages `yolov8n` (Nano) for high-speed tracking on consumer hardware.
*   **Smart Loitering Detection**: Define custom polygon zones (e.g., driveways, porches). The system tracks individuals and triggers alerts if they linger beyond a set threshold (default: 5s).
*   **Persistent Tracking**: Utilizes YOLO's native tracking capabilities to maintain subject identity across frames.
*   **Visual Analytics**: dynamic bounding boxes, alert zone overlays, and on-screen status warnings.

### 2. 👤 YuNet Face Detection & Analytics
*Located in: `Open CV/face_Detection_OpenCV.py`*

A modern, GUI-based application for facial analysis.
*   **Deep Learning Backend**: Powered by OpenCV's `FaceDetectorYN` (YuNet) for superior accuracy over Haar cascades.
*   **Interactive GUI**: Built with standard libraries to allow drag-and-drop image analysis and live webcam switching.
*   **Detailed Landmarks**: Detects and visualizes 5 key facial landmarks (eyes, nose, mouth corners).
*   **Configurable**: Adjust Confidence Threshold, NMS (Non-Maximum Suppression), and Top-K parameters in real-time.

### 3. 👥 AI People Counter & Tracker
*Located in: `yolov5/GetCounting.py`*

A lightweight, custom implementation of object tracking for counting applications.
*   **Centroid Tracking Algorithm**: Implements a custom pure-Python centroid tracker to assign and maintain IDs.
*   **Video Analysis**: Select any video file via system dialog to automatically count unique persons.
*   **Filtered Detection**: Intelligent filtering based on confidence scores and bounding box size to reduce false positives.
*   **Real-time Visualization**: Displays dynamic bounding boxes, unique IDs, and a live total count overlay.

### 4. 🎯 Universal Object Tracking Benchmark
*Located in: `Open CV/Object_trackeng_OpenCV.py`*

A comprehensive suite allowing side-by-side comparison of 7+ tracking algorithms.
*   **Supported Algorithms**: `CSRT` (High Accuracy), `KCF` (Fast), `MOSSE` (Ultra Fast), `MIL`, `TLD`, `MEDIANFLOW`, `BOOSTING`.
*   **ROI Selection**: Interactive Region-of-Interest selection to start tracking any arbitrary object.
*   **Performance Metrics**: Real-time FPS display to evaluate tracker efficiency.

### 5. 🛠️ Classical Computer Vision Utilities
A treasure trove of essential image processing scripts:
*   **Panorama Stitching**: Automatically stitch multiple overlapping photos into a single seamless panorama.
*   **Sketch Artist**: Convert standard video/images into high-quality pencil sketches using bilateral filtering.
*   **Hough Line Detection**: Detect structural lines in architectural or geometric images.
*   **Image Segmentation**: Implement Watershed algorithm for complex object separation.

---

## 📦 Installation

### Prerequisites
*   **Python 3.8+**
*   **NVIDIA GPU** (Recommended for YOLOv8 performance)
*   **Webcam** (For live demos)

### Setup
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/yolov5-yolov8-computer-vision-main.git
    cd yolov5-yolov8-computer-vision-main
    ```

2.  **Install Dependencies**
    ```bash
    pip install numpy opencv-python ultralytics pillow torch torchvision torchaudio ipywidgets
    ```

3.  **Model Setup (For Face Detection)**
    *   Download the [YuNet ONNX model](https://github.com/opencv/opencv_zoo/blob/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx).
    *   Place `face_detection_yunet_2023mar.onnx` in the `Open CV/` directory.

---

## 💻 Usage Guide

### Running the Security Tracker
Monitor your video feeds for suspicious activity.
```bash
cd "YOLOv8 and OpenCV built-in tracking"
# Edit the video path in the script if not using a webcam
python Live_Tracking.py
```

### Launching the Face Detection App
Start the GUI for image and video analysis.
```bash
cd "Open CV"
python face_Detection_OpenCV.py
```

### Running the AI People Counter
Select a video file to count unique individuals.
```bash
cd yolov5
python GetCounting.py
```

### Testing Object Trackers
Compare different tracking algorithms on your own footage.
```bash
cd "Open CV"
python Object_trackeng_OpenCV.py
```

---

## 📂 Project Structure

```text
root/
├── YOLOv8 and OpenCV built-in tracking/   # Modern Deep Learning Tracking
│   ├── Live_Tracking.py                   # Main Security Script
│   └── Live_Tracking.ipynb                # Jupyter Notebook demonstration
│
├── Open CV/                               # Classical & DNN OpenCV Tools
│   ├── face_Detection_OpenCV.py           # YuNet Face Detection GUI
│   ├── Object_trackeng_OpenCV.py          # Multi-algorithm Tracker
│   ├── image_Stitching_OpenCV.py          # Panorama Creator
│   ├── Pencil_sketch_conversion_OpenCV.py # Artistic Filters
│   └── ... (various utility scripts)
│
└── README.md                              # This file
```

---

## 🔮 Future Roadmap

*   [ ] **Web Interface**: Porting the Security Tracker to a Streamlit Dashboard.
*   [ ] **Multi-Camera Support**: Enabling simultaneous streams for larger area coverage.
*   [ ] **Action Recognition**: Integrating Pose Estimation to detect specific behaviors (falling, running).
*   [ ] **Docker Support**: Containerizing the application for easy deployment.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
