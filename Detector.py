from importlib.resources import path
import re
import cv2
from time import sleep
from PIL import Image 

def main_app(name):

    # 导入xml文件
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    # 人脸识别算法的 LBP 提取局部二进制模式
    # 将提取方法扩展为计算7×7 = 49 个单元的直方图非常简单。
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # 读取传入名字的xml文件 
    recognizer.read(f"data/classifiers/{name}_classifier.xml")

    cap = cv2.VideoCapture(0)
    pred = 0
    while True:
        ret, frame = cap.read()
        # bgr 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测输入图像中不同大小的对象。检测到的对象作为矩形列表返回。 
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            id,confidence = recognizer.predict(roi_gray)
            # 置信区间
            confidence = 100 - int(confidence)
            # 累计每一帧的置信区间都大于70的个数
            pred = 0
            # 大于70才是right chocie
            if confidence > 70:
                pred += 1
                # upper大写
                text = name.upper() 
                font = cv2.FONT_HERSHEY_PLAIN
                # 边框
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

            else:   
                pred -= 1
                text = "unknow faces"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)

        cv2.imshow("image", frame)

        # quit 退出
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
        
                

