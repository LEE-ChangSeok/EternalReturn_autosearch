import time, datetime
import numpy as np
import pygetwindow
import dxcam
import argparse
from PIL import Image, ImageFilter
from textdetect import scan_text
from web import multisearch

def main():
    parser = argparse.ArgumentParser(description='lumia auto multisearch with screen capture, intended to use in FHD env')
    parser.add_argument('--monitor', type=int, default=0, help='int of monitor to capture')
    parser.add_argument('--test', action="store_true", help='test')
    parser.add_argument('--myself', action="store_false", help='declare if you want your search result')
    args = parser.parse_args()

    #init
    corners = [[1081,915,1216,949], [1364,915,1499,949], [1648,915,1783,949]]
    bar_loc = [1061,3,1907,12]
    log_output("Waiting for Eternal Return Client to start")
    while "Eternal Return" not in pygetwindow.getAllTitles() and args.test == False:
        time.sleep(5)
    camera = dxcam.create(device_idx=args.monitor)
    while "Eternal Return" in pygetwindow.getAllTitles() or args.test == True:
        #waiting for game to start
        log_output("waiting for matchmaking")
        while "Eternal Return" in pygetwindow.getAllTitles() or args.test == True:
            time.sleep(2)
            screenshot = camera.grab()
            if screenshot is None:
                continue
            image = Image.fromarray(screenshot)
            bar_screenshot = image.crop(bar_loc).convert('L')
            bar_avg = np.mean(bar_screenshot,axis=1)
            if bar_avg[0] < 1 and bar_avg[-1] > 30:
                log_output("game found")
                break
        image = Image.fromarray(screenshot)
        namelist = []
        for i in range(3):
            cropped = image.crop(corners[i])
            #cropped = upsampling(cropped,2)
            #cropped = cropped.filter(ImageFilter.GaussianBlur(radius = 1.3))
            #cropped = filtering(cropped)
            cropped.save(f'screen{i}.png',"PNG")
            namelist.append(scan_text(cropped).strip())
        with open("log.txt",mode="a") as f:
            f.write("  and  ".join(namelist) + "\n")
        if args.myself == False:
            namelist = namelist[1:]
        multisearch(namelist)
        log_output("waiting 35sec until game end")
        time.sleep(40)

    log_output("Eternal Return Closed")

def log_output(str):
    now = datetime.datetime.now()
    print(now.strftime('%H:%M:%S'),str)

def filtering(image):
    image_gray = image.convert('L')
    image_sharp = image_gray.filter(ImageFilter.SHARPEN)
    threshold = 128  # 임계값 설정 (0-255)
    image_binary = image_sharp.point(lambda p: p > threshold and 255)
    return image_binary

def upsampling(image,n=2):
    original_width, original_height = image.size
    new_width = original_width * n
    new_height = original_height * n
    return image.resize((new_width, new_height))

if __name__ == "__main__":
    main()