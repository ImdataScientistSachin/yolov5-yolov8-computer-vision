# YOLOv5: State-of-the-Art Object Detection & Segmentation

**Author:** Sachin Paunikar

## Overview

YOLOv5 is a cutting-edge, state-of-the-art (SOTA) computer vision model developed by Ultralytics for real-time object detection, instance segmentation, and image classification. Built on PyTorch, YOLOv5 combines ease of use, speed, and accuracy to tackle diverse vision AI challenges. This repository contains a comprehensive implementation with training, inference, and deployment capabilities.

## 🚀 Key Highlights

- **Ultra-Fast Detection**: Process images and videos in real-time with minimal latency
- **High Accuracy**: Achieve state-of-the-art mean Average Precision (mAP) scores
- **Multiple Model Sizes**: Choose from nano to extra-large models based on speed/accuracy trade-offs
- **Full Pipeline Support**: Detection, segmentation, classification, and pose estimation
- **Cross-Platform Deployment**: Export to ONNX, TensorRT, CoreML, TensorFlow, and more
- **Easy Integration**: Simple Python API for seamless integration into applications
- **Active Community**: Extensive documentation and community support

## 📋 Project Features

### 1. **Multiple Task Support**
   - **Object Detection**: Precise localization and classification of objects
   - **Instance Segmentation**: Pixel-level object segmentation masks
   - **Image Classification**: Categorize entire images into predefined classes
   - **Pose Estimation**: Detect and track human keypoints

### 2. **Model Variants**
   - **YOLOv5n (Nano)**: Lightweight, fastest, ideal for edge devices
   - **YOLOv5s (Small)**: Balanced speed and accuracy
   - **YOLOv5m (Medium)**: Enhanced accuracy with reasonable speed
   - **YOLOv5l (Large)**: High accuracy for demanding applications
   - **YOLOv5x (Extra-Large)**: Maximum accuracy for research

### 3. **Comprehensive Training Pipeline**
   - Multi-GPU distributed training support
   - Advanced data augmentation (Mosaic, MixUp, CutMix)
   - Automatic hyperparameter optimization
   - Mixed precision training for faster convergence
   - Real-time training visualization

### 4. **Inference Capabilities**
   - Batch processing for high throughput
   - GPU and CPU support
   - Webcam and stream processing
   - Video file detection and annotation
   - Multi-source input handling

### 5. **Export & Deployment**
   - PyTorch native format
   - ONNX (Open Neural Network Exchange)
   - TensorFlow SavedModel and Lite
   - TensorRT for NVIDIA GPUs
   - CoreML for Apple devices
   - OpenVINO for Intel hardware
   - PaddlePaddle for mobile deployment

## 📁 Repository Structure

```
yolov5/
├── models/                      # Model architectures
│   ├── __init__.py
│   ├── yolo.py                 # Core YOLO implementation
│   ├── common.py               # Common backbone components
│   ├── experimental.py         # Experimental architectures
│   ├── yolov5n.yaml            # Nano model config
│   ├── yolov5s.yaml            # Small model config
│   ├── yolov5m.yaml            # Medium model config
│   ├── yolov5l.yaml            # Large model config
│   ├── yolov5x.yaml            # Extra-large model config
│   └── hub/                    # Hub configurations
├── utils/                      # Utility modules
│   ├── general.py              # General utilities
│   ├── dataloaders.py          # Data loading and preprocessing
│   ├── augmentations.py        # Image augmentation techniques
│   ├── loss.py                 # Loss function definitions
│   ├── metrics.py              # Evaluation metrics
│   ├── plots.py                # Visualization utilities
│   ├── torch_utils.py          # PyTorch helpers
│   ├── autoanchor.py           # Anchor optimization
│   ├── autobatch.py            # Batch size optimization
│   └── loggers/                # Logging integrations
├── segment/                    # Instance segmentation module
│   ├── predict.py             # Segmentation inference
│   ├── train.py               # Segmentation training
│   ├── val.py                 # Segmentation validation
│   └── tutorial.ipynb         # Segmentation tutorial
├── classify/                   # Image classification module
│   ├── predict.py             # Classification inference
│   ├── train.py               # Classification training
│   ├── val.py                 # Classification validation
│   └── tutorial.ipynb         # Classification tutorial
├── data/                      # Dataset configurations
│   ├── coco.yaml              # COCO dataset config
│   ├── coco128.yaml           # COCO128 mini dataset
│   ├── VOC.yaml               # Pascal VOC config
│   ├── custom.yaml            # Custom dataset template
│   └── hyps/                  # Hyperparameter configs
├── detect.py                  # Inference script for object detection
├── detect_org.py              # Original detection implementation
├── train.py                   # Main training script
├── val.py                     # Validation script
├── export.py                  # Model export utility
├── hubconf.py                 # PyTorch Hub integration
├── requirements.txt           # Project dependencies
├── pyproject.toml             # Project metadata and build config
├── tutorial.ipynb             # Comprehensive tutorial notebook
├── LICENSE                    # Project license (AGPL-3.0)
├── README.md                  # Official documentation
└── README.zh-CN.md            # Chinese documentation
```

