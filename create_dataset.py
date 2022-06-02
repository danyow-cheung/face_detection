import cv2
import os
'''
功能：
    摄像头捕获数据集'''
def start_capture(name):
    # 存储路径
    path = "./data/" + name
    # 图像数目
    num_of_images = 0
    # 导入检测文件
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    try:
        # 新建文件夹
        os.makedirs(path)
    except:
        print('Directory Already Created 文件夹已经存在')
    # 调用摄像头
    vid = cv2.VideoCapture(0)
    while True:
        # 读取帧数
        ret, img = vid.read()

        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        '''
        检测输入图像中不同大小的对象。检测到的对象作为矩形列表返回。 
        参数：
            image:包含检测到对象的图像的类型矩阵 
            scaleFactor: 指定每个图像比例缩小图像大小的参数。
            minNeighbors:定每个候选矩形应保留多少个邻居的参数。
        '''
        
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y+h, x:x+w]
        
        cv2.imshow("FaceDetection", img)
        key = cv2.waitKey(1) & 0xFF


        try :
            # 写入文件
            cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), new_img)
            num_of_images += 1
        except :
            pass
        # 退出或者设置最大摄取帧数
        if key == ord("q") or key == 27 or num_of_images > 201:
            break
    cv2.destroyAllWindows()
    return num_of_images

