from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from ai import chat
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from llm2 import chat

app = Flask(__name__)

CHANNEL_SECRET = ""
CHANNEL_ACCESS_TOKEN = ""

@app.route("/", methods=['GET'])
#def home():
        #return "Hi"

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            tk = event.reply_token
            msg = event.message.text
            reply_text = chat(msg)  # 使用 AI 模組來獲取回復的文本
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'

app.run(port="5000")
~                             
