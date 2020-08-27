from selenium import webdriver
from bs4 import BeautifulSoup

import time



import requests

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbspart

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/product-info', methods=['POST'])
def url_go():

    url = request.form['url']

    driver = webdriver.Chrome('C:\\Users\\윤재희\\Desktop\\chromedriver_win32\\chromedriver')

    driver.get(url)

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_name = soup.select(".prod-buy-header__title")[0].text

    korea_price = soup.select(".total-price")[0].text.strip('\n')

    product_image_list = soup.select('#repImageContainer > div.prod-image__items > div')
    refined_image_url_list = []
    for image_tag in product_image_list:
        image_url = image_tag.select_one('img')['data-src']
        str_image_url = str(image_url)
        origin_size_string = '48x48ex'
        changed_size_string = '492x492ex'
        refined_image_url_list.append(str_image_url.replace(origin_size_string, changed_size_string))

    option_list = soup.select('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-option > div > div > ul > li')

    product_option_list = []
    for option in option_list:
        option_name = option.select_one('.prod-option__dropdown-item-title > strong').text
        option_price = option.select_one('strong > .price-label').text
        product_option = {
            'name': option_name,
            'price': option_price,
        }

        print('option:', product_option)
        product_option_list.append(product_option)

    detail = soup.select('.productDetail > div.product-detail-content-inside')

    detail_text = detail[0].text if detail else ''

    driver.quit()

    product_db = {
        'product_name': product_name,
        'korea_price': korea_price,
        'product_img': refined_image_url_list,
        'product_option_list': product_option_list,
        'detail': detail_text,
    }

    product_info = {
        'product_name': product_name,
        'korea_price': korea_price,
        'product_img': refined_image_url_list,
        'product_option_list': product_option_list,
        'detail': detail_text,
    }

    db.productDB.insert_one(product_db)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '상품을 성공적으로 가져왔습니다.', 'product_info': product_info})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)