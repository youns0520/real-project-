from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbspart

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/product-info', methods=['POST'])
def url_go():
    url = request.form['url']
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    product_name = soup.select('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-buy-header > h2')
    print(product_name)
    korea_price = soup.select('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-price-container > div.prod-price > div > div.prod-sale-price.prod-major-price > span.total-price')
    print(korea_price)
    product_img = soup.select('#repImageContainer > div.prod-image__items > div:nth-child(1) > img')
    print(product_img)
    product_option = soup.select('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-option > div > div > ul')
    print(product_option)
    detail_form = soup.select('#productDetail > div.product-detail-content-inside')
    print(detail_form)

    productDB = {
        'product_name': product_name,
        'korea_price': korea_price,
        'product_img': product_img,
        'product_option': product_option,
        'detail_form': detail_form
    }

    db.productDB.insert_one(productDB)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '상품을 성공적으로 가져왔습니다.'})


@app.route('/viewInfo', methods=['GET'])
def writeInfos():
    productDBs = list(db.productDB.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'productDBs': productDBs})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)