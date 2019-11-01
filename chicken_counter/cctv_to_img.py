'''

A video capturing tool.

You can choose to capture frames either from live cctvs
or from local video files.

To capture from live streaming:
python3 cctv_to_img.py -ch 3 -m l -n 5
-> You will get 5 consecutive frames for the third screen of your cctv.

To capture from local video files:
python3 cctv_to_img.py -ch 3 -m r -n 10
-> You will get 10 copies of capture where two images have the interval of
   1/10 of the total duration.

To get captures from all local video channels:
python3 cctv_to_img.py -ch 0 -m r -n 15

'''

import cv2
import argparse
import os

RTSP_URL = '' # The rtsp url of your cctv.
FIRST_PORT_NUM = 0 # The first port number that refers to your first channel.
W, H = 0, 0 # The width and height of a image that you would like to save.
INPUT_PATH = 'records/' # The input path where your local videos located in.
OUTPUT_PATH = 'capture/' # The output path where you save your captures.


def cctv_to_img(channel, mode, n):

    port_num = FIRST_PORT_NUM + (channel - 1)
    if mode == 'l':
        cap = cv2.VideoCapture(RTSP_URL + ':{}'.format(port_num))

        # if there is no directory, mkdir and save imgs.
        if not(os.path.exists(OUTPUT_PATH + 'live_cap/channel_{}'.format(channel))):
            os.mkdir(OUTPUT_PATH + 'live_cap/channel_{}'.format(channel))

        count = 0
        while(count < n):
            _, frame = cap.read()
            cv2.imwrite(OUTPUT_PATH + 'live_cap/channel_{}/frame_{}.jpg'.format(channel, count + 1), frame)
            count += 1

        cap.release()

    elif mode == 'r':
        cap = cv2.VideoCapture(INPUT_PATH + 'channel_{}.mp4'.format(channel))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_f_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        f_interval = int(total_f_num/n)

        # if there is no directory, mkdir and save imgs.
        if not(os.path.exists(OUTPUT_PATH + 'record_cap/channel_{}'.format(channel))):
            os.mkdir(OUTPUT_PATH + 'record_cap/channel_{}'.format(channel))

        for idx in range(n):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_interval * idx)
            _, frame = cap.read()
            # capture imgs
            cv2.imwrite(OUTPUT_PATH + 'record_cap/channel_{}/frame_{}.jpg'.format(channel, idx + 1), frame)

        cap.release()


if __name__ == '__main__':
    # create a parser object
    parser = argparse.ArgumentParser("A video capturing tool")
    # add arguments
    parser.add_argument('-ch', nargs=1, type=int, required=True, choices={0,1,2,3,4,5,6,7}, \
        help='channel number(0: capture all videos)')
    parser.add_argument('-m', nargs=1, type=str, choices={'l', 'r'}, required=True, \
        help='l: live streaming capture, r: recorded video capture')
    parser.add_argument('-n', nargs=1, default=[10], type=int, \
        help='the number of captures you want')
    # parse the arguments from standard input
    args = parser.parse_args()

    # if ch 0 is given, capture all channels
    if(args.ch[0] == 0):
        for i in range(1,8):
            cctv_to_img(i,args.m[0], args.n[0])
    else:
        cctv_to_img(args.ch[0], args.m[0], args.n[0])
