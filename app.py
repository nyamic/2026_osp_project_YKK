from flask import Flask, render_template, request
from database import DBhandler

app = Flask(__name__)
DB = DBhandler()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/list')
def view_list():
    return render_template('list.html')

@app.route('/review')
def view_review():
    return render_template('review.html')

@app.route('/register-items')
def register_items():
    return render_template('reg_items.html')

@app.route('/register-reviews')
def register_reviews():
    return render_template('reg_reviews.html')

@app.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    status=request.args.get("status")
    return "Input name:" + name + " input status:" + status

@app.route("/submit_item_post", methods=["POST"])
def reg_item_submit_post():
        image_file=request.files["picture"]
        image_file.save("static/images/{}".format(image_file.filename))
        data=request.form
        return render_template("result.html", data=data,
                               img_path="static/images/{}".format(image_file.filename))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    if DB.insert_user(data,pw):
        return render_template("login.html")
    else:
        return render_template("signup.html", error="User ID already exists!")


if __name__ == '__main__':
    app.run(debug=True)