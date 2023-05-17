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

@app.route("/menu", methods=["GET"])
def menu_get():
    all_member = list(db.memberTable.find({},{'_id':False}))

    return jsonify({'result_member': all_member})


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

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

# all_members_data = list(db.member.find({},{'_id':False}))
# print(all_members_data)