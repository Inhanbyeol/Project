from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from config import Admin_Authcode, DB_Client
from datetime import datetime


from pymongo import MongoClient
Client = MongoClient(DB_Client)
DB = Client.UBASE_GCCOMPANY_EXAM

@app.route('/')
def home():
    return render_template('index.html')

### 시험 관리 페이지
@app.route('/exam_list_management')
def exam_list_management():
    return render_template('exam_list_management.html')

### 시험 생성 페이지
@app.route('/exam_list_create')
def exam_list_create():
    return render_template('exam_list_create.html')


### 시험 생성 페이지 - 시험 생성
@app.route("/exam_list_management/exam_create", methods=["POST"])
def exam_list_management_create():
    exam_name = request.form['exam_name']
    admin_name = request.form['admin_name']


    exam_list = list(DB.examlist.find({}, {'_id': False}))
    count = len(exam_list) + 1

    doc = {'no': count,
           'exam_name': exam_name,
           'admin_name' : admin_name,
           'time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           }

    DB.examlist.insert_one(doc)

    return jsonify({'msg': '시험 생성이 완료되었습니다.'})

@app.route("/exam_list_management/save", methods=["POST"])
def exam_list_management_save():

    exam_no = request.form['exam_no']
    exam_data_no = request.form['exam_data_no']
    exam_data_quest = request.form['exam_data_quest']
    exam_data_desc = request.form['exam_data_desc']
    exam_data_1 = request.form['exam_data_1']
    exam_data_2 = request.form['exam_data_2']
    exam_data_3 = request.form['exam_data_3']
    exam_data_4 = request.form['exam_data_4']
    exam_data_5 = request.form['exam_data_5']
    exam_data_answer = request.form['exam_data_answer']


    doc = {'exam_no': int(exam_no),
           'exam_data_no': int(exam_data_no),
           'exam_data_quest' : exam_data_quest,
           'exam_data_desc' : exam_data_desc,
           'exam_data_1': exam_data_1,
           'exam_data_2': exam_data_2,
           'exam_data_3': exam_data_3,
           'exam_data_4': exam_data_4,
           'exam_data_5': exam_data_5,
           'exam_data_answer': exam_data_answer,
           }


    DB.examdata.update_one({'exam_no': int(exam_no),'exam_data_no': int(exam_data_no)},{'$set':doc},upsert=True)

    return jsonify({'msg': '데이터 저장 완료'})

### 시험 제목 리스트 가져오기
@app.route("/exam_list_management/exam_list/", methods=["GET"])
def exam_get():
    exam_list = list(DB.examlist.find({}, {'_id': False}))

    return jsonify({'exam_list': exam_list})


### 시험 문제 리스트 가져오기
@app.route("/exam_list_management/exam_data", methods=["POST"])
def exam_data_get():
    exam_no = request.form['exam_no']

    exam_data = list(DB.examdata.find({'exam_no' : int(exam_no)},{'_id' : False}))

    return jsonify({'exam_datax': exam_data})


### 시험 문제 삭제
@app.route("/exam_list_management/del", methods=["POST"])
def exam_data_del():
    exam_no = request.form['exam_no']
    exam_data_no = request.form['exam_data_no']

    DB.examdata.delete_one({'exam_no': int(exam_no), 'exam_data_no':int(exam_data_no)})

    return jsonify({'msg': '시험 문제가 삭제되었습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)