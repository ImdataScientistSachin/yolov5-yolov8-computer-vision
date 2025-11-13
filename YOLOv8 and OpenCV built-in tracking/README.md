# YOLOv8 and OpenCV Built-in Tracking

**Author:** Sachin Paunikar

## Overview

This project demonstrates advanced **real-time object tracking and security monitoring** using YOLOv8 and OpenCV. It showcases how to build intelligent surveillance systems capable of detecting, tracking, and monitoring suspicious activities in video feeds. The system is designed for practical security applications including home surveillance, perimeter monitoring, and loitering detection.

## 🎯 Project Objectives

- **Real-time Object Detection**: Leverage YOLOv8's state-of-the-art neural network for accurate person detection
- **Continuous Tracking**: Track detected individuals across video frames with unique IDs
- **Behavioral Analysis**: Monitor for suspicious behavior patterns such as loitering
- **Night Vision Support**: Optimized for low-light surveillance scenarios
- **Alert Generation**: Trigger notifications when threats are detected in predefined zones
- **GPU Acceleration**: Utilize CUDA for fast processing on NVIDIA GPUs

## 📋 Key Features

### 1. **YOLOv8 Integration**
   - Fast and accurate person detection using YOLOv8 nano model (`yolov8n.pt`)
   - Automatic GPU/CPU detection and utilization
   - Support for multiple model sizes (nano, small, medium, large, extra-large)

### 2. **OpenCV-based Tracking**
   - Real-time multi-object tracking with persistent ID assignment
   - Tracking multiple individuals simultaneously
   - Trajectory history visualization for movement analysis

### 3. **Security Features**
   - **Zone-based Alerts**: Define alert zones (driveway, porch, etc.) for restricted areas
   - **Loitering Detection**: Identify when persons remain in alert zones for extended periods
   - **Night Mode Optimization**: Enhanced performance for dark/low-light conditions
   - **Event Logging**: Record detected events with timestamps and locations

### 4. **Visualization & Monitoring**
   - Real-time bounding box annotations
   - Trajectory trails for visual tracking confirmation
   - Zone highlighting with color-coded alerts
   - Frame-by-frame debugging capabilities

## 📁 Project Structure

```
YOLOv8 and OpenCV built-in tracking/
├── Live_Tracking.ipynb              # Main interactive notebook for security tracking
├── yolov8n.pt                       # Pre-trained YOLOv8 nano model weights
├── README.md                        # Project documentation
└── .ipynb_checkpoints/              # Jupyter notebook backup files
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **CUDA 11.8+** (for GPU acceleration, optional but recommended)
- **cuDNN** (for GPU support)

### Installation

1. **Clone or Navigate to Project Directory**
   ```bash
   cd "YOLOv8 and OpenCV built-in tracking"
   ```

2. **Install Required Dependencies**
   ```bash
   pip install ultralytics opencv-python numpy ipywidgets torch torchvision
   ```

   For optimal performance with GPU support:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Verify GPU Availability** (Optional)
   ```python
   import torch
   print(f"GPU Available: {torch.cuda.is_available()}")
   print(f"Device Count: {torch.cuda.device_count()}")
   ```

## 🎬 Usage Guide

### Basic Live Tracking

```python
import cv2
from ultralytics import YOLO
import torch

# Configuration
DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'
model = YOLO('yolov8n.pt')

