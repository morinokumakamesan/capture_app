from flask import Flask, request, make_response, render_template, url_for

from . import service

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/capture_img', methods=['POST'])
def capture_img():
    msg = service.save_img(request.form["img"])
    return make_response(msg)