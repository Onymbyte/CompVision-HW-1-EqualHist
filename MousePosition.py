import cv2
import numpy as np

ix, iy = -1, -1
# mouse callback function
# For more mouse event types, check https://docs.opencv.org/3.1.0/d7/dfc/group__highgui.html#ga927593befdddc7e7013602bca9b079b0
# For more drawing functions, check https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html


def draw_circle(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(param, (x, y), 10, (255, 0, 0), -1)
        ix, iy = x, y

    if event == cv2.EVENT_LBUTTONUP:
        # try to drag the mouse before you release the left button
        cv2.circle(param, (x, y), 10, (0, 0, 255), -1)
        ix, iy = x, y


# Create a black image, a window and bind the function to window.  
img = np.zeros((512,512,3), np.uint8)

# It is a good idea to first clone this image, 
# so that your drawing will not contaminate the original image
cloneImg = img.copy()

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle, cloneImg)

while (1):
    cv2.imshow('image',cloneImg)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(ix, iy)

cv2.destroyAllWindows()

