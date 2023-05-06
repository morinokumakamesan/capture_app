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

api = Flask(__name__, static_url_path='/static')

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

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)
# line_bot_api_2 = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN_2)
# handler_2 = WebhookHandler(config.LINE_CHANNEL_SECRET_2)

# アプリにPOSTがあったときの処理
@api.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    api.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    # for handler in [handler_1, handler_2]:
    #     try:
    #         handler.handle(body, signature)
    #     except InvalidSignatureError:
    #         abort(400)
    #     else:
    #         pass
    return "OK"

# botにメッセージを送ったときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('文字を受信')
    image_message = ImageSendMessage(
        original_content_url = 'https://capture-app.onrender.com/static/images/r39rquo416g.jpg',
        preview_image_url = 'https://capture-app.onrender.com/static/images/r39rquo416g.jpg'
    )
    text_message = TextSendMessage(text=str(event.source.user_id))
    line_bot_api.reply_message(
        event.reply_token, [image_message, text_message]
    )