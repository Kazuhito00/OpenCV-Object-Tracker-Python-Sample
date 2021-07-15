#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import copy
import time
import argparse

import cv2 as cv


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", default="sample_movie/bird.mp4")
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    args = parser.parse_args()

    return args


def isint(s):
    p = '[-+]?\d+'
    return True if re.fullmatch(p, s) else False


def initialize_tracker(window_name, image):
    params = cv.TrackerDaSiamRPN_Params()
    params.model = "model/DaSiamRPN/dasiamrpn_model.onnx"
    params.kernel_r1 = "model/DaSiamRPN/dasiamrpn_kernel_r1.onnx"
    params.kernel_cls1 = "model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx"
    tracker = cv.TrackerDaSiamRPN_create(params)

    # 追跡対象指定
    while True:
        bbox = cv.selectROI(window_name, image)

        try:
            tracker.init(image, bbox)
        except Exception as e:
            print(e)
            continue

        return tracker


def main():
    color_list = [
        [255, 0, 0],  # blue
    ]

    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    # カメラ準備 ###############################################################
    if isint(cap_device):
        cap_device = int(cap_device)
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Tracker初期化 ############################################################
    window_name = 'Tracker Demo'
    cv.namedWindow(window_name)

    ret, image = cap.read()
    if not ret:
        sys.exit("Can't read first frame")
    tracker = initialize_tracker(window_name, image)

    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        debug_image = copy.deepcopy(image)

        # 追跡アップデート
        start_time = time.time()
        ok, bbox = tracker.update(image)
        elapsed_time = time.time() - start_time
        if ok:
            # 追跡後のバウンディングボックス描画
            cv.rectangle(debug_image, bbox, color_list[0], thickness=2)

        # 各アルゴリズム処理時間描画
        cv.putText(
            debug_image,
            'DaSiamRPN' + " : " + '{:.1f}'.format(elapsed_time * 1000) + "ms",
            (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, color_list[0], 2,
            cv.LINE_AA)

        cv.imshow(window_name, debug_image)

        k = cv.waitKey(1)
        if k == 32:  # SPACE
            # 追跡対象再指定
            tracker = initialize_tracker(window_name, image)
        if k == 27:  # ESC
            break


if __name__ == '__main__':
    main()