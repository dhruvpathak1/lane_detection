# Hough Transform (Lane Detection) Algorithm
In this study, we present a perception algorithm that is based purely on vision or camera data. We focus on demonstrating an end-to-end lane detection method using contemporary computer vision techniques for self-driving cars. We first present a basic approach based on edge detection and Hough transform which is the baseline approach for detecting only the straight lane lines.
We will study in detail, detecting lanes in images as any lane detection in videos, is done on individual frames i.e. individual images.

## Programming Language: Python
## Libraries: OpenCV, Numpy, Pyplot from Matplot Lib
 
## I.	Convert to Grayscale
A conversion to grayscale is needed as the original image comprises of 3 channels (red, green, blue), meaning each pixel is a combination of 3 intensity values. Grayscale images consists of only 1 channel with each pixel having only 1 intensity value ranging from 0 to 255. This makes processing the image faster and easier.
(Grayscale) 0 in 2nd parameter makes it black and white

lane_img = cv2.imread("lane_pic.jpg", 0)
Another way to convert to grayscale
cv2.cvtColor(lane_img,cv2.COLOR_RGB2GRAY)
 
## II.	Reduction of noise
To detect lanes in an image, it is very important to detect the edges on an image (an edge in an image is a sharp change in intensity or colour of neighbouring pixels).
(Intensity 0 = Black, 255 = White)
Therefore, before we detect edges, any noise in the image is to be reduced to smoothen the image. This is done to prevent false edges being detected. Gaussian Blur is applied for this purpose.
•	Working of Gaussian Blur with 3x3 kernel
A matrix of n x n is taken (n is always odd), so that there is a single middle pixel (m). The Gaussian blur takes a kernel of n x n and runs through all whole image, to change the value of the pixel m, as the average of its neighbouring pixel values.
 
Here cv2.GaussianBlur makes use of a 5x5 kernel to average the noise in the image.
-	cv2.GaussianBlur(image, (kernel value), deviation)
Applying Gaussian Blur for noise reduction and smoothening

blur_image = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow("Blurred Image", blur_image)

## III.	Edge Detection
Canny Edge Detection is used for detecting all the edges of an image. The Canny function applies a derivative to a function of f(x, y) where x and y are the pixel values in x and y directions. A high change in pixel values is considered as an edge.
 
Here cv2.Canny with a threshold ratio of 1:3 to detect the required edges of the grayscale image.
-	cv2.Canny( image, lower threshold, higher threshold)
Detecting edges in the image

canny_image = cv2.Canny(blur_image, 50, 150)
cv2.imshow("Canny Image", canny_image)
 
## IV.	Region of Interest
To use the edge detected output, a particular region is to be extracted. The region of interest will be different with respect to different camera angles.
To find the region of interest, the image is plotted using ‘matplotlib’.
 
The triangle depicts the region of interest. This region is first masked on a black image as shown below. This is done to trace only the required region on the edge detected image.
Creating the region of interest with reference to plotted image
polygons = np.array([[(150, height), (920, height), (500, 300)]])
Creating a black image

mask = np.zeros_like(image)
cv2.fillPoly(mask, polygons, 255)

A ‘bitwise_and’ operation is applied on the edge detected image and the masked region image. This leads to an image with edges only of the region of interest.
(A black masked image has value 0 in the unrequired region. A bitwise AND operation always gives 0 if one input is 0, therefore eliminating the edges of the unrequired region)
masked_img = cv2.bitwise_and(image, mask)
cv2.imshow("Masked Image", masked_img)

 
## V.	Detecting Straight Lines
Hough transform plays a major role in detecting the straight lines of the lanes. The basic goal is to detect whether a cluster of pixels (of the edges) are part of a line or not.
Working of Hough Transform is explained below:-
After extracting the required edges, you want to know its slope, its intercept, etc. But right now the "edge" is just a sequence of pixels.
If somehow one can loop through all pixels, and figure out the slope and intercept. But that is one difficult task. Images are never perfect. So you want some mechanism that give more weightage to pixels that are already in a line. This is exactly what the Hough Transform does.

