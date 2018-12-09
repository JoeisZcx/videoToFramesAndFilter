#!/usr/bin/env python  
# _*_ coding:utf-8 _*_

import os
import sys
import cv2
from PIL import Image
import traceback

videosSrcDir = "D:/3DWork/vbr3dTestLog/20181207/5"
videoFormats = [".MP4", ".mp4", ".MOV", ".mov", ".WMA", ".wma", ".AVI", ".avi"]
framesSaveDir = "D:/3DWork/vbr3dTestLog/20181207/5"
timeInterval = 10

def video2frame(videosSrcDir, framesSaveDir, formats , interval):
    """
    :param videosSrcDir: 视频存放位置
    :param formats:包含视频格式
    :param framesSaveDir:帧图片保存位置
    :param interval:抽帧间隔
    :return:帧图片
    """
    videos = os.listdir(videosSrcDir)

    # 筛选符合要求的视频
    def filterFormat(x, allFormat):
        if x[-4:] in allFormat:
            return True
        else:
            return False

    videos = filter(lambda x: filterFormat(x, formats), videos)
    frames = []
    # if not framesSaveDir.endswith("/"):
    #     framesSaveDir = framesSaveDir + "/"
    # timestamp = str(int(round(time.time()) * 1000))
    # path = framesSaveDir + timestamp
    # os.makedirs(path)
    for video in videos:
        videoName = video[:-4]
        # framesSavePath = os.path.join(framesSaveDir, timestamp)
        # framesSavePath = framesSaveDir

        ### 为了放在不同文件夹+ ###
        if not framesSaveDir.endswith("/"):
            framesSaveDir = framesSaveDir + "/"
        path = framesSaveDir + videoName
        os.makedirs(path)
        framesSavePath = os.path.join(framesSaveDir, videoName)
        ###                     ###

        videosSrcPath = os.path.join(videosSrcDir, video)
        cap = cv2.VideoCapture(videosSrcPath)
        frameIndex = 0
        frameCount = 0
        if cap.isOpened():
            success = True
        else:
            success = False
            print("####视频读取错误####")
        while(success):
            success, frame = cap.read()
            print("---->正在读取第%d帧 %s" % (frameIndex, success))
            if success and frameIndex % interval == 0:
                frames.append(format("%s-%06d.jpg" % (videoName, frameCount)))
                # cv2.imwrite(framesSaveDir+ "/%s-%06d.jpg" % (videoName, frameCount), frame)
                cv2.imwrite(framesSavePath + "/%s-%06d.jpg" % (videoName, frameCount), frame)
                frameCount += 1

            frameIndex += 1
        ###
        filterFrame(path)
        ###
        cap.release()
        # os.remove(videosSrcPath)
    return path

def filterFrame(framesSaveDir, frames=""):
    """
    :param path: 视频帧所在文件夹
    :return:
    """
    frames = os.listdir(framesSaveDir)
    frames.sort()
    num = len(frames)
    if num < 2:
        print("Frames is not enough!")
        sys.exit(1)
    else:
        i = 0
        while i <= num-2:
            framePath1 = os.path.join(framesSaveDir, frames[i])
            framePath2 = os.path.join(framesSaveDir, frames[i+1])
            frame1 = Image.open(framePath1)
            frame2 = Image.open(framePath2)
            frame1 = frame1.resize((256, 256)).convert("RGB")
            g = frame1.histogram()
            frame2 = frame2.resize((256, 256)).convert("RGB")
            s = frame2.histogram()
            assert len(g) == len(s), "Error"
            sim = []
            for index in range(len(g)):
                if g[index] != s[index]:
                    sim.append(round(1-float(abs(g[index]-s[index]))/max(g[index], s[index]), 2))
                else:
                    sim.append(1)
            ave = sum(sim)/len(g)
            print("framePath1:%s,framePath2:%s,相似度:%2f" % (framePath1, framePath2, ave))
            if ave >0.85:
                os.remove(framePath2)
                del frames[i+1]
                num = num - 1
                print("---->移除视频帧:%s" % framePath2)
            else:
                i += 1
    return 0

if __name__ == "__main__":
    try:
        # filterFrame("D:/3DWork/bagVideo/MVI_0003")
        path = video2frame(videosSrcDir, framesSaveDir, videoFormats, timeInterval)
    except Exception, e:
        print("exception:" + traceback.format_exc())
        sys.exit(1)
    sys.exit(0)