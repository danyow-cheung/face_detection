import numpy as np
from PIL import Image
import os, cv2

'''
人脸识别训练器:局部二进制直方图
'''
# 训练自定义分类器识别人脸的方法
def train_classifer(name):# 读取自定义数据集中的所有图像
        
    path = os.path.join(os.getcwd()+"/data/"+name+"/")
    faces = []
    ids = []
    pictures = {}

    # 以 numpy 格式存储图像，并将用户的 id 存储在 imageNp 和 id 列表中的同一索引上

    for root,dirs,files in os.walk(path):
        pictures = files


    for pic in pictures :

        imgpath = path+pic
        #L模式图像，则意味着它是单通道图像 - 通常解释为灰度
        # L就是存储亮度的方法。它非常紧凑，但只存储灰度，不存储颜色。
        img = Image.open(imgpath).convert('L')
        # 图像转换为np
        imageNp = np.array(img, 'uint8')
        # 得到名字
        id = int(pic.split(name)[0])
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    #x训练保存分类器
    clf = cv2.face.LBPHFaceRecognizer_create()
    # (src,label)
    clf.train(faces, ids)
    clf.write("./data/classifiers/"+name+"_classifier.xml")

