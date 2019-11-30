# https://github.com/line/line-bot-sdk-python
# https://qiita.com/kro/items/67f7510b36945eb9689b

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

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
    print("test")
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
