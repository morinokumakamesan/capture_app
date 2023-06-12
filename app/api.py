from flask import Flask, request, make_response, render_template, url_for, abort
import requests, os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, FollowEvent, UnfollowEvent
from PIL import Image
from io import BytesIO
from . import service
from pprint import pprint
import config
from flask_socketio import SocketIO, send, emit
import time
import json

api = Flask(__name__, static_url_path='/static')
socketio = SocketIO(api, cors_allowed_origins='*')

client_sessions = {}

@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/show', methods=['GET'])
def show():
    return render_template('show.html')

@api.route('/capture_img', methods=['POST'])
def capture_img():
    msg = service.save_img(request.form["img"], request.form["deviceId"])
    return make_response(msg)

line_bot_api_1 = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN_1)
handler_1 = WebhookHandler(config.LINE_CHANNEL_SECRET_1)
line_bot_api_2 = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN_2)
handler_2 = WebhookHandler(config.LINE_CHANNEL_SECRET_2)

# アプリにPOSTがあったときの処理
@api.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    api.logger.info("Request body: " + body)
    # handle webhook body
    # try:
    #     # handler_1.handle(body, signature)
    #     handler_2.handle(body, signature)
    # except InvalidSignatureError:
    #     abort(400)
    for handler in [handler_1, handler_2]:
        try:
            handler.handle(body, signature)
            break
        except InvalidSignatureError:
            pass
            # abort(400)
    return "OK"

# botにメッセージを送ったときの処理
@handler_1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    deviceId = '8i2np4sobag'
    print('文字を受信_1')
    socketio.emit('img_event', str(time.time()), room=client_sessions[id_1])
    image_message = ImageSendMessage(
        original_content_url = 'https://capture-app.onrender.com/static/images/' + deviceId + '.jpg',
        preview_image_url = 'https://capture-app.onrender.com/static/images/' + deviceId + '.jpg'
    )
    text_message = TextSendMessage(text=str(event.source.user_id))
    line_bot_api_1.reply_message(
        event.reply_token, [image_message, text_message]
    )

# botにメッセージを送ったときの処理
@handler_2.add(MessageEvent, message=TextMessage)
def handle_message(event):
    deviceId = '2f0i9aa7t08'
    print('文字を受信_2')
    socketio.emit('img_event', str(time.time()), room=client_sessions[deviceId])
    image_message = ImageSendMessage(
        original_content_url = 'https://capture-app.onrender.com/static/images/' + deviceId + '.jpg',
        preview_image_url = 'https://capture-app.onrender.com/static/images/' + deviceId + '.jpg'
    )
    text_message = TextSendMessage(text=str(event.source.user_id))
    line_bot_api_2.reply_message(
        event.reply_token, [image_message, text_message]
    )

@api.route("/hoge")
def hoge():
    return render_template('hoge.html')

@socketio.on("initial_data")
def initial(data):
    print(data)
    print(data['socketId'])
    print(data['deviceId'])
    print('-'*50)
    deviceId = data['deviceId']
    client_sessions[deviceId] = request.sid
    print(client_sessions)