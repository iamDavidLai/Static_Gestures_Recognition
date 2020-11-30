# -*- coding: utf-8 -*-
"""
@author: David Lai
"""
import json
from keras.models import load_model, model_from_json
from cv2 import cv2


# model = load_model("D:\my_gesture_7_model.h5")          # MODEL

with open("D:\my_gesture_7_structure.json", "r") as j:    # Structure of JSON & Weights
    model_json = json.load(j)
model = model_from_json(model_json)
model.load_weights("D:\my_gesture_7_model_weights.h5")

model.summary()

print("Helloooo")







"""
Videocapture predict
"""    
pixel = 256
img_width = pixel
img_height = pixel

left, top, right, bottom = 350, 0, 256+350, 256

label = {0:"None", 1:"Fist", 2:"I love you", 3:"Five", 4:"Okay", 5:"Peace", 6:"Straight", 7:"Thumbs"} 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# print("width: ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # 640
# print("height: ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # 480
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)


while True:
    frame = cap.read()[1]
    frame = cv2.flip(frame, 1)
    # cv2.imshow("Original", frame)    
    
    display = frame[0:320, 0:640]
    
    cv2.rectangle(frame, (left, top), (right, bottom), (0,195,250), 2)     # (x1:0, y1:0),   (x2:256, y2:256)
    roi = frame[top:bottom, left:right]     # crop_img = img[y:y+h, x:x+w]
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)        
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    binary = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)[1]
    
    
    """
    get pics and prediction
    """
    temp = cv2.resize(binary.copy(), (img_width,img_height))
    # prediction = model.predict(temp.reshape(1,256,256,1)/255)     # [[0. 0. 0. 0. 0. 0. 0. 1.]]  8 組 One hot 編碼
    prediction = model.predict_classes(temp.reshape(1, img_width, img_height, 1)/255)     # [0]~[9]
    
    # print(prediction)         # [2]
    # print(prediction.dtype)   # int64
    # print(prediction.shape)   # (1,)
    # print(prediction.ndim)    # 1 階張量
    # print(prediction[0])      # 2 
    

    index = prediction[0]
    print(label[index])
    
    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
    cv2.putText(display, label[index], (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 1, cv2.LINE_AA)
    
    
    cv2.imshow("Display", display)
    cv2.imshow("ROI", roi)
    cv2.imshow("Binary", binary)
    
    key = cv2.waitKey(5)
    if key == 27:   # ESC
        break
    
    
cap.release()    
cv2.destroyAllWindows()
    