## 🛠️ Installation

### Prerequisites

- **Python 3.8 or higher**
- **PyTorch 1.12.0+** with CUDA support (optional but recommended)
- **pip** package manager

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ultralytics/yolov5
   cd yolov5
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install with GPU Support (Recommended)**
   ```bash
   # For CUDA 12.1
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   
   # For CUDA 11.8
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   
   # For CPU only
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

4. **Verify Installation**
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
   python -c "from models.yolo import Model; print('YOLOv5 ready!')"
   ```

## 🚀 Quick Start

### Object Detection (Inference)

**Using PyTorch Hub (Easiest)**
```python
import torch

# Load a pretrained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Inference on an image
img = 'https://ultralytics.com/images/zidane.jpg'
results = model(img)

# Display results
results.print()
results.show()
```

**Using detect.py Script**
```bash
# Webcam detection
python detect.py --weights yolov5s.pt --source 0

# Image detection
python detect.py --weights yolov5s.pt --source path/to/image.jpg

# Video detection
python detect.py --weights yolov5s.pt --source path/to/video.mp4

# Multiple sources
python detect.py --weights yolov5s.pt --source img1.jpg img2.jpg path/to/video.mp4

# URL source
python detect.py --weights yolov5s.pt --source 'https://youtu.be/LNwODJXcvt4'
```

### Object Detection (Custom Python)

```python
from ultralytics import YOLO
import cv2

# Load model
model = YOLO('yolov5s.pt')

# Load image
image = cv2.imread('image.jpg')

# Run inference
results = model(image)

# Access results
for detection in results:
    boxes = detection.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        confidence = box.conf[0]
        class_id = box.cls[0]
        print(f"Box: ({x1}, {y1}, {x2}, {y2}), Conf: {confidence:.2f}, Class: {class_id}")

# Visualize
annotated_image = results[0].plot()
cv2.imshow('YOLOv5 Detection', annotated_image)
cv2.waitKey(0)
```

### Training on Custom Dataset

**Prepare Your Dataset**
```
dataset/
├── images/
│   ├── train/     # Training images
│   ├── val/       # Validation images
│   └── test/      # Test images
└── labels/
    ├── train/     # Training labels (YOLO format)
    ├── val/       # Validation labels
    └── test/      # Test labels
```

**Create Dataset Configuration**
```yaml
# data/custom.yaml
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

nc: 80  # Number of classes
names: ['person', 'car', 'dog', ...]  # Class names
```

**Train Model**
```bash
# Single GPU training
python train.py --data data/custom.yaml --weights yolov5s.pt --img 640 --epochs 100

# Multi-GPU training
python -m torch.distributed.run --nproc_per_node 4 train.py \
    --data data/custom.yaml --weights yolov5s.pt --img 640 --epochs 100 --device 0,1,2,3

# Train from scratch
python train.py --data data/custom.yaml --cfg models/yolov5s.yaml --img 640 --epochs 100
```

**Training Arguments**
```bash
python train.py --data data/custom.yaml \
    --weights yolov5s.pt \           # Pretrained weights
    --img 640 \                      # Image size
    --batch 16 \                     # Batch size
    --epochs 100 \                   # Number of epochs
    --patience 20 \                  # Early stopping patience
    --augment \                      # Use augmentation
    --cache ram \                    # Cache images in RAM
    --device 0 \                     # GPU device
    --workers 8 \                    # Data loader workers
    --name experiment1               # Run name
```

### Model Validation

```bash
# Validate on validation set
python val.py --weights yolov5s.pt --data data/coco.yaml --img 640

# Validate with test augmentation
python val.py --weights yolov5s.pt --data data/coco.yaml --augment

# Save results
python val.py --weights yolov5s.pt --data data/coco.yaml --save-txt --save-conf
```

### Export Model

**Export to Different Formats**
```bash
# Export to ONNX
python export.py --weights yolov5s.pt --include onnx

# Export to TensorFlow
python export.py --weights yolov5s.pt --include saved_model tflite

# Export to TensorRT
python export.py --weights yolov5s.pt --include engine

# Export to CoreML
python export.py --weights yolov5s.pt --include coreml

# Export multiple formats
python export.py --weights yolov5s.pt --include onnx tflite engine
```

## 📊 Performance Metrics

### Detection Performance

| Model | mAP@0.5 | mAP@0.5:0.95 | Speed (ms) | Params (M) |
|-------|---------|-------------|-----------|-----------|
| YOLOv5n | 45.7 | 28.0 | 45 | 1.9 |
| YOLOv5s | 56.8 | 37.2 | 98 | 7.2 |
| YOLOv5m | 60.3 | 41.2 | 224 | 21.2 |
| YOLOv5l | 62.9 | 43.3 | 430 | 46.5 |
| YOLOv5x | 64.7 | 45.7 | 766 | 86.7 |

*Metrics on COCO dataset with TensorRT acceleration on NVIDIA A100*

## 🎓 Advanced Topics

### Custom Loss Functions

Edit `utils/loss.py` to implement custom loss functions:

```python
def custom_loss(predictions, targets):
    # Your custom loss implementation
    pass
```

