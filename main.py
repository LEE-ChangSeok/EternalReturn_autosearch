import time, datetime, os, sys
import pygetwindow
import dxcam
import argparse
from PIL import Image, ImageFilter
from textdetect import scan_text
from web import multisearch

current_DIR = os.path.dirname(os.path.abspath(__file__))
exe_DIR = os.path.dirname(sys.executable)

if __debug__:
    print("debug :",__debug__)
    print("current file path",current_DIR)
    print("exe file path",exe_DIR)
    os.makedirs(os.path.join(current_DIR,"lumia_log"), exist_ok=True)

if "Local/Temp" in current_DIR:
    current_DIR = exe_DIR

def main():
    parser = argparse.ArgumentParser(description='lumia auto multisearch with screen capture, intended to use in FHD env')
    parser.add_argument('--monitor', type=int, default=0, help='int of monitor to capture')
    parser.add_argument('--myself', action="store_false", help='declare if you want your search result')
    args = parser.parse_args()

    #init
    corners = [[1081,915,1216,949], [1364,915,1499,949], [1648,915,1783,949]]
    bar_loc = [1906,3,1907,12]
    log_output("Waiting for Eternal Return Client to start")
    while "Eternal Return" not in pygetwindow.getAllTitles():
        if __debug__:
            break
        time.sleep(5)
    camera = dxcam.create(device_idx=args.monitor)
    while "Eternal Return" in pygetwindow.getAllTitles() or __debug__:
        #waiting for game to start
        log_output("waiting for matchmaking")
        while "Eternal Return" in pygetwindow.getAllTitles() or __debug__:
            time.sleep(2)
            screenshot = camera.grab()
            if screenshot is None:
                continue
            image = Image.fromarray(screenshot)
            bar_screenshot = image.crop(bar_loc).convert('L')
            bar_avg = list(bar_screenshot.getdata())
            if bar_avg[0] < 1 and bar_avg[-1] > 30:
                log_output("game found")
                break
        image = Image.fromarray(screenshot)
        namelist = []
        for i in range(3):
            cropped = image.crop(corners[i])
            cropped = upsampling(cropped,2)
            #cropped = cropped.filter(ImageFilter.GaussianBlur(radius = 1.3))
            #cropped = filtering(cropped)
            if __debug__:
                cropped.save(os.path.join(current_DIR,f'lumia_log/screen{i}.png'),"PNG")
            namelist.append(scan_text(cropped).strip())
        if __debug__:
            image.save(os.path.join(current_DIR,f'lumia_log/screenshot.png'),"PNG")
            with open(os.path.join(current_DIR,"lumia_log/log.txt"),mode="a") as f:
                f.write("  and  ".join(namelist) + "\n")
        if args.myself == False:
            namelist = namelist[1:]
        multisearch(namelist)

        log_output("waiting 35sec until game end")
        for t in range(35):
            if "Eternal Return" not in pygetwindow.getAllTitles():
                sys.exit("Eternal Return closed")
            else:
                time.sleep(1)

    sys.exit("Eternal Return closed")

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