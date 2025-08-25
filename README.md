

### **Project Description**

This project presents a perception algorithm for lane detection in self-driving car systems, relying purely on vision-based data from a camera. It demonstrates a complete, end-to-end lane detection method using classic computer vision techniques. The core of the project is a foundational approach based on **edge detection** and the **Hough Transform** algorithm, which serves as a baseline for identifying straight lane lines in both images and video streams. The process is broken down into a series of logical steps, from initial image processing to final visualization of the detected lanes.

### **Technical Stack**
* **Programming Language**: Python
* **Libraries**:
    * **OpenCV**: For core computer vision tasks, including image processing and video handling.
    * **NumPy**: For numerical operations, particularly for manipulating image arrays.
    * **Matplotlib**: Used for visualizing the processed images and results.

### **Algorithm Steps**
The lane detection pipeline follows these sequential steps:
1.  **Convert to Grayscale**: Reduces the image to a single color channel to simplify processing.
2.  **Noise Reduction**: Applies filters to remove noise and smooth the image.
3.  **Edge Detection**: Uses an algorithm like Canny edge detection to identify sharp changes in image intensity.
4.  **Region of Interest**: Masks the image to focus only on the relevant area where lanes are expected to be.
5.  **Detecting Straight Lines**: Applies the **Hough Transform** to identify potential straight lines within the defined region.
6.  **Averaging the Lines**: Combines the detected line segments into two solid lines representing the left and right lanes.
7.  **Displaying Final Image**: Overlays the detected lanes onto the original image for a clear visual representation.
8.  **Video Processing**: Extends the algorithm to apply the same steps to each frame of a video stream to achieve real-time lane detection.
