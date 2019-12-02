# https://github.com/line/line-bot-sdk-python
# https://qiita.com/kro/items/67f7510b36945eb9689b
# https://qiita.com/bambi_engineer/items/0e8593d3a3047ece3f77
# https://developers.line.biz/console/channel/1653518321
# https://manager.line.biz/account/@535futje/setting

from flask import Flask, request, abort
from argparse import ArgumentParser

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage
)
import os
import datetime
import response
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = 'l4SWZyXcnECkqJTTCKyF4Ud8cAUgsXjhfHOqot2uGWhnxs2ana9rb1SPOjVwr3+mx+R/uiytm/xygkMHRtIn0CABInwK9UEIoMIESTydGo37XqteE46y9VlfRZSCqv7cj9Kkfn/4QWYobicJpO14eQdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'ca94df008b50208788c8f236982477e8'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    google_url = "https://drive.google.com/uc?id=" + response.random_id()
    try:
        if event.message.text in ["ダーディさん", "じっちゃん", "おじいちゃん", "おじいさん", "深井晃"]:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=response.one_word()),
                 ImageSendMessage(original_content_url=google_url,
                                  preview_image_url=google_url)])
        elif event.message.text.split()[0] in ["ダーディさん", "じっちゃん", "おじいちゃん", "おじいさん", "深井晃"] and \
                event.message.text.split()[1] == '画像':
            # Change to saving-image mode
            with open("Constant.json", "r") as fr:
                Constant = json.load(fr)
            Constant["SEND_IMAGE"] = "True"
            Constant["LIMIT_TIME"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            with open("Constant.json", "w") as fw:
                json.dump(Constant, fw, indent=2)

    except:
        pass


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # Allow images to save if it's sent within five mins
    with open("Constant.json", "r") as f:
        Constant = json.load(f)
    LIMIT_TIME = datetime.datetime.strptime(Constant["LIMIT_TIME"], "%Y/%m/%d %H:%M:%S")
    duration = datetime.datetime.now() - LIMIT_TIME
    if Constant["SEND_IMAGE"] == "True" and (duration // datetime.timedelta(minutes=1)) < 5:
        message_id = event.message.id
        message_content = line_bot_api.get_message_content(message_id)
        filename = "{}.jpg".format(message_id)
        path = "memories/" + filename
        with open(filename, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)
        response.upload_image(path, filename)

    else:
        Constant["SEND_IMAGE"] = "False"
        with open("Constant.json", "w") as fw:
            json.dump(Constant, fw, indent=2)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# git add .
# git commit -m "COMMENT"
# git push heroku master
