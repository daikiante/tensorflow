"""
No.2
このセクションでは取得した画像データを画像データをTensorFlowが扱いやすいようにnumpyで配列型式に変換していく

scikit-learn
Pythonの機械学習用のライブラリ

クロスバリデーション : 交差検証
データを分離して学習と評価を行う手法

glob : グローブ
パターン一致でファイル一覧を取得する
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


# 画像の読み込み

# 画像データを保存するリスト
X = []
Y = []

# クラスを取り出して番号をつける
for index, classlabel in enumerate(classes):
    photos_dir = './animals/' + classlabel
    
    # globを使って.jpgのファイルを取得
    files = glob.glob(photos_dir + '/*.jpg')
    for i, file in enumerate(files):
        # 200枚取り出す
        if i >= 200:
            break
        else:
            image = Image.open(file)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X.append(data)
            Y.append(index)

# TensorFlowが扱いやすいデータ型に揃える
X = np.array(X)
Y = np.array(Y)


# データを交差検証用に分割していく
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)

xy = (X_train, X_test, y_train, y_test)

np.save("./animal.npy", xy)