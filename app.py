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

app = Flask(__name__)

line_bot_api = LineBotApi('2seNVgMgRphdCLHoILweTEWIbYMQk2Wrb9RM0Vq0/s497Pzuir+VIvqV+Rr2j0sm9pKZ1GKSoCct+VMC/879gI72+o/I123YABbABGSLhVZQ8MG/+OMtym6nfam1CqDWOP5AlkyXYV1TyPoT2+LVaQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('13fb4cdecbc0fc32e82dd1810ff3599b')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()