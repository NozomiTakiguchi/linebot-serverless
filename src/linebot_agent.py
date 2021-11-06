import os, http.server as http_server, socketserver
import settings # load dotenv
from scraping import Reservator
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, FlexContainer

linebot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# Docker in Docker で AWS SAM CLI がうまく扱えなかったので、ひとまずローカルに http server 立ててみた (本当は簡単に AWS Lambda に移行できるようにしたい)
class SimpleLocalHttpHandler(http_server.BaseHTTPRequestHandler):
    def do_POST(self):
        signature = self.headers.get('X-Line-Signature')
        content_len  = int(self.headers.get("content-length"))
        req_body = self.rfile.read(content_len).decode("utf-8")

        try:
            handler.handle(req_body, signature)
        except InvalidSignatureError as e:
            print(e)
        
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.send_response(200)
    
@handler.add(MessageEvent, TextMessage)
def handle_message(body):
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
