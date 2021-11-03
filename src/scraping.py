# https://qiita.com/hoto17296/items/c2abfb60d3c6a77f065d
# https://xp-cloud.jp/blog/2020/01/22/6637/
import chromedriver_binary # installed through pip in Dockerfile. Implicitly used when instantiate webdriver
import json
import time
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import (
    CONFIG,
    CHROME_OPTIONS,
    LINEBOT_CAROUSEL_TEMPLATE,
    BASE_URL,
    TODAY
    )


INNER_OPTIONS = webdriver.ChromeOptions()
for option in CHROME_OPTIONS:
    INNER_OPTIONS.add_argument(option)

class Reservator():
    def __init__(self, chrome_options, region='kanto', genre='futsal', area_id=2, exec_date=TODAY) -> None:
        self.base_url = BASE_URL.format(region, genre, area_id, exec_date)
        self.area = CONFIG['area'][area_id]
        self.driver = webdriver.Chrome(options=chrome_options)
        self.drivers_pool = []
        self.results = []

    @staticmethod
    def launch():
        options = webdriver.ChromeOptions()
        # options.binary_location = '/opt/python/bin/headless-chromium'
        for option in CHROME_OPTIONS:
            options.add_argument(option)

        return Reservator(options)

    def list_available_schedules(self):
        self.driver.get(self.base_url)
        current_url = self.base_url
        for web_element in self.driver.find_elements(By.CLASS_NAME, 'default-schedule-row'):
            if len(self.results) >= 9:
                break
            # 開催日程
            date = web_element.find_element(By.CLASS_NAME, 'date').find_element(By.CSS_SELECTOR, 'span').get_attribute('innerHTML')
            # 開催地情報 url
            loc_url = web_element.find_element(By.CLASS_NAME, 'court').find_element(By.TAG_NAME, 'a').get_attribute('href')
            # 予約ページ url
            detail_url = web_element.find_element(By.CLASS_NAME, 'dtl').find_element(By.TAG_NAME, 'a').get_attribute('href')

            # すべての url を driver.get すると replyToken が expire するので仕方なく..
            if loc_url not in CONFIG['courts']:
                court_img = 'https://www.calcio-a.com/images/w360_h270/c/2/c25f6ec2c96ef8bacfc89fd4433d216c.png' #TODO なかった時に no image png とかいれる
            else:
                court_img = CONFIG['courts'][loc_url]
            
            self.results.append({
                'imageUri': court_img,
                'name': date,
                'uri': detail_url
            })
        return current_url, self.results

    def add_detail_navigation_carousel_if_exceeded(self):
        print('to be impled.')
        pass
    
    def format_available_schedule(self, properties, current_url):
        template = Template(LINEBOT_CAROUSEL_TEMPLATE)
        return json.loads(template.render(properties=properties))


def main():
    # test locally
    start_time = time.time()
    driver = Reservator.launch()
    current_url, properties = driver.list_available_schedules()
    messages = driver.format_available_schedule(properties, current_url)
    print(messages)
    print(f'finished in {time.time() - start_time} seconds.')


if __name__ == '__main__':
    #lambda をローカルでテストできるようにしたい
    event = []
    main()
