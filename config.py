import sys
sys.argv = ['main.py', 
            '--modeldir', '/home/ws/tflite1/TFLite_model',
            '--threshold', '0.5',
            '--resolution', '1280x720']

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder containing .tflite and labelmap', required=True)
    parser.add_argument('--threshold', help='Minimum confidence threshold', default=0.5)
    parser.add_argument('--resolution', help='Camera resolution WxH', default='1280x720')
    args = parser.parse_args()

    MODEL_NAME = args.modeldir
    GRAPH_NAME = 'detect.tflite'
    LABELMAP_NAME = 'labelmap.txt'
    min_conf_threshold = float(args.threshold)
    res_w, res_h = map(int, args.resolution.split('x'))

    return MODEL_NAME, GRAPH_NAME, LABELMAP_NAME, min_conf_threshold, res_w, res_h