# Load video or webcam
cap = cv2.VideoCapture(0)  # 0 for webcam, or path to video file

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run YOLOv8 detection
    results = model(frame, device=DEVICE)
    
    # Visualize results
    annotated_frame = results[0].plot()
    cv2.imshow('YOLOv8 Tracking', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Security Zone Setup

```python
# Define alert zone as polygon coordinates (x, y)
ALERT_ZONE = [(100, 100), (400, 100), (400, 300), (100, 300)]

# Function to check if point is in zone
def point_in_zone(point, zone):
    from shapely.geometry import Point, Polygon
    return Point(point).within(Polygon(zone))

# Check if tracked person enters alert zone
if point_in_zone(person_location, ALERT_ZONE):
    print("ALERT: Person detected in restricted zone!")
```

### Loitering Detection

```python
from collections import defaultdict
import time

# Track time in zone
person_zone_time = defaultdict()
LOITER_THRESHOLD = 10  # seconds

for detection in results:
    person_id = detection.id
    person_location = detection.bbox_center
    
    if point_in_zone(person_location, ALERT_ZONE):
        if person_id not in person_zone_time:
            person_zone_time[person_id] = time.time()
        else:
            elapsed = time.time() - person_zone_time[person_id]
            if elapsed > LOITER_THRESHOLD:
                print(f"LOITERING ALERT: Person {person_id} for {elapsed:.1f}s")
```

## 🎓 Notebook Features

The `Live_Tracking.ipynb` notebook includes:

1. **GPU Configuration Section**: Automatic device detection
2. **Model Loading**: Pre-configured YOLOv8 nano model
3. **Video Input Handling**: Support for files, streams, and webcams
4. **Real-time Detection**: Frame-by-frame processing
5. **Tracking Management**: Maintaining object IDs across frames
6. **Zone Configuration**: Customizable alert regions
7. **Event Logging**: Recording suspicious activities
8. **Visualization**: Real-time frame annotation and display

## 📊 Model Performance

| Model | Speed (ms) | mAP | Parameters |
|-------|-----------|-----|------------|
| YOLOv8n (nano) | 45 | 37.3 | 3.2M |
| YOLOv8s (small) | 66 | 44.9 | 11.2M |
| YOLOv8m (medium) | 106 | 50.2 | 25.9M |

*Note: Times are approximate for GPU (CUDA) inference*

## 🔧 Configuration Parameters

Customize behavior by modifying these variables:

```python
DEVICE = 'cuda:0'                # GPU device or 'cpu'
MODEL_PATH = 'yolov8n.pt'       # Model weights path
CONFIDENCE_THRESHOLD = 0.5       # Detection confidence (0-1)
LOITER_THRESHOLD = 10            # Seconds before loitering alert
VIDEO_PATH = 'input_video.mp4'  # Video source path
OUTPUT_PATH = 'output_video.mp4' # Save annotated video
FRAME_RATE = 30                  # FPS for video output
```

## 🌙 Night Vision Optimization

For better low-light performance:

1. **Increase Input Image Brightness**
   ```python
   # Apply histogram equalization
   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   frame[:, :, 2] = cv2.equalizeHist(frame[:, :, 2])
   frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
   ```

2. **Use Larger YOLOv8 Models**
   - Switch from `yolov8n.pt` to `yolov8s.pt` or `yolov8m.pt` for better accuracy

3. **Adjust Confidence Threshold**
   - Lower threshold (0.3-0.4) for night scenarios but may increase false positives

## 📤 Output & Results

The system generates:

- **Annotated Video**: Frames with bounding boxes and tracking IDs
- **Event Log**: Timestamps and descriptions of detected events
- **Statistics**: Detection counts, tracking accuracy metrics
- **Alert Notifications**: Real-time or saved alerts for suspicious activities

## 🎯 Use Cases

1. **Home Security**: Monitor property perimeters and entry points
2. **Retail Security**: Track suspicious shoplifters and protect merchandise
3. **Corporate Facilities**: Monitor restricted areas and unauthorized access
4. **Parking Lot Surveillance**: Detect loitering vehicles and persons
5. **Event Management**: Monitor crowd behavior and security
6. **Transportation Hubs**: Track movement patterns at stations and terminals

## 🐛 Troubleshooting

### GPU Not Detected
```python
# Verify CUDA installation
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

### Model Not Found
```bash
# Download model manually
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Low FPS Performance
- Reduce frame resolution: `frame = cv2.resize(frame, (640, 480))`
- Use smaller model: Switch to `yolov8n.pt` from `yolov8m.pt`
- Enable mixed precision: Add `half=True` to model inference

### Poor Detection in Low Light
- Enable histogram equalization (see Night Vision section)
- Use larger model size
- Increase confidence threshold for fewer false positives

## 📚 Resources & References

- [YOLOv8 Official Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [YOLOv8 GitHub Repository](https://github.com/ultralytics/ultralytics)

## 📝 Project Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| ultralytics | ≥8.0.0 | YOLOv8 implementation |
| opencv-python | ≥4.6.0 | Computer vision library |
| torch | ≥1.12.0 | Deep learning framework |
| torchvision | ≥0.13.0 | Vision utilities |
| numpy | ≥1.23.0 | Numerical computing |
| ipywidgets | Latest | Interactive notebook features |

## 🚀 Advanced Features

### Custom Model Training
To train on your custom dataset:
```bash
# Prepare dataset in YOLOv8 format
python -m ultralytics.yolo detect train data=custom_data.yaml model=yolov8n.pt epochs=100 imgsz=640
```

### Model Export
Export to different formats for deployment:
```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.export(format='onnx')  # ONNX format
model.export(format='tflite')  # TensorFlow Lite
```

## 📄 License

This project uses models and code from Ultralytics. Please refer to the [Ultralytics License](https://www.ultralytics.com/license) for usage terms.

## 👨‍💻 Author

**Sachin Paunikar**

For questions, issues, or contributions, please refer to the main repository documentation.

---

**Last Updated:** November 2024
**Status:** Production Ready
**Maintained By:** Sachin Paunikar
