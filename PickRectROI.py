import cv2
import numpy as np

#global variables for drawing rectangle and equlization mode
ix, iy = -1, -1
jx, jy = -1, -1
drawing = False
mode = 0
modeMessages = ["RGB Mode", "Y Channel Mode", "Dual Mode"]            
RGBMODE = 0
YMODE = 1
DUALMODE = 2


#Function to equalize each of the RGB channels
def enhanceRGB(img):
    b, g, r = cv2.split(img)        #Split channels
    #Equalize Histograms
    b = cv2.equalizeHist(b)
    g = cv2.equalizeHist(g)
    r = cv2.equalizeHist(r)

    newImg = cv2.merge([b, g, r])   #Merge channels back
    return newImg                   #Return new image

#Function to equalize the yellow channel
def enhanceY(img):
    #convert to YCrCb
    newImg = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    cY, Cr, Cb = cv2.split(newImg)      #Split Channels
    newY = cv2.equalizeHist(cY)         #Equalize yellow channel
    newImg = cv2.merge([newY, Cr, Cb])  #Merge channels back
    #convert back to RGB
    newImg =cv2.cvtColor(newImg, cv2.COLOR_YCrCb2RGB)
    return newImg                       #return new image

#Mouse Callback function draw rectangle
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, jx, jy, drawing, cloneImg
    global rectLayer

    if event == cv2.EVENT_LBUTTONDOWN:
        #set rectangle points
        ix, iy = x, y
        jx, jy = x, y
        drawing = True              #Set drawing to True
        cloneImg = img.copy()       #Clear cloneImg of old selection
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        jx, jy = x, y               #Set rectangle corner
        rectLayer = cloneImg.copy()     #Set the rectLayer to the cloneImg
        cv2.rectangle(rectLayer, (ix, iy), (jx, jy), (0, 0, 255), 1)
        cv2.imshow('image', rectLayer)  #Show rectLayer image
        #print(jx, jy)              #Show cursor position
        
    elif event == cv2.EVENT_LBUTTONUP:
        jx, jy = x, y               #Set cursor
        cv2.rectangle(cloneImg, (ix, iy), (jx, jy), (0, 0, 255), 1)
        drawing = False             #Stop drawing rectangle


# Set image to adjust
imgName = "TestImages/4.portrait.jpg"
img = cv2.imread(imgName)
if img is None:
    print("Failed to read image")
    exit()

#Temporary images
cloneImg = img.copy()       #Image layer for temporary changes
rectLayer = cloneImg.copy() #Image layer for rectangle changes

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

while (1):
    rectLayer = cloneImg.copy()     #Update rectLayer
    if drawing:                     #Draw rectangle if currently drawing
        cv2.rectangle(rectLayer,(ix,iy),(jx,jy),(0,0,255),1)
    cv2.imshow('image',rectLayer)   #Show rectLayer
    k = cv2.waitKey(10) & 0xFF      #Listen for keys
    if k == 27:                     #Exit program on 'Esc' key
        break
    elif k == ord('a'):             #Show rectangle position when 'a' key is pressed
        print(ix, iy, jx, jy)
    elif k == ord('r'):             #Press 'r' key to reset image
        img = cv2.imread(imgName)   
        cloneImg = img.copy()
        rectLayer = cloneImg.copy()
    elif k == ord('c'):             #Choose current rectangle section
        ROI_minRow = max(min(iy, jy), 0)
        ROI_maxRow = min(max(iy, jy), len(img[:,0]))
        ROI_minCol = max(min(ix, jx), 0)
        ROI_maxCol = min(max(ix, jx), len(img[0,:]))
        imgROI = img[ROI_minRow:ROI_maxRow+1, ROI_minCol:ROI_maxCol+1]
    elif k == ord('h'):             #Enhance based on mode
        if mode == RGBMODE:
            enh_roi_img = enhanceRGB(imgROI)
            print("Enhancing RGB channels...")

        elif mode == YMODE:
            enh_roi_img = enhanceY(imgROI)
            print("Enhancing Y channel...")
        elif mode == DUALMODE:
            enh_roi_img = enhanceRGB(imgROI)
            enh_roi_img = enhanceY(enh_roi_img)
            print("Enhancing both RGB and Y channels")
        #put enhanced area back into original image and reset layers to new image
        img[ROI_minRow:ROI_maxRow+1, ROI_minCol:ROI_maxCol+1] = enh_roi_img
        cloneImg = img.copy()
        rectLayer = cloneImg.copy()
    elif k == ord('m'):             #Changes mode
        mode = (mode + 1) % 3
        print(modeMessages[mode])
    elif k == ord('s'):             #Save enhanced photo
        cv2.imwrite("Enhanced.jpg",img)
        print('Image saved as "Enhanced.jpg"')


cv2.destroyAllWindows()

