# Kao-janken: Computer Vision Tutorial with OpenCV and MediaPipe

A step-by-step Python tutorial for learning computer vision, featuring webcam capture, face detection, and interactive applications.

## Overview

This tutorial series guides you through building computer vision applications from basic webcam capture to an interactive rock-paper-scissors game using facial gestures. Each lesson builds upon the previous one, gradually introducing new concepts and techniques.

## Features

- 📹 Real-time webcam processing
- 🔍 Face mesh detection with MediaPipe
- 🖼️ Image overlay and blending
- 🎮 Interactive gesture-based game
- 📚 Progressive learning approach

## Prerequisites

- Python 3.12+
- Webcam (built-in or external)
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/computer-vision-tutorial.git
cd computer-vision-tutorial
```

2. Install dependencies with uv:
```bash
uv sync
```

## Usage

Run any lesson with uv:
```bash
uv run lesson_1.py
uv run lesson_8.py
uv run lesson_12.py
```

Press 'q' to quit any application.
Press 's' to save a photo (in applicable lessons).

## Key Concepts Covered

- **Computer Vision Fundamentals**: Image coordinates, color spaces, alpha channels
- **OpenCV Techniques**: Video capture, image processing, text overlays
- **MediaPipe Integration**: Face mesh detection, landmark extraction

## Troubleshooting

### Camera Issues
Ensure your webcam is not being used by another application. If you encounter resolution issues, try modifying the camera settings:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

## Acknowledgments

- [OpenCV](https://opencv.org/) for computer vision functionality
- [MediaPipe](https://mediapipe.dev/) for machine learning solutions
