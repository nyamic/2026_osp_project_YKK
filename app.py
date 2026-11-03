from flask import Flask, render_template, request

app = Flask(__name__)

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
        return render_template("result.html", data=data,
                               img_path="static/images/{}".format(image_file.filename))

if __name__ == '__main__':
    app.run(debug=True)