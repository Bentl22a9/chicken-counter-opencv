'''

A cctv streaming tool.
You can choose to play either a live video or a local video file.

To play a live video:
python3 cctv_streamer.py -ch 3 -m l

To play a local video file:
You are supposed to save your file name as 'channel_CHANNEL NUMBER' inside
'records/' directory in advance.
python3 cctv_streamer.py -ch 1 -m r

Press 'q' to turn off a video.

'''

import cv2
import argparse

RTSP_URL = '' # The rtsp url of your cctv.
FIRST_PORT_NUM = 0 # The first port number that refers to your first channel.
W, H = 0, 0 # The width and height of a video that you would like to monitor.
INPUT_PATH = 'records/' # The input path where your local videos located in.

def cctv_streamer(channel, mode):

    port_num = FIRST_PORT_NUM + (channel - 1)
    if mode == 'l':
        cap = cv2.VideoCapture(RTSP_URL + ':{}'.format(port_num))
    elif mode == 'r':
        cap = cv2.VideoCapture(INPUT_PATH + 'channel_{}.mp4'.format(channel))

    while(True):
        r_flag, frame = cap.read()
        frame = cv2.resize(frame, (W,H))
        cv2.imshow('CHANNEL_{}'.format(channel), frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # create a parser object
    parser = argparse.ArgumentParser("A cctv streaming tool")
    # add arguments
    parser.add_argument('-ch', nargs=1, type=int, \
        required=True, help='channel number', choices={1,2,3,4,5,6,7})
    parser.add_argument('-m', nargs=1, type=str, \
        required=True, help='l: live streaming, r: recorded video streaming', \
        choices={'l', 'r'})
    # parse the arguments from standard input
    args = parser.parse_args()

    cctv_streamer(args.ch[0], args.m[0])
