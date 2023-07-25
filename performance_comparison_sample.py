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

    parser.add_argument('--use_mil', action='store_true')
    parser.add_argument('--use_goturn', action='store_true')
    parser.add_argument('--use_dasiamrpn', action='store_true')
    parser.add_argument('--use_csrt', action='store_true')
    parser.add_argument('--use_kcf', action='store_true')
    parser.add_argument('--use_boosting', action='store_true')
    parser.add_argument('--use_mosse', action='store_true')
    parser.add_argument('--use_medianflow', action='store_true')
    parser.add_argument('--use_tld', action='store_true')
    parser.add_argument('--use_nano', action='store_true')

    args = parser.parse_args()

    return args


def isint(s):
    p = '[-+]?\d+'
    return True if re.fullmatch(p, s) else False


def initialize_tracker_list(window_name, image, tracker_algorithm_list):
    tracker_list = []

    # Trackerリスト生成
    for tracker_algorithm in tracker_algorithm_list:
        tracker = None
        if tracker_algorithm == 'MIL':
            tracker = cv.TrackerMIL_create()
        if tracker_algorithm == 'GOTURN':
            params = cv.TrackerGOTURN_Params()
            params.modelTxt = "model/GOTURN/goturn.prototxt"
            params.modelBin = "model/GOTURN/goturn.caffemodel"
            tracker = cv.TrackerGOTURN_create(params)
        if tracker_algorithm == 'DaSiamRPN':
            params = cv.TrackerDaSiamRPN_Params()
            params.model = "model/DaSiamRPN/dasiamrpn_model.onnx"
            params.kernel_r1 = "model/DaSiamRPN/dasiamrpn_kernel_r1.onnx"
            params.kernel_cls1 = "model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx"
            tracker = cv.TrackerDaSiamRPN_create(params)
        if tracker_algorithm == 'Nano':
            params = cv.TrackerNano_Params()
            params.backbone = "model/nanotrackv2/nanotrack_backbone_sim.onnx"
            params.neckhead = "model/nanotrackv2/nanotrack_head_sim.onnx"
            # params.backbone = "model/nanotrackv3/nanotrack_backbone_sim.onnx"
            # params.neckhead = "model/nanotrackv3/nanotrack_head_sim.onnx"
            tracker = cv.TrackerNano_create(params)
        if tracker_algorithm == 'CSRT':
            tracker = cv.TrackerCSRT_create()
        if tracker_algorithm == 'KCF':
            tracker = cv.TrackerKCF_create()
        if tracker_algorithm == 'Boosting':
            tracker = cv.legacy_TrackerBoosting.create()
        if tracker_algorithm == 'MOSSE':
            tracker = cv.legacy_TrackerMOSSE.create()
        if tracker_algorithm == 'MedianFlow':
            tracker = cv.legacy_TrackerMedianFlow.create()
        if tracker_algorithm == 'TLD':
            tracker = cv.legacy_TrackerTLD.create()

        if tracker is not None:
            tracker_list.append(tracker)

    # 追跡対象指定
    while True:
        bbox = cv.selectROI(window_name, image)

        try:
            for tracker in tracker_list:
                tracker.init(image, bbox)
        except Exception as e:
            print(e)
            continue

        return tracker_list


def main():
    color_list = [
        [255, 0, 0],  # blue
        [255, 255, 0],  # aqua
        [0, 255, 0],  # lime
        [128, 0, 128],  # purple
        [0, 0, 255],  # red
        [255, 0, 255],  # fuchsia
        [0, 128, 0],  # green
        [128, 128, 0],  # teal
        [0, 0, 128],  # maroon
        [0, 128, 128],  # olive
        [0, 255, 255],  # yellow
    ]

    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_mil = args.use_mil
    use_goturn = args.use_goturn
    use_dasiamrpn = args.use_dasiamrpn
    use_csrt = args.use_csrt
    use_kcf = args.use_kcf
    use_boosting = args.use_boosting
    use_mosse = args.use_mosse
    use_medianflow = args.use_medianflow
    use_tld = args.use_tld
    use_nano = args.use_nano

    # 使用アルゴリズム #########################################################
    tracker_algorithm_list = []
    if use_mil:
        tracker_algorithm_list.append('MIL')
    if use_goturn:
        tracker_algorithm_list.append('GOTURN')
    if use_dasiamrpn:
        tracker_algorithm_list.append('DaSiamRPN')
    if use_csrt:
        tracker_algorithm_list.append('CSRT')
    if use_kcf:
        tracker_algorithm_list.append('KCF')
    if use_boosting:
        tracker_algorithm_list.append('Boosting')
    if use_mosse:
        tracker_algorithm_list.append('MOSSE')
    if use_medianflow:
        tracker_algorithm_list.append('MedianFlow')
    if use_tld:
        tracker_algorithm_list.append('TLD')
    if use_nano:
        tracker_algorithm_list.append('Nano')
        
    if len(tracker_algorithm_list) == 0:
        tracker_algorithm_list.append('DaSiamRPN')
    print(tracker_algorithm_list)

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
    tracker_list = initialize_tracker_list(window_name, image,
                                           tracker_algorithm_list)

    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        debug_image = copy.deepcopy(image)

        elapsed_time_list = []
        for index, tracker in enumerate(tracker_list):
            # 追跡アップデート
            start_time = time.time()
            ok, bbox = tracker.update(image)
            try:
                tracker_score = tracker.getTrackingScore()
            except:
                tracker_score = '-'
            
            elapsed_time_list.append(time.time() - start_time)
            if ok:
                # 追跡後のバウンディングボックス描画
                new_bbox = []
                new_bbox.append(int(bbox[0]))
                new_bbox.append(int(bbox[1]))
                new_bbox.append(int(bbox[2]))
                new_bbox.append(int(bbox[3]))
                cv.rectangle(debug_image,
                             new_bbox,
                             color_list[index],
                             thickness=2)

        # 各アルゴリズム処理時間描画
        for index, tracker_algorithm in enumerate(tracker_algorithm_list):
            if tracker_score != '-':
                cv.putText(
                    debug_image, tracker_algorithm + " : " +
                    '{:.1f}'.format(elapsed_time_list[index] * 1000) + "ms" + ' Score:{:.2f}'.format(tracker_score),
                    (10, int(25 * (index + 1))), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                    color_list[index], 2, cv.LINE_AA)
            else:
                cv.putText(
                    debug_image, tracker_algorithm + " : " +
                    '{:.1f}'.format(elapsed_time_list[index] * 1000) + "ms",
                    (10, int(25 * (index + 1))), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                    color_list[index], 2, cv.LINE_AA)

        cv.imshow(window_name, debug_image)

        k = cv.waitKey(1)
        if k == 32:  # SPACE
            # 追跡対象再指定
            tracker_list = initialize_tracker_list(window_name, image,
                                                   tracker_algorithm_list)
        if k == 27:  # ESC
            break


if __name__ == '__main__':
    main()