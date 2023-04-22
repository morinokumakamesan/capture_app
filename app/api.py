from flask import Flask, request, make_response, render_template, url_for, abort
import requests, os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, FollowEvent, UnfollowEvent
from PIL import Image
from io import BytesIO
from . import service
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
    msg = service.save_img(request.form["img"])
    return make_response(msg)

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

header = {
    "Content_Type": "application/json",
    "Authorization": "Bearer " + config.LINE_CHANNEL_ACCESS_TOKEN
}

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
    return "OK"


# botにメッセージを送ったときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('文字を受信')
    image_message = ImageSendMessage(
        original_content_url = 'https://capture-app.onrender.com/static/images/capture.jpg',
        preview_image_url = 'https://capture-app.onrender.com/static/images/capture.jpg'
    )
    text_message = TextSendMessage(text=event.source.userId)
    line_bot_api.reply_message(
        event.reply_token, [image_message, text_message]
    )
    print("返信完了!!\ntext:", event.message.text)


# botに画像を送ったときの処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    print("画像を受信")
    message_id = event.message.id
    image_path = getImageLine(message_id)
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url = 'https://capture-app.onrender.com/static/images/capture.jpg',
            preview_image_url = 'https://capture-app.onrender.com/static/images/capture.jpg'
        )
    )
    print("画像の送信完了!!")


# 受信メッセージに添付された画像ファイルを取得
def getImageLine(id):
    line_url = f"https://api-data.line.me/v2/bot/message/{id}/content"
    result = requests.get(line_url, headers=header)
    print(result)

    img = Image.open(BytesIO(result.content))
    w, h = img.size
    if w >= h:
        ratio_main, ratio_preview = w / 1024, w / 240
    else:
        ratio_main, ratio_preview = h / 1024, h / 240

    width_main, width_preview = int(w // ratio_main), int(w // ratio_preview)
    height_main, height_preview = int(h // ratio_main), int(h // ratio_preview)

    img_main = img.resize((width_main, height_main))
    img_preview = img.resize((width_preview, height_preview))
    image_path = {
        "main": f"./app/static/images/image_{id}_main.jpg",
        "preview": f"./app/static/images/image_{id}_preview.jpg"
    }
    img_main.save(image_path["main"])
    img_preview.save(image_path["preview"])
    return image_path
