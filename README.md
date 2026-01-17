# 🌟 The "Jedi" Volume & Brightness Controller

> A futuristic, touch-free interface that lets you control your computer's audio and screen brightness using hand gestures, inspired by *Minority Report*.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-orange) ![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green)

## 📖 About
This project uses **Computer Vision** and **AI Hand Tracking** to detect your hand gestures in real-time. By calculating the distance between your thumb and index finger, you can adjust system settings without ever touching the keyboard.

## ✨ Features
* **🔊 Volume Control (Right Hand):** Pinch to lower volume, spread to raise it.
* **🔆 Brightness Control (Left Hand):** Pinch to dim screen, spread to brighten.
* **🔇 Instant Mute:** Make a **Fist** with either hand to instantly mute/unmute.
* **📊 Head-Up Display (HUD):** Visual bars and percentage indicators on-screen.
* **🌊 Smooth Motion:** Integrated smoothing algorithms to prevent jittery controls.

## 🛠️ Requirements
* **Python 3.11** (Recommended due to MediaPipe compatibility)
* Webcam

### Libraries
```txt
opencv-python
mediapipe==0.10.9
screen-brightness-control
pycaw
numpy
comtypes
protobuf==3.20.3
