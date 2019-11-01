'''

You can get the number and coordinates of chickens in a captured image.

To counter number of chickens for frame 3 of channel 4:
python3 chicken_counter.py 3 4

Since chicken_counter.py applies 'Canny Edge Detecting' algorithm to detect
chickens, it might detect non-chicken objects as well. To handle this, you
can drop a few dected boxes from the beginning through
'append_sliced_dict_to_array' method, or from the end through 'drop_last_n'
method.

'''

import cv2
import sys
import numpy as np

IMG_PATH = '' # 'captures/record_cap/' or 'captures/live_cap'
W, H = 0, 0 # The width and height of a image that you would like to monitor.

# Calculate the area of rectangular box binding a contour.
def rectArea(cnt) :
    _, _, w, h = cv2.boundingRect(cnt)
    return w * h

# Append values of dictionary into an array, from index 1 to (index2 -1)
def append_sliced_dict_to_array(dict, idx1, idx2):
    if (idx1 > idx2):
        temp = idx1, idx1 = idx2, idx2 = temp

    splited = []
    for i in range(idx1, idx2):
        splited += dict.get(i)
    return np.asarray(splited)

# Drop last n elements from a given array.
def drop_last_n(cnts, n):
    return cnts[: len(cnts) - n]

# Make a dictionary of arrays, where keys are indices of intervals, and
# values are arrays of contours belong to each interval.
def get_linspace_dict(cnts, l):
    dict = {}
    for n in range(len(l) -1):
        dict[n] = [cnt for cnt in cnts if l[n] <= rectArea(cnt) <= l[n+1]]
    return dict

# Read image from a given path and return the image on which 'Canny Edge Detection'
# algorithm is applied.
def get_canny(img_path, w, h):
    # read img.
    orig_img = cv2.imread(IMG_PATH)
    # adjust the size of an image.
    orig_img = cv2.resize(orig_img , (W, H))
    # convert RGB to grayscale.
    gray_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    # median blurring.
    m_blur = cv2.medianBlur(gray_img, 5)
    # apply canny edge detecting algorithm.
    canny = cv2.Canny(m_blur, 50, 255)
    return canny

# Draw rectangular boxes around detected contours and markers at the centre of
# boxes.
def draw_marks_and_boxes(img_path, w, h, cnts):
    orig_img = cv2.imread(img_path)
    orig_img = cv2.resize(orig_img, (w,h))
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        coord = int(x+w/2), int(y+h/2)
        cv2.drawMarker(orig_img, coord , (127,255,127), markerType=cv2.MARKER_TILTED_CROSS, markerSize=5)
        cv2.rectangle(orig_img, (x, y+h), (x+w, y), (0,255,0), 1)
    return orig_img

# Get an array of coordinates from boxes bounding each given contour.
def get_coords(cnts):
    coords=[]
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        coord = int(x+w/2), int(y+h/2)
        coords.append(coord)
    return coords

# Count the number of chickens in a given image.
def chicken_counter(img_path, w, h):

    canny = get_canny(img_path, w, h)

    # find contours
    cnts, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours according to its area of box surrounding it.
    sorted_cnts = sorted(cnts, key=lambda x: rectArea(x))

    # get linspace where the minimum is the area of the smallest rectangular box, and
    # the maximum is that of the largest.
    l = np.linspace(rectArea(sorted_cnts[0]), rectArea(sorted_cnts[-1]), len(sorted_cnts))

    cnts_to_dict = get_linspace_dict(sorted_cnts, l)

    splited_cnts = append_sliced_dict_to_array(cnts_to_dict, 4 , len(cnts_dict) - 1)
    dropped_cnts = drop_last_n(splited_cnts, 20)

    # draw boxes around spotted chickens.
    result_img = draw_marks_and_boxes(img_path, w, h, dropped_cnts)

    # render image
    cv2.imshow('Result', result_img)
    cv2.imshow('Canny', canny)
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()

    coords = get_coords(dropped_cnts)
    n = len(dropped_cnts)
    return coords, n

if __name__ == '__main__':
    ch = sys.argv[1]
    f = sys.argv[2]
    IMG_PATH += 'channel_{}/frame_{}.jpg'.format(ch, f)
    coords, n = chicken_counter(IMG_PATH, W, H)