### Hyperparameter Optimization

Use `data/hyps/` configuration files:

```bash
python train.py --data coco.yaml --hyp data/hyps/hyp.scratch-med.yaml
```

### Distributed Training

```bash
# 4 GPUs on single machine
python -m torch.distributed.run --nproc_per_node 4 train.py \
    --data coco.yaml --weights yolov5s.pt --device 0,1,2,3

# Multi-machine training (requires setup)
python -m torch.distributed.run --nproc_per_node 4 \
    --nnodes 2 --node_rank 0 --master_addr master_ip --master_port 29500 \
    train.py --data coco.yaml
```

### Instance Segmentation

```bash
# Train segmentation model
python segment/train.py --data coco.yaml --weights yolov5s-seg.pt

# Inference with segmentation
python segment/predict.py --weights yolov5s-seg.pt --source image.jpg
```

### Image Classification

```bash
# Train classification model
python classify/train.py --data ImageNet --weights yolov5s-cls.pt

# Classify images
python classify/predict.py --weights yolov5s-cls.pt --source image.jpg
```

## 🔧 Configuration Reference

### Training Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `img` | 640 | Input image size |
| `batch` | 16 | Batch size |
| `epochs` | 100 | Training epochs |
| `patience` | 20 | Early stopping patience |
| `device` | 0 | GPU device |
| `workers` | 8 | Data loader workers |
| `cache` | - | Cache images (ram/disk) |
| `augment` | True | Use augmentation |
| `flipud` | 0.5 | Vertical flip probability |
| `fliplr` | 0.5 | Horizontal flip probability |
| `mosaic` | 1.0 | Mosaic augmentation ratio |
| `mixup` | 0.1 | MixUp augmentation ratio |

### Inference Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `conf` | 0.25 | Confidence threshold |
| `iou` | 0.45 | IoU threshold for NMS |
| `max-det` | 300 | Maximum detections |
| `device` | 0 | GPU device |
| `half` | False | Use FP16 inference |
| `dnn` | False | Use OpenCV DNN |

## 📚 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| torch | ≥1.12.0 | Deep learning framework |
| torchvision | ≥0.13.0 | Vision utilities |
| numpy | ≥1.23.5 | Numerical computing |
| opencv-python | ≥4.6.0 | Image processing |
| PyYAML | ≥5.3.1 | Configuration handling |
| requests | ≥2.32.2 | HTTP library |
| tqdm | ≥4.66.3 | Progress bars |
| pillow | ≥10.3.0 | Image library |
| matplotlib | ≥3.3 | Visualization |
| scipy | ≥1.4.1 | Scientific computing |
| ultralytics | ≥8.2.34 | Latest YOLO utilities |

## 🐛 Troubleshooting

### CUDA Out of Memory
```bash
# Reduce batch size
python train.py --batch 8 --img 640

# Use smaller model
python train.py --weights yolov5n.pt

# Enable automatic mixed precision
python train.py --device 0 --amp
```

### Poor Detection Accuracy
- Increase model size (yolov5l or yolov5x)
- Collect more training data
- Improve data quality and labeling
- Increase training epochs
- Adjust learning rate and optimizer

### Slow Training
- Increase batch size (if GPU memory allows)
- Use mixed precision training
- Reduce image size
- Use data augmentation caching

### Model Not Found
```bash
# Download manually
python -c "from models.yolo import Model; import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s')"
```

## 📖 Documentation & Resources

- [Official YOLOv5 Docs](https://docs.ultralytics.com/yolov5/)
- [Ultralytics Blog](https://www.ultralytics.com/blog/)
- [GitHub Issues](https://github.com/ultralytics/yolov5/issues)
- [Community Forum](https://community.ultralytics.com/)
- [YouTube Tutorials](https://www.youtube.com/ultralytics)

## 🎯 Common Use Cases

1. **Retail Analytics**: Customer tracking and behavior analysis
2. **Manufacturing QC**: Defect detection and quality assurance
3. **Traffic Monitoring**: Vehicle and pedestrian detection
4. **Medical Imaging**: Anomaly detection in X-rays and scans
5. **Agriculture**: Crop health monitoring and pest detection
6. **Security**: Surveillance and threat detection
7. **Robotics**: Navigation and obstacle avoidance
8. **Sports**: Player tracking and game analytics

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. 
See the [LICENSE](./LICENSE) file for details.

For commercial licensing, visit [Ultralytics Licensing](https://www.ultralytics.com/license).

## 👥 Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## 🙏 Acknowledgments

- **Ultralytics** team for YOLOv5 development and maintenance
- **PyTorch** team for the excellent deep learning framework
- **OpenCV** for computer vision utilities
- Community contributors and researchers

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/ultralytics/yolov5/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ultralytics/yolov5/discussions)
- **Community**: [Ultralytics Community Forum](https://community.ultralytics.com/)
- **Email**: For enterprise support, contact Ultralytics

---

**Author:** Sachin Paunikar

**Last Updated:** November 2024

**Status:** Production Ready

**Version:** 7.0.0

For the most up-to-date information, visit the [official Ultralytics repository](https://github.com/ultralytics/yolov5).
