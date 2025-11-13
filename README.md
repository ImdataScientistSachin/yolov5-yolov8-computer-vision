# Computer Vision & Object Detection Projects

**Author:** Sachin Paunikar

A comprehensive collection of advanced computer vision projects featuring state-of-the-art object detection, tracking, and analysis capabilities.

## 📁 Projects Included

### 1. [YOLOv8 and OpenCV Built-in Tracking](./YOLOv8%20and%20OpenCV%20built-in%20tracking)
Real-time security surveillance system with advanced tracking capabilities. Features person detection, tracking, and loitering detection for security applications.

**Key Features:**
- Real-time YOLOv8 object detection
- Multi-object tracking with persistent IDs
- Zone-based security alerts
- Loitering detection
- Night vision optimization
- GPU acceleration support

[Read Full Documentation](./YOLOv8%20and%20OpenCV%20built-in%20tracking/README.md)

---

### 2. [YOLOv5: State-of-the-Art Object Detection](./yolov5)
Comprehensive YOLOv5 implementation with training, inference, and deployment capabilities. Supports object detection, instance segmentation, and image classification.

**Key Features:**
- Multiple model sizes (nano to extra-large)
- Fast inference with high accuracy
- Full training pipeline with custom datasets
- Export to multiple formats (ONNX, TensorRT, CoreML, etc.)
- Instance segmentation support
- Image classification module
- Multi-GPU training support

[Read Full Documentation](./yolov5/README_CUSTOM.md)

---

## 🚀 Quick Start

### YOLOv8 Security Tracking
```bash
cd "YOLOv8 and OpenCV built-in tracking"
pip install ultralytics opencv-python torch numpy
jupyter notebook Live_Tracking.ipynb
```

### YOLOv5 Object Detection
```bash
cd yolov5
pip install -r requirements.txt

# Run inference
python detect.py --weights yolov5s.pt --source 0  # webcam

# Train custom model
python train.py --data data/custom.yaml --weights yolov5s.pt --img 640
```

## 📋 Requirements

### Common Dependencies
- Python 3.8+
- PyTorch 1.12.0+
- CUDA 11.8+ (optional, for GPU acceleration)

### Project-Specific
Each project has detailed requirements in their respective README files.

## 📚 Documentation

- **YOLOv8 Tracking**: [Complete Documentation](./YOLOv8%20and%20OpenCV%20built-in%20tracking/README.md)
- **YOLOv5 Detection**: [Complete Documentation](./yolov5/README_CUSTOM.md)

## 🎯 Use Cases

### YOLOv8 Tracking
- Home security systems
- Retail security and anti-theft
- Perimeter monitoring
- Loitering detection
- Event surveillance

### YOLOv5 Detection
- Object detection in images and videos
- Custom model training
- Multi-class detection
- Instance segmentation
- Image classification

## 📊 Model Performance

### YOLOv8 (Nano)
- Speed: ~45ms per frame
- Accuracy: 37.3 mAP
- Parameters: 3.2M

### YOLOv5 (Small)
- mAP@0.5: 56.8
- mAP@0.5:0.95: 37.2
- Speed: 98ms
- Parameters: 7.2M

## 🔧 Installation

### Clone Repository
```bash
git clone https://github.com/ImdataScientistSachin/project_yolo.git
cd project_yolo
```

### Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd yolov5
pip install -r requirements.txt
```

## 📝 Project Structure

```
project_yolo/
├── YOLOv8 and OpenCV built-in tracking/
│   ├── README.md                 # Project documentation
│   ├── Live_Tracking.ipynb       # Interactive notebook
│   └── yolov8n.pt               # Model weights
├── yolov5/
│   ├── README_CUSTOM.md         # Project documentation
│   ├── detect.py                # Inference script
│   ├── train.py                 # Training script
│   ├── requirements.txt         # Dependencies
│   └── models/                  # Model configurations
└── README.md                    # This file
```

## 🐛 Troubleshooting

Refer to the individual project README files for specific troubleshooting guidance:
- [YOLOv8 Tracking Troubleshooting](./YOLOv8%20and%20OpenCV%20built-in%20tracking/README.md#-troubleshooting)
- [YOLOv5 Troubleshooting](./yolov5/README_CUSTOM.md#-troubleshooting)

## 📄 License

These projects use components licensed under:
- **AGPL-3.0** for YOLOv5 and YOLOv8
- Individual project licenses apply (see project README files)

## 👨‍💻 Author

**Sachin Paunikar**

## 🤝 Contributing

Contributions are welcome! Please follow the guidelines in the individual project repositories.

## 📚 Resources

- [Ultralytics YOLOv5 Documentation](https://docs.ultralytics.com/yolov5/)
- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check individual project README files for detailed troubleshooting

---

**Last Updated:** November 2024
**Status:** Production Ready
