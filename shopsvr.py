from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('shop.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_review():
      text_receive = request.form['text_give']
      num_receive = request.form['num_give']
      address_receive = request.form['address_give']
      phone_receive = request.form['phone_give']
      # DB에 삽입할 order 만들기
      order = {
         'text': text_receive,
         'num': num_receive,
         'address': address_receive,
         'phone': phone_receive
      }
      # reviews에 review 저장하기
      db.orders.insert_one(order)
      # 성공 여부 & 성공 메시지 반환
      return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


@app.route('/orders', methods=['GET'])
def read_reviews():
      # 1. DB에서 리뷰 정보 모두 가져오기
      orders = list(db.orders.find({},{'_id':0}))
      # 2. 성공 여부 & 리뷰 목록 반환하기
      return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)