"""
pip install flask
https://flask.palletsprojects.com/en/2.1.x/
[주의]
- 디버깅할 때 설정
- 경로 설정 주의
"""

from tkinter import N
from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


@app.route("/image")
def image():
    return send_from_directory("static", "loseyourself.jpg")


@app.route("/test")
def test():
    return render_template("/test.html")


@app.route("/image_upload")
def image_upload():
    return render_template("/image_upload.html")


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    TEMP_PATH = "D:/FlaskExamples/example/flask_server/static/temp"

    if not os.path.isdir(TEMP_PATH):
        os.mkdir(TEMP_PATH)

    print(request.headers)
    if request.method == "POST":

        # 클라이언트로부터 받은 이미지 파일 저장
        f = request.files["image_file"]
        imge_filename = os.path.join(TEMP_PATH, f.filename)
        f.save(imge_filename)  # 절대 경로 사용

        return f"{f.filename}가 성공적으로 업로드 되었습니다."


if __name__ == "__main__":
    app.run(debug=True)
