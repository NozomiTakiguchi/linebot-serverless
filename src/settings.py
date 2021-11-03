# https://qiita.com/hedgehoCrow/items/2fd56ebea463e7fc0f5b

import os
from os.path import join, dirname
from dotenv import load_dotenv
import yaml
from yaml.loader import SafeLoader

dotenv_path = join(dirname(__file__), os.pardir, '.env')
load_dotenv(dotenv_path)

config_path = join(dirname(__file__), 'config.yaml')
with open(config_path) as f:
    CONFIG = yaml.load(f, Loader=SafeLoader)

CHROME_OPTIONS = [
    '--headless',
    '--no-sandbox',
    # '--single-process',
    # '--process-per-tab',
    # selenium session deleted because of page crash from tab crashed で怒られる時の呪文
    '--disable-dev-shm-usage'
]
BASE_URL =  'https://www.calcio-a.com/games/{}?type={}&area_id={}&court_id=back&exec_dt={}'

# https://developers.line.biz/ja/reference/messaging-api/#template-messages
LINEBOT_CAROUSEL_TEMPLATE = """{
    "type": "template",
    "altText": "Linebot returned search result",
    "template": {
        "type": "carousel",
        "columns": [
{%- for p in properties  %}
            {
                "thumbnailImageUrl": "{{ p.imageUri }}",
                "imageBackgroundColor": "#FFFFFF",
                "title": "{{ p.name }}",
                "text": "{{ p.name }}",
                "defaultAction": {
                    "type": "uri",
                    "label": "View Detail",
                    "uri": "{{ p.uri }}"
                },
                "actions": [
                    {
                        "type": "uri",
                        "label": "View Detail",
                        "uri": "{{ p.uri }}"
                    }
                ]
            }{%- if not loop.last %},{%- endif %}
{%- endfor %}
        ]
    }
}"""