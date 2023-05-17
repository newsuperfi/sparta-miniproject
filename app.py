from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.51mtyai.mongodb.net/?retryWrites=true&w=majority')
db = client.miniproject

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/team')
def team():
   return render_template('member.html')

@app.route('/post_member')
def post_member():
   return render_template('postmember.html')

@app.route("/members", methods=["GET"])
def menu_get():
    all_member = list(db.member.find({},{'_id':False}))

    return jsonify({'result': all_member})

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

@app.route("/members/<memberId>", methods=["DELETE"])
def membertable_delete(memberId):
    
    db.member.delete_one({'memberId': memberId})
    return jsonify({'msg':'삭제 완료!'})


@app.route("/guestbook/<memberId>", methods=["POST"])
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

@app.route("/guestbook/<memberId>", methods=["GET"])
def guestbook_get(memberId):
    all_comments = list(db.guestbook.find({'memberId': memberId},{'_id':False}))

    return jsonify({'result_guestbook': all_comments})


@app.route("/members/<memberId>", methods=["GET"])
def member_get(memberId):
    member_data = db.member.find_one({'memberId': memberId},{'_id':False})
    return jsonify({'result': member_data})



@app.route("/guestbook/<memberId>", methods=["DELETE"])
def guestbook_delete(memberId):
    
    db.guestbook.delete({'memberId': memberId})
    return jsonify({'msg':'삭제 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
