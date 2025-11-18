# Contributing to Advanced Computer Vision Suite

First off, thank you for considering contributing to this project! 🎉

It's people like you that make the open-source computer vision community such a fantastic place to learn, inspire, and create. Every contribution helps make this project better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Pull Request Process](#-pull-request-process)
- [Coding Standards](#-coding-standards)
- [Testing Guidelines](#-testing-guidelines)
- [Documentation Standards](#-documentation-standards)
- [Community](#-community)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and harassment-free environment. By participating, you are expected to uphold this standard.

### Our Standards

**Examples of encouraged behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by opening an issue or contacting the project maintainer. All complaints will be reviewed and investigated promptly and fairly.

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Use input '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots/Logs**
If applicable, add screenshots or error logs.

**Environment:**
- OS: [e.g. Ubuntu 22.04, Windows 11]
- Python version: [e.g. 3.10.12]
- PyTorch version: [e.g. 2.3.0]
- CUDA version: [e.g. 11.8]
- GPU: [e.g. RTX 3060]

**Additional context**
Add any other context about the problem.
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

**Enhancement Template:**
```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. I'm frustrated when [...]

**Describe the solution you'd like**
Clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Use case**
Describe the real-world scenario where this would be useful.

**Additional context**
Mockups, diagrams, or examples from other projects.
```

### 🔧 Contributing Code

We love pull requests! Here are areas where contributions are especially welcome:

#### High-Priority Areas
- 🎯 **Performance Optimization**: Improve FPS, reduce memory usage
- 🌙 **Low-Light Enhancement**: Better night vision detection
- 📊 **New Tracking Algorithms**: SORT, DeepSORT, ByteTrack implementations
- 🔌 **Integration Examples**: Flask API, FastAPI, gRPC services
- 📱 **Mobile Deployment**: TensorFlow Lite, NCNN conversions
- 🧪 **Test Coverage**: Unit tests, integration tests, benchmark tests

#### Medium-Priority Areas
- 📚 **Documentation**: Tutorials, API docs, use case examples
- 🌍 **Multi-Language Support**: Internationalization (i18n)
- 🎨 **Visualization Tools**: Better annotation UI, dashboard
- 🔊 **Alert Systems**: Email, SMS, webhook notifications
- 🗄️ **Database Integration**: PostgreSQL, MongoDB logging

#### Good First Issues
Look for issues labeled `good first issue` - these are perfect for newcomers!

---

## 🛠️ Development Setup

### Prerequisites

```bash
# Required
Python >= 3.10
Git >= 2.30
CUDA >= 11.8 (optional, for GPU acceleration)

# Recommended
Miniconda/Anaconda for environment management
VS Code with Python extension
```

### Fork & Clone

```bash
# 1. Fork the repository on GitHub (click "Fork" button)

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/yolov5-yolov8-computer-vision.git
cd yolov5-yolov8-computer-vision

# 3. Add upstream remote
git remote add upstream https://github.com/ImdataScientistSachin/yolov5-yolov8-computer-vision.git

# 4. Verify remotes
git remote -v
# origin    https://github.com/YOUR_USERNAME/yolov5-yolov8-computer-vision.git (fetch)
# upstream  https://github.com/ImdataScientistSachin/yolov5-yolov8-computer-vision.git (fetch)
```

### Environment Setup

```bash
# Create virtual environment
conda create -n cv-contrib python=3.10
conda activate cv-contrib

# Install dependencies
cd yolov5
pip install -r requirements.txt

cd "../YOLOv8 and OpenCV built-in tracking"
pip install ultralytics opencv-python torch numpy

# Install development tools
pip install pytest pytest-cov black flake8 mypy pre-commit

# Set up pre-commit hooks (optional but recommended)
pre-commit install
```

### Verify Installation

```bash
# Test YOLOv5
cd yolov5
python detect.py --weights yolov5s.pt --source data/images/bus.jpg

# Test YOLOv8
cd "../YOLOv8 and OpenCV built-in tracking"
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('✓ YOLOv8 working')"
```

---

## 🔄 Pull Request Process

### 1. Create a Feature Branch

```bash
# Sync with upstream first
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch (use descriptive names)
git checkout -b feature/add-bytetrack-tracker
# or
git checkout -b fix/memory-leak-loitering
# or
git checkout -b docs/update-export-tutorial
```

### 2. Make Your Changes

Follow the [Coding Standards](#-coding-standards) and commit often with clear messages:

```bash
git add .
git commit -m "feat: add ByteTrack multi-object tracker"
# or
git commit -m "fix: resolve memory leak in loitering detection"
# or
git commit -m "docs: add TensorRT export tutorial"
```

**Commit Message Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style/formatting (no logic change)
- `refactor:` Code restructuring (no behavior change)
- `perf:` Performance improvement
- `test:` Add or update tests
- `chore:` Maintenance tasks

### 3. Test Your Changes

```bash
# Run existing tests
pytest tests/ -v

# Add new tests for your changes
# tests/test_your_feature.py

# Check code quality
black . --check
flake8 . --max-line-length=120
mypy . --ignore-missing-imports
```

### 4. Update Documentation

- Add/update docstrings for new functions
- Update README.md if adding major features
- Add examples in `examples/` folder
- Update CHANGELOG.md (if exists)

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/add-bytetrack-tracker

# Go to GitHub and click "Compare & pull request"
```

### 6. PR Template

Your PR should include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested on local machine (specify OS, GPU)
- [ ] Added unit tests
- [ ] All existing tests pass
- [ ] Benchmarked performance (if applicable)

## Performance Impact
- FPS: Before X → After Y
- Memory: Before Xmb → After Ymb
- Accuracy: Before X% → After Y%

## Screenshots/Demo
(If applicable, add screenshots or GIF demos)

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Related Issues
Closes #123
Related to #456
```

### 7. Code Review Process

- Maintainers will review your PR within 3-7 days
- Address review comments by pushing new commits
- Once approved, a maintainer will merge your PR
- Your contribution will be credited in the release notes!

---

## 💻 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 120 characters (not 79)
# Use Black formatter with default settings

# Good examples:

def detect_loitering(
    tracker_data: Dict[int, List[float]],
    threshold_seconds: float = 10.0,
    zone_coords: Optional[List[Tuple[float, float]]] = None
) -> List[int]:
    """
    Detect loitering behavior based on tracking history.
    
    Args:
        tracker_data: Dictionary mapping object IDs to timestamp lists
        threshold_seconds: Minimum time in seconds to trigger loitering alert
        zone_coords: Optional zone coordinates as [(x1,y1), (x2,y2), ...]
    
    Returns:
        List of object IDs that are loitering
    
    Example:
        >>> tracker_data = {1: [0.0, 1.5, 3.0, 10.5], 2: [0.0, 2.0]}
        >>> detect_loitering(tracker_data, threshold_seconds=10.0)
        [1]
    """
    loitering_ids = []
    
    for obj_id, timestamps in tracker_data.items():
        if len(timestamps) < 2:
            continue
            
        duration = timestamps[-1] - timestamps[0]
        if duration >= threshold_seconds:
            loitering_ids.append(obj_id)
    
    return loitering_ids


# Use type hints
def process_frame(frame: np.ndarray, model: YOLO) -> Tuple[np.ndarray, List[Detection]]:
    pass


# Use descriptive variable names
tracking_results = model.track(source=video_path)  # Good
res = model.track(src=vid)  # Bad


# Constants in UPPERCASE
LOITERING_THRESHOLD = 10.0
MAX_TRACKING_OBJECTS = 100
DEFAULT_CONFIDENCE = 0.3
```

### Code Organization

```python
# File structure:
"""
Module docstring explaining purpose.
"""

# 1. Standard library imports
import os
import sys
from typing import Dict, List, Optional

# 2. Third-party imports
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# 3. Local imports
from utils.tracking import initialize_tracker
from config import Config

# 4. Constants
DEFAULT_MODEL = "yolov8n.pt"
FPS_SMOOTHING_WINDOW = 30

# 5. Classes and functions
class SecuritySystem:
    """Production-grade security monitoring system."""
    pass


def main():
    """Entry point for CLI usage."""
    pass


# 6. Script execution
if __name__ == "__main__":
    main()
```

### Error Handling

```python
# Always use specific exceptions
try:
    model = YOLO(model_path)
except FileNotFoundError:
    logger.error(f"Model file not found: {model_path}")
    raise
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

# Use context managers for resources
with open(output_path, 'w') as f:
    json.dump(results, f)

# Validate inputs
def set_threshold(value: float) -> None:
    if not 0 < value < 60:
        raise ValueError(f"Threshold must be between 0 and 60 seconds, got {value}")
```

---

## 🧪 Testing Guidelines

### Writing Tests

```python
# tests/test_loitering.py
import pytest
from security_system import detect_loitering


class TestLoiteringDetection:
    """Test suite for loitering detection functionality."""
    
    def test_basic_loitering_detection(self):
        """Test simple loitering case with one object."""
        tracker_data = {
            1: [0.0, 5.0, 10.0, 15.0]  # 15 seconds tracked
        }
        result = detect_loitering(tracker_data, threshold_seconds=10.0)
        assert result == [1]
    
    def test_no_loitering(self):
        """Test that short durations don't trigger loitering."""
        tracker_data = {
            1: [0.0, 2.0, 4.0]  # Only 4 seconds
        }
        result = detect_loitering(tracker_data, threshold_seconds=10.0)
        assert result == []
    
    def test_multiple_objects(self):
        """Test with multiple tracked objects."""
        tracker_data = {
            1: [0.0, 5.0, 12.0],  # Loitering
            2: [0.0, 3.0],        # Not loitering
            3: [0.0, 8.0, 15.0]   # Loitering
        }
        result = detect_loitering(tracker_data, threshold_seconds=10.0)
        assert set(result) == {1, 3}
    
    @pytest.mark.parametrize("threshold,expected", [
        (5.0, [1, 2]),
        (10.0, [1]),
        (20.0, [])
    ])
    def test_threshold_variations(self, threshold, expected):
        """Test different threshold values."""
        tracker_data = {
            1: [0.0, 15.0],
            2: [0.0, 7.0]
        }
        result = detect_loitering(tracker_data, threshold_seconds=threshold)
        assert set(result) == set(expected)


# Run tests:
# pytest tests/ -v --cov=. --cov-report=html
```

### Performance Benchmarks

```python
# tests/test_performance.py
import time
import pytest
from ultralytics import YOLO


@pytest.mark.benchmark
def test_inference_speed():
    """Benchmark inference FPS on standard input."""
    model = YOLO('yolov8n.pt')
    
    # Warmup
    for _ in range(10):
        model.predict('data/images/bus.jpg')
    
    # Benchmark
    start = time.time()
    num_frames = 100
    for _ in range(num_frames):
        model.predict('data/images/bus.jpg')
    
    elapsed = time.time() - start
    fps = num_frames / elapsed
    
    assert fps > 50, f"Expected >50 FPS, got {fps:.1f}"
```

---

## 📚 Documentation Standards

### Docstring Format (Google Style)

```python
def track_objects(
    model: YOLO,
    source: str,
    conf: float = 0.3,
    iou: float = 0.5,
    tracker: str = "botsort.yaml"
) -> Generator[Results, None, None]:
    """
    Track objects in video with persistent IDs.
    
    This function wraps Ultralytics YOLO tracking with enhanced
    error handling and logging for production use.
    
    Args:
        model: Initialized YOLO model instance
        source: Path to video file, image folder, or camera index (0)
        conf: Confidence threshold for detections (0.0-1.0)
        iou: IoU threshold for NMS (0.0-1.0)
        tracker: Tracker config file name ('botsort.yaml' or 'bytetrack.yaml')
    
    Returns:
        Generator yielding Results objects for each frame
    
    Raises:
        FileNotFoundError: If source video file doesn't exist
        ValueError: If invalid confidence/IOU thresholds provided
        RuntimeError: If tracking initialization fails
    
    Example:
        >>> model = YOLO('yolov8n.pt')
        >>> for result in track_objects(model, 'video.mp4', conf=0.4):
        ...     boxes = result.boxes
        ...     ids = result.boxes.id  # Tracking IDs
        ...     print(f"Frame: {len(boxes)} objects")
    
    Note:
        Requires sufficient GPU memory for video processing.
        Use smaller model (yolov8n) for real-time on limited hardware.
    
    See Also:
        - detect_objects: For single-frame detection without tracking
        - process_stream: For live camera streams
    """
    pass
```

### README Documentation

When adding new features, update README.md with:
- Clear feature description
- Code examples
- Configuration options
- Performance metrics (if applicable)
- Troubleshooting tips

---

## 🌟 Recognition

### Contributors Wall of Fame

All contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for version releases
- **GitHub Contributors** page (automatic)

### Significant Contributions

Major contributors (10+ merged PRs or significant features) may be invited as:
- **Project Collaborators** (write access)
- **Core Team Members** (architectural decisions)

---

## 📬 Community

### Getting Help

- 💬 **GitHub Discussions**: General questions, ideas, show-and-tell
- 🐛 **GitHub Issues**: Bug reports, feature requests
- 📧 **Email**: For security vulnerabilities or private matters
- 🔗 **LinkedIn**: Professional networking and collaboration

### Stay Updated

- ⭐ **Star the repo** to get notifications for releases
- 👁️ **Watch the repo** for all activity updates
- 📰 **Check Releases** for changelogs and announcements

---

## 📖 Additional Resources

### Learning Materials
- [Git Workflow Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Writing Great Commit Messages](https://chris.beams.io/posts/git-commit/)
- [Python Type Hints Guide](https://realpython.com/python-type-checking/)
- [Pytest Documentation](https://docs.pytest.org/)

### Ultralytics Resources
- [YOLOv8 Custom Training Guide](https://docs.ultralytics.com/modes/train/)
- [Tracking Documentation](https://docs.ultralytics.com/modes/track/)
- [Export Formats Guide](https://docs.ultralytics.com/modes/export/)

---

## ❓ Questions?

Don't hesitate to ask! We're here to help:

- Open a **Discussion** for general questions
- Open an **Issue** if you think you found a bug
- Reach out via **LinkedIn** for collaboration ideas

**Thank you for contributing! Together we're building the best open-source computer vision security system.** 🚀

---

<div align="center">

**Happy Coding!** 💻✨

*Last Updated: November 18, 2025*

</div>
