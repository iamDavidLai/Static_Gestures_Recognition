from cv2 import cv2
from time import sleep
import shutil, os


def makeDir(dirname):
    if os.path.isdir(dirname):      # IF exist, 可以直接新增寫入內容
        # shutil.rmtree(dirname)    # IF exist, delete folder and images (先前作法)
        # sleep(1)  
        print("資料夾已存在, return")
        return
    else:
        os.mkdir(dirname)          # create new folder



"""
Folder &  setting
"""
i = 1                                    # 圖檔編號命名, 若要接續新增要以dataset中最後的檔案編號為起始。 
thre = r"dataset\threshold"              # your images path
dir_threshold = os.path.join(thre, "your_gesture_folder_name")   
makeDir(dir_threshold)         

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

MODE = ""
CAPTURE = "capture"
STOP = "stop"

    

while True:
    ret, frame = cap.read()

    flipImage = cv2.flip(frame, 1)  # 0: 上下,   1:左右
    roi = flipImage[0:256, 354:610] # 256(Y)*256(X)         [y-top:bottom,  x-left:right]    replace dimension what you want

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    # thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]       
    # thresh = cv2.threshold(blur, 125, 255, cv2.THRESH_BINARY)[1]        # 大於門檻值的設為最大灰階, 小於門檻設為 25
    thresh = cv2.threshold(blur, 135, 255, cv2.THRESH_BINARY_INV)[1]    # 門檻值, 超過門檻值之後設為最大灰階值   超過150轉換為0, 否則為255    FOR SINGLE GESTURE

    
    cv2.imshow("ROI-Binary", thresh)
    cv2.imshow("ROI-Webcam", roi)
    # cv2.imshow("blur", blur)
    # cv2.imshow("original", flipImage)

    
    key = cv2.waitKey(5)
    # print("keyboard:", key)
    
    if MODE == CAPTURE:
        # print("Start Capture")
        sleep(0.03)
        path_name = dir_threshold + "\\" + str(i) + ".png"
        cv2.imwrite(path_name, thresh)
        i += 1
        print("File path:" + path_name )
    else:
        # print("Stop Capture")
        pass


    if key == 13:       # ENTER   
       MODE = CAPTURE
    
    if key == 32:       # SPACE     
       MODE = STOP

    if key == 27:       # ESC ms毫秒 , IF 0 無限等待鍵盤事件
        break


cap.release()
cv2.destroyAllWindows()    
