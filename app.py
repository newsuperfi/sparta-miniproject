from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.51mtyai.mongodb.net/?retryWrites=true&w=majority')
db = client.miniproject

# 최초 접속 시 팀 소개 페이지 파일 제공
@app.route('/')  
def home():
   return render_template('index.html')  


# 팀소개 페이지 -> 팀원 소개 버튼 -> GET /team 요청 -> 팀원 소개 페이지 파일 제공
@app.route('/team') 
def team():
   return render_template('team.html') 


# 팀원 소개 페이지 -> 팀원 등록 버튼 -> GET /post_member 요청 
# -> postmember.html 파일 제공(팀원 등록 페이지 파일)
@app.route('/post_member')  
def post_member():
   return render_template('postmember.html')


# 팀원소개 페이지 show_member() 함수 실행 -> GET /members 요청 
# -> DB 내의 member 테이블 내의 정보를 모두 json 형태로 클라이언트로 전송
@app.route("/members", methods=["GET"])  
def menu_get():
    all_member = list(db.member.find({},{'_id':False}))

    return jsonify({'result': all_member})



# 팀원 등록 페이지 save_member() 함수 실행 -> POST /members 요청 -> json형태로 폼 데이터 전송받음 
# -> db내의 member 테이블에 저장 -> 클라이언트로 json형태로 메시지 전송
@app.route("/members", methods=["POST"])
def membertable_post():
    member_receive = request.form['member_give']
    mbti_receive = request.form['mbti_give']
    motive_receive = request.form['motive_give']
    blog_receive = request.form['blog_give']
    github_receive = request.form['github_give']
    memberId_receive = request.form['memberId_give']
 
    doc = {
      'member': member_receive,
      'mbti':mbti_receive,
      'motive' : motive_receive,
      'blog': blog_receive,
      'github': github_receive,
      'memberId': memberId_receive
      }
    db.member.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/members/<memberId>", methods=["PUT"])
def membertable_edit(memberId):
    member_receive = request.form['member_give']
    mbti_receive = request.form['mbti_give']
    motive_receive = request.form['motive_give']
    blog_receive = request.form['blog_give']
    github_receive = request.form['github_give'] 

    db.member.update_one({'memberId':memberId},
    {'$set':{
        'member': member_receive,
        'mbti':mbti_receive,
        'motive' : motive_receive,
        'blog': blog_receive,
        'github': github_receive
        }})

    return jsonify({'msg': '수정 완료!'})


# 팀원 소개 페이지 삭제 버튼 클릭 -> DELETE /members/memberId 요청 (memberId부분은 팀원에 따라 변동되므로 동적URL ex) 원희: /members/wonhee 승준: /members/seungjun)
# -> member 테이블 내에서 'memberId' 필드가 전송받은 memberId인 데이터를 한개 찾아서 삭제
# 플라스크에서는 동적URL을 처리할 때 받아온 파라미터 부분을 꺽새로 감싸주고( <memberId> ), 함수 내부에서는 일반 변수형태로 사용
@app.route("/members/<memberId>", methods=["DELETE"])
def membertable_delete(memberId):
    
    db.member.delete_one({'memberId': memberId})
    return jsonify({'msg':'삭제 완료!'})


# 팀원 소개 페이지 방명록 등록 버튼 클릭 -> POST /guestbook/memberId 요청 
# -> 전송받은 폼데이터를 guestbook 테이블에 저장 
# -> json형태의 저장완료 메시지를 클라이언트로 전송
@app.route("/members/<memberId>/guestbook", methods=["POST"])
def guestbook_post(memberId):
    nick_receive = request.form['nick_give']
    comment_receive = request.form['comment_give']
    memberId_receive = memberId

    doc = {
      'nick':nick_receive,
      'comment':comment_receive,
      'memberId': memberId_receive
      }
    db.guestbook.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


    db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# 팀원 소개 페이지 로드 시 show_comment() 함수 자동 실행 -> GET /guestbook/memberId 요청 
# -> guestbook 테이블 내에 있는 데이터 중 동적URL로 전송받은 memberId에 해당되는 데이터를 찾아 json 형태로 클라이언트로 전송
@app.route("/members/<memberId>/guestbook", methods=["GET"])
def guestbook_get(memberId):
    all_comments = list(db.guestbook.find({'memberId': memberId},{'_id':False}))

    return jsonify({'result_guestbook': all_comments})


## 팀원소개 페이지 show_member() 함수 실행 -> GET /members 요청 
# -> DB 내의 member 테이블 내의 정보를 모두 json 형태로 클라이언트로 전송
@app.route("/members/<memberId>", methods=["GET"])
def member_get(memberId):
    member_data = db.member.find_one({'memberId': memberId},{'_id':False})
    return render_template('member.html', result=member_data)
    # return jsonify({'result': member_data})


# 팀원 소개 페이지 내에서 방명록 삭제 버튼 클릭 -> DELETE /guestbook/memberId 요청 
# -> member 테이블 내에서 'memberId' 필드가 전송받은 memberId인 데이터를 한개 찾아서 삭제
@app.route("/members/<memberId>/guestbook", methods=["DELETE"])
def guestbook_delete(memberId):
    db.guestbook.delete_one({'memberId': memberId})
    return jsonify({'msg':'삭제 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
