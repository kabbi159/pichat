from flask import Flask, render_template, request
import requests
import json
import urllib.request
from urllib.parse import unquote

import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import os


app = Flask(__name__)

@app.route('/')
def index():  # 웹페이지의 첫 화면을 불러온다. index.html 올리기
    return render_template('index.html')

@app.route('/oauth')
def oauth():  # 카카오 계정 로그인 후 얻어온 authorize code를 이용하여 API를 사용하기 위한 access token을 가져온다.
    code = str(request.args.get('code'))  # authorize_code
    response_token = getAccessToken("def706d31baa63561863e79df9c20bca", code)  # client_id = REST API code
    return render_template('friend.html', token=response_token, code=code, test='test.html')

@app.route('/receiver', methods = ['POST'])
def preprocess_friend_information():
    # request로 전해진 데이터를 받는다. (현재 받는 데이터는 친구 API의 결과)
    friend_info = request.get_data()

    # 받은 데이터가 binary string 및 URI가 UTF-8로 인코딩이 되어있으므로, decode 및 unquote를 해준다.
    friend_info = friend_info.decode('UTF-8')
    friend_info = unquote(friend_info)
    print(friend_info)

    # &로 구분하여 리스트에 넣는다
    a = friend_info.split('&')  # 맨 뒤에서 3번째 까지 total_count, after_url, result_id
    # 한 친구마다 elements[i][profile_nickname], elements[i][profile_thumbnail_image], elements[i][id] 가 존재함.

    # 친구 숫자 구하는 코드
    total_count = int(a[-3][12:])
    print(total_count)

    # 친구 숫자 만큼 친구 정보를 추출한다. (이름, 이미지 저장, id)
    for i in range(total_count):
        profile_nickname = a[3*i].split('=')[1]
        profile_thumbnail_image = a[3*i + 1].split('=')[1]
        urllib.request.urlretrieve(profile_thumbnail_image, 'known/'+profile_nickname+'.jpg')
        id = a[3*i + 2].split('=')[1]
        print(profile_nickname, profile_thumbnail_image, id)

    # face recognition API 사용을 위하여, 친구 이미지들이 저장되어 있는 디렉토리로부터 사진을 가져온 다음, load & encode 한다.
    friend_img_path_list = os.listdir('known')
    print(friend_img_path_list)
    friend_img_list = []
    for img in friend_img_path_list:
        img_loaded = face_recognition.load_image_file('known/' + img)
        img_encoded = face_recognition.face_encodings(img_loaded)
        # print(len(img_encoded))
        friend_img_list.append(img_encoded)

    return render_template('test.html')

def getAccessToken(client_id, code):  # 세션 코드값 code 를 이용해서 ACCESS TOKEN 을 발급 받음
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + client_id
    payload += "&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads((response.text.encode('utf-8')))
    print(access_token)
    return access_token['access_token']


if __name__ == '__main__' :
    app.run(debug=True)

