from flask import Flask, jsonify, render_template, request
from flask import session, redirect, url_for, flash
from database import DBhandler
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/list')
def view_list():
    items = list((DB.get_items() or {}).items())
    items_per_row = 2
    items_per_page = 4
    page = request.args.get("page", 0, type=int)
    total_pages = max(1, (len(items) + items_per_page - 1) // items_per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * items_per_page
    page_items = items[start:start + items_per_page]
    rows = []
    for i in range(0, len(page_items), items_per_row):
        rows.append(page_items[i:i + items_per_row])
    return render_template('list.html', data=rows,
                           page_arg=page, total_pages=total_pages, total=len(items))

@app.route("/view_detail/<name>")
def view_item_detail(name):
    data = DB.get_item_byname(str(name))
    img_path = data.get('img_path') if data else None
    return render_template("detail.html", name=name, data=data, img_path=img_path)

@app.route('/review')
def view_review():
    reviews = list((DB.get_reviews() or {}).items())

    items_per_row = 2
    items_per_page = 4

    page = request.args.get("page", 1, type=int)

    total_pages = max(1, (len(reviews) + items_per_page - 1) // items_per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * items_per_page
    page_reviews = reviews[start:start + items_per_page]

    rows = []
    for i in range(0, len(page_reviews), items_per_row):
        rows.append(page_reviews[i:i + items_per_row])

    return render_template(
        'review.html',
        data=rows,
        page_arg=page,
        total_pages=total_pages,
        total=len(reviews)
    )

@app.route("/view_review_detail/<review_id>")
def view_review_detail(review_id):
    review = DB.get_review_by_id(review_id)
    return render_template("review_detail.html", review_id=review_id, review=review)

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
    if image_file and image_file.filename:
        if not allowed_file(image_file.filename):
            return """
    <script>
        alert("지원하지 않는 이미지 형식입니다.\\nPNG, JPG, JPEG, GIF, WEBP 파일만 업로드할 수 있습니다.");
        history.back();
    </script>
    """
        image_file.save("static/images/{}".format(image_file.filename))
        data=request.form
        DB.insert_item(data["product_name"], data, image_file.filename)
        return render_template("result.html", data=data,
                               img_path="static/images/{}".format(image_file.filename))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_confirm", methods=['POST'])
def login_user():
    id_ = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id'] = id_
        return redirect(url_for('hello'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

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

@app.route("/item_like/<name>", methods=["GET", "POST"])
def item_like(name):
    user_id = session.get("id")
    if user_id is None:
        return jsonify({"error": "Login required"}), 401
    if request.method == "GET":
        return jsonify({"liked": DB.get_heart(user_id, name)})  
    data = request.get_json()
    saved = DB.set_heart(user_id, name, data["liked"])
    return jsonify({"liked": saved})
@app.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("reg_reviews.html", name=name)

@app.route("/reg_reviews", methods=["POST"])
def reg_reviews():
    data = request.form
    image_file = request.files.get("photo")

    img_name = ""
    if image_file and image_file.filename:
        image_file.save("static/images/{}".format(image_file.filename)) 
        img_name = image_file.filename

    DB.insert_review(data, img_name) 
    return redirect(url_for("hello"))  


if __name__ == '__main__':
    app.run(debug=True)