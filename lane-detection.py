import cv2
import numpy as np
import matplotlib.pyplot as plt

org_img=cv2.imread("lane_pic.jpg")
lane_img=cv2.imread("lane_pic.jpg",0)
cv2.resize(org_img,(1289,704))
cv2.resize(lane_img,(1289,704))
# cv2.imshow("Grayscale Image", lane_img)

def coordinates(image, line_para):
    slope, intercept=line_para
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))

    left_fit_avg=np.average(left_fit,axis=0)
    right_fit_avg=np.average(right_fit,axis=0)

    left_line=coordinates(image, left_fit_avg)
    right_line=coordinates(image, right_fit_avg)
    return np.array([left_line, right_line])

def canny(image):
    blur_image = cv2.GaussianBlur(image, (5, 5), 0)
    # cv2.imshow("Blurred Image", blur_image)
    canny_image = cv2.Canny(blur_image, 50, 150)
    # cv2.imshow("Canny Image", canny_image)
    return canny_image

def region_of_interest(image):
    height=image.shape[0]
    polygons=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_img=cv2.bitwise_and(image,mask)
    # cv2.imshow("Masked Image", masked_img)
    return masked_img

def display_lines(image,lines):
    line_img=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line
            cv2.line(line_img,(x1,y1),(x2,y2),(255,0,0),10)
        # cv2.imshow("Lane Image", line_img)
    return line_img

# For Static Image
# canny_img = canny(lane_img)
# cropped_img = region_of_interest(canny_img)
# lines = cv2.HoughLinesP(cropped_img,2,np.pi/180, 100, np.array([]),minLineLength=40,maxLineGap=5)
# avg_line = average_slope(org_img,lines)
# line_img = display_lines(org_img, avg_line)
# combo_image = cv2.addWeighted(org_img, 0.8, line_img, 1, 1)
# # cv2.imshow("Lane Detected Image", line_img)
# cv2.imshow("Lane Detected Image", combo_image)
# cv2.waitKey(0)

# plt.imshow(canny_img)
# plt.show()

vid = cv2.VideoCapture("test2.mp4")
while(vid.isOpened()):
    bool_value,frame = vid.read()
    canny_img = canny(frame)
    cropped_img = region_of_interest(canny_img)
    lines = cv2.HoughLinesP(cropped_img, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    avg_line = average_slope(frame, lines)
    line_img = display_lines(frame, avg_line)
    combo_image = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
    # cv2.imshow("Lane Detected Image", line_img)
    cv2.imshow("Lane Detection", combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()