•	From lines to points
A lines is a collection of points. And managing a collection of points is tougher than managing a single point. Obviously. So the first thing we learn is how to represent a line as a single point, without losing any information about it. This is done through the m-c space also called the Hough Space.
![alt txt](https://aishack.in/static/img/tut/hough_mc_space.jpg)
As shown in the above picture, every line has two quantities associated with it, the slope and the intercept. With these two numbers, you can describe a line completely.
•	From points to lines
We know that infinite lines pass through a point. So, for every line passing through (xa, ya), there would be a point in the mc space.
So, a point in the xy space is equivalent to a line in the mc space.
 ![alt txt](https://aishack.in/static/img/tut/hough_mc_space_point1.jpg)
The Hough transform is all about doing what we just learned: converting points in the xy space to lines in the mc space.
You take an edge detected image, and for every point that is non-black, you draw lines in the mc place. Obviously, some lines will intersect. These intersections mark are the parameters of the line.
The following picture will clarify the idea:
 ![alt txt](https://aishack.in/static/img/tut/hough_lines_example.jpg)
Instead of the slope-intercept form of lines, we use the normal form to resolve the issue that the value of m (slope) tends to infinity for vertical lines.
 
•	Angle and Distance parameters
In this representation, a line is formed using two parameters - an angle θ and a distance p. p is the length of the normal from the origin (0, 0) onto the line. and θ is the angle this normal makes with the x axis. This is represented my sinusoidal waves in the Hough Space.
![alt txt](https://aishack.in/static/img/tut/hough_p0.jpg)
Next, to detect lane lines, loop through every pixel of the edge detected image. If a pixel is zero, it is ignored. It's not an edge, so it can't be a line. So move on to the next pixel. If a pixel is non-zero, you generate its sinusoidal curve (in the Hough space). So for every non-zero pixel, you'll get a sinusoidal curve in the Hough space. And you'll end up with an image similar to the one at the top. 
The Hough Space is then made into a 2D grid as shown above (known as the accumulator). Each bin will have a vote, every point of intersection increases the vote of that bin by 1. The bin with maximum votes is the line that best represents the points for which the Hough space is plotted. This is because a line plotted with these values will pass through maximum pixels of the edge in the image.
Here cv2.HoughLinesP is used where 2nd and 3rd parameter give the bin size. 4th parameter is the minimum intersections in a bin needed to detect a line. 5th parameter is a placeholder, 6th,  indicates that a line should comprise of a minimum of 40 pixels and the last parameter will allow connecting two lines with a gap of less than or equal to 5 pixels.
-	cv2.HoughLinesP( image, distance resolution(pixels), angle resolution(radians), threshold, min. line length, max. line gap )
Applying Hough Transform
lines1 = cv2.HoughLinesP(cropped_img,2,np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)

## VI.	Displaying the detected Lines
The Hough Transform outputs a 2D array which is converted in to 1D array so that cv2.lines() can be used to print the detected lines on a black image.
Here cv2.line helps plot the values of the 1D array.
-	cv2.line( image, coordinates X, coordinates Y, colour RGB, thickness )

if lines is not None:
    for line in lines:
        # Reshaping 2D array lines to 1D
        x1, y1, x2, y2 = line.reshape(4)
        # Printing each coordinate on a black image with blue color and thickness 10
        cv2.line(lines_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

## VII.	Averaging the Lines
As the output shows, there are multiple lines displayed over each image. To print a single line, first, the slope and intercept values are stored in 2 different arrays namely left_fit[] and right_fit[]. This separation is done with respect to its slope values. All negative slope correspond to the left line whereas all positive slopes correspond to the right line (keep in mind an image represents a 2D array so the y axis values “increase” downwards).  
To determine the slope and intercept for a linear function of 1 degree

parameters = np.polyfit((x1, x2), (y1, y2), 1)
slope = parameters[0]
intercept = parameters[1]

Variable parameters will store the slope and y-intercept values at indexes 0 and 1 respectively which is obtained using ‘np.polyfit’. These values are then averages and its coordinates to be printed in the original image is determined from the ‘coordinates’ function.

left_fit_avg = np.average(left_fit, axis=0)
right_fit_avg = np.average(right_fit, axis=0)

def coordinates(image, line_para):
    slope, intercept = line_para
    y1 = image.shape[0]
    # Length of the line
    y2 = int(y1 * (4 / 6))
    # Obtaining values of x1 and x2 from y= mx + c
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

 
## VIII.	Displaying the Final Image
The final image is formed with the lane detected image above is added to the original image using ‘cv2.addWeighted’
Here cv2.addWeighted adds two images with gamma a value to be added to the sum.
-	cv2.addWeighted( image A, weight A, image B, weight B, gamma)
( Here the black image has a different use. When this line is to be imprinted in the original image, the pixel values will be added, therefore having a black image will result in adding 0 to the original image. Resulting in no unwanted alteration in the original image)
combo_image = cv2.addWeighted(org_img, 0.8, line_img, 1, 1)

## IX.	Lane Detection in Videos
Videos are inputted using cv2.VideoCapture(). To read the video, read() function is used. It outputs 2 values. First value is a boolean value and the second value is the frame of the video. While is the video is open, each frame is taken into account and the lane detection algorithm is applied to each frame. 
For lane detection in Videos

vid = cv2.VideoCapture("test2.mp4")
while (vid.isOpened()):
    bool_value, frame = vid.read()
    rest of the steps are same it is followed for a single image...
    
## X.	Conclusion
A general flow or steps of the Lane Detection Algorithm using Hough Transform is shown below.

After completion of this algorithm and successfully obtaining the correct outputs in images and also correct detection of lanes in test videos, I would like to conclude by saying that Hough Transform Lane Detection Algorithm is a straightforward method of correctly detecting straight lines and small turns and curves. It has helped detection of lanes in a sure and fast procedure in current self-driving cars.. For detection of roundabouts and sharp curves in lanes or sharp turns, Spatial Convolutional Neutral Networks or SCNN has given effective outputs.


Reference:
https://www.youtube.com/watch?v=eLTLtUVuuy4
