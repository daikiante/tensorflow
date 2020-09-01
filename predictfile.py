"""
このセクションではファイルをアップロードして実行するアプリケーション化するコードを書いていく

WAF : Web Application Framework

request : フォームから送信したデータを扱うための関数
redirect : ページを移動する
url_for : アドレスを指定してページを遷移させる

werkzeug : Flaskのモジュール。英語ではツールという意味
secure_filename : 悪意あるファイル名を除去する関数
"""
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import flash


from keras.models import Sequential, load_model
import keras,sys
import numpy as np
from PIL import Image

classes = ['monkey', 'boar', 'crow']
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'

# アップロードできる拡張子を制限させる
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'nicotine'


# ファイルのアップロード可否判定関数
def allowed_file(filename):
    """
    確認すること2点
    1, ファイルがピリオドを持っているかどうか
    2, ファイルがapp.configで定義した拡張子を持っているかどうか
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            model = load_model('./animal_cnn_aug.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)
            
            result = model.predict([X])[0]
            
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return classes[predicted] + str(percentage) + ' %'
            # return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset='UTF-8'>
    <title>ファイルをアップロードして判定しよう！</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう！</h1>
    <form method=POST enctype=multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
