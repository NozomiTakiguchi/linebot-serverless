import os, http.server as http_server, socketserver
import settings # load dotenv
from scraping import Reservator
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, FlexContainer

linebot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

class SimpleLocalHttpHandler(http_server.BaseHTTPRequestHandler):
    def do_POST(self):
        # signature = get_xline_signature(self.headers)
        signature = self.headers.get("X-Line-Signature")
        content_len  = int(self.headers.get("content-length"))
        # req_body = self.rfile.read(content_len).decode("utf-8")
        req_body = self.rfile.read(int(self.headers.get("content-length"))).decode("utf-8")

        try:
            handler.handle(req_body, signature)
        except InvalidSignatureError as e:
            print(e)
        
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.send_response(200)
    
def get_xline_signature(headers):
    def is_prod(signaure):
        # sam local invoke を識別する何か

        # None の場合、テスト以外の何かしらのエラー
        if not signature:
            return True
        
        if signature == '':
            return False

        return True

    signature = None
    for k in headers:
        if k in ['X-Line-Signature', 'x-line-signature']:
            signature = headers[k]
    # flag と signature そのものを typle で返すようにするのはアリ？
    if is_prod(signature):
        pass
    return signature

#aws lambda
def lambda_handler(event, context):
    signature = get_xline_signature(event['headers'])
    req_body = event['body']

    # try:
    #     handler.handle(req_body, signature)
    # except InvalidSignatureError as e:
    #     print(e)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": "Success"
    }

@handler.add(MessageEvent, TextMessage)
def handle_message(body):
    # ↓ 関数化する. x-line-signature がサンプルの場合は sdk 使えなさそうなので 
    # WerbhookHandler じゃないハンドラを実装してそっちからも呼び出す
    driver = Reservator.launch()
    current_url, properties = driver.list_available_schedules()
    messages = driver.format_available_schedule(properties, current_url)

    alt_text = messages['altText']
    template = messages['template']
    columns = [CarouselColumn(
        text=elms['text'],
        title=elms['title'],
        thumbnail_image_url=elms['thumbnailImageUrl'],
        image_background_color=elms['imageBackgroundColor'],
        actions=elms['actions'],
        default_action=elms['defaultAction']
    ) for elms in template['columns']]

    # interact with RichMenu???? PushMessage???? store state in DynamoDB????

    linebot_api.reply_message(
        reply_token=body.reply_token,
        messages=TemplateSendMessage(
            alt_text=alt_text,
            template=CarouselTemplate(columns=columns)
        )
    )

if __name__ == '__main__':
    port = int(os.environ['PORT'])
    try:
        with socketserver.TCPServer(("", port), SimpleLocalHttpHandler, bind_and_activate=False) as httpd:
            print(f"serving at port: {port}")
            httpd.allow_reuse_address = True
            httpd.timeout = 600
            httpd.server_bind()
            httpd.server_activate()
            httpd.handle_request()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('server finished')
        exit(0)
