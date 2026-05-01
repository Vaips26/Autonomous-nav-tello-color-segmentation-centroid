# Tello Autonomous Navigation using Color Segmentation

Autonomous navigation system for a DJI Tello drone based on computer vision.  
The drone detects orange frames using color segmentation in HSV space and navigates towards them using centroid-based control.

---

##  Features

- Real-time orange object detection (HSV color space)
- Centroid calculation for target tracking
- Autonomous forward navigation when aligned
- Search behavior when no target is detected
- Simple proportional control for smooth movement

---

##  How it works

1. The drone captures live video using its onboard camera  
2. The image is converted from BGR to HSV  
3. A mask is applied to detect orange regions  
4. Morphological operations reduce noise  
5. Contours are extracted and filtered by area  
6. The largest contour is selected  
7. The centroid is computed  
8. The drone adjusts its movement based on centroid position:

- If the object is off-center → adjust left/right or forward/backward  
- If centered → move forward  
- If no object detected → rotate to search  

---

##  Requirements

- Python 3.8+
- OpenCV
- NumPy
- djitellopy

Install dependencies:

```bash
pip install opencv-python numpy djitellopy
