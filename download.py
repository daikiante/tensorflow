"""
No.1
APIから画像を取得する
"""

from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys



# APIキーの情報
key = '8cfae380b4ef3c0278c437ac5c36c58a'
secret = '39316af1039dca6a'
wait_time = 1

# 保存フォルダの指定
animalname = sys.argv[1]
savedir = './animals/' + animalname

# for x in animalname:
#     print(x)


# FlickrAPIが正しければflicr.photosが実行されてresultに代入する
flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = animalname,
    per_page = 400,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, license'
)
photos = result['photos']
# pprint(photos)

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath):
        continue
    else:
        urlretrieve(url_q, filepath)
        time.sleep(wait_time)