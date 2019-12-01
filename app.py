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
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import os
import json
import threading
import datetime
import response

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
    if event.message.text in ["ダーディさん", "じっちゃん", "おじいちゃん", "おじいさん", "深井晃"]:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=response.one_word()),
             ImageSendMessage(original_content_url="https://zicchan-bot.herokuapp.com/memories/LINE.png",
                              preview_image_url="https://zicchan-bot.herokuapp.com/memories/LINE.png")])


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# git add .
# git commit -m "COMMENT"
# git push heroku master
