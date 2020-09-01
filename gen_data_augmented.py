"""
No.4
このセクションでは画像データを5°づつ回転(-20°から20°)させて1枚の写真を9枚の写真として認識させる。
さらに反転させることで18枚の写真として学習させる。

"""

from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection
from sklearn.model_selection import cross_val_score


classes = ['monkey', 'boar', 'crow']
num_classes = len(classes)
# 計算時間短縮のため50px
image_size = 50
num_testdata = 100

# 画像の読み込み

# 画像データを保存するリスト
X_train = []
X_test = []
Y_train = []
Y_test = []

# クラスを取り出して番号をつける
for index, classlabel in enumerate(classes):
    photos_dir = './animals/' + classlabel
    
    # globを使って.jpgのファイルを取得
    files = glob.glob(photos_dir + '/*.jpg')
    for i, file in enumerate(files):
        # 200枚取り出す
        if i >= 200:
            break
        image = Image.open(file)
        image = image.convert('RGB')
        image = image.resize((image_size, image_size))
        data = np.asarray(image)

        if i < num_testdata:
            X_test.append(data)
            Y_test.append(index)
        else:
            X_train.append(data)
            Y_train.append(index)

            for angle in range(-20, 20, 5):
                # 回転
                img_r = image.rotate(angle)
                data = np.asarray(img_r)
                X_train.append(data)
                Y_train.append(index)

                # 反転
                img_trans = img_r.transpose(Image.FLIP_LEFT_RIGHT)
                data = np.asarray(img_trans)
                X_train.append(data)
                Y_train.append(index)


# TensorFlowが扱いやすいデータ型に揃える
# X = np.array(X)
# Y = np.array(Y)

X_train = np.asarray(X_train)
X_test = np.asarray(X_test)
y_train = np.asarray(Y_train)
y_test = np.asarray(Y_test)


# データを交差検証用に分割していく
# X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)

xy = (X_train, X_test, y_train, y_test)

np.save("./animal_aug.npy", xy)
