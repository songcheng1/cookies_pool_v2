# -*- coding: UTF-8 -*-
# @author: ylw
# @file: imgas
# @time: 2023/11/9
# @desc:
# import sys
# import os
import numpy as np
import cv2
from base64 import b64decode
from io import BytesIO
from PIL import Image
from ddddocr import DdddOcr


def base64_to_image(base64_string: str, output_file: str):
    """
    base64 转为png图片
    :param base64_string:
    :param output_file:
    :return:
    """
    header, encoded = base64_string.split(",", 1)
    decoded = b64decode(encoded)
    image_data = BytesIO(decoded)
    image = Image.open(image_data)
    image.save(output_file, "png")


def get_distance(templateJpg: str, blockJpg:str) -> int:
    # 读取灰度图
    block = cv2.imread(blockJpg, 0)
    template = cv2.imread(templateJpg, 0)
    # 保存图像
    cv2.imwrite(templateJpg, template)
    cv2.imwrite(blockJpg, block)

    block = cv2.imread(blockJpg)
    block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
    block = abs(255 - block)
    cv2.imwrite(blockJpg, block)
    block = cv2.imread(blockJpg)
    template = cv2.imread(templateJpg)

    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # # 这里就是下图中的绿色框框
    # cv2.rectangle(template, (y + 20, x + 20), (y + 136 - 25, x + 136 - 25), (7, 249, 151), 2)
    return y


def identify_gap(fg: bytes, bg: bytes):
    """
    多缺口识别
    """
    bg_img = cv2.imdecode(np.asarray(bytearray(bg), dtype=np.uint8), 0)  # 背景图片
    bg_img2 = bg_img.copy()  # 背景图片
    bg_pic2 = cv2.cvtColor(bg_img2, cv2.COLOR_GRAY2RGB)

    tp_img = cv2.imdecode(np.asarray(bytearray(fg), dtype=np.uint8), 0)  # 缺口图片
    # 识别图片边缘
    bg_img[bg_img < 60] = 0
    bg_img[bg_img >= 60] = 255
    bg_edge = cv2.Canny(bg_img, 0, 20)

    tp_edge = cv2.Canny(tp_img, 100, 200)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # 缺口匹配
    s = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(s)  # 寻找最优匹配
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标

    cv2.rectangle(bg_pic2, tl, br, (0, 255, 255), 2)  # 绘制矩形

    # 显示图像
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    # cv2.imwrite("3.png", bg_img2)
    # cv2.imshow('Image', bg_img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    distance = tl[0]
    # 返回缺口的X坐标
    return distance


def get_tracks(dis, distance):
    v = 130
    t = 0.3
    # 保存0.3内的位移
    tracks = []
    current = 0
    mid = distance * 4 / 5
    while current <= dis:
        if current < mid:
            a = 8
        else:
            a = -12
        v0 = v
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        tracks.append(round(s))
        v = v0 + a * t
    return tracks


def show_distance(background_png, slide_png):
    """
    :param background_png:
    :param slide_png:
    :return:
    """
    with open(background_png, 'rb') as f:
        background_bytes = f.read()

    with open(slide_png, 'rb') as f:
        target_bytes = f.read()

    Oorc = DdddOcr(det=False, ocr=False, show_ad=False)
    res = Oorc.slide_match(target_bytes, background_bytes)
    return res['target'][0]


if __name__ == '__main__':
    print(show_distance(
    ))
