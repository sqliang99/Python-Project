"""
author: Iris Shi
game prices from gg deals
"""
import time

import pandas as pd
from selenium import webdriver
from tqdm import tqdm


class ggdeal(object):
    def __init__(self):
        self.chrome = webdriver.Chrome(executable_path="./chromedriver")
        self.data = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.chrome.close()

    def get_data_by_page(self, page_number):
        self.chrome.get("https://gg.deals/deals/?minRating=0&page={}".format(page_number))
        """
        scroll down
        """
        for i in range(30):
            js = "var q=document.documentElement.scrollTop={}".format(400 * (i + 1))
            self.chrome.execute_script(js)
        sections = self.chrome.find_elements_by_css_selector("div.hoverable-box")
        with tqdm(sections,total=len(sections)) as t:
            for section in t:
                game_name = None
                original_price = None
                new_price = None
                platform = None
                price_start_date = None
                
                try:
                    game_name = section.find_element_by_css_selector("div.game-info-title-wrapper").text
                except:
                    pass
                try:
                    original_price = section.find_element_by_css_selector("span.price-label").text
                except:
                    pass
                try:
                    new_price = section.find_element_by_css_selector("span.price-inner").text
                except:
                    pass
                try:
                    platform = section.get_attribute("data-shop-name")
                except:
                    pass
                try:   
                    price_start_date = section.find_element_by_css_selector('time.timeago-short').get_attribute("datetime")
                except:
                    pass
                
                if (original_price is not None) and (game_name is not None) and (new_price is not None):
                    self.data.append({
                        "game_name": game_name,
                        "original_price": original_price,
                        "new_price": new_price,
                        'platform':platform,
                        'price_start_date':price_start_date
                    })

    def save_data(self, target_name="result.xls"):
        df = pd.DataFrame(self.data)
        print(df)
        df.to_excel(target_name, index=False, header=True)


if __name__ == '__main__':
    with ggdeal() as crawler:
        for page_number in range(150):
            print("crawling page: {}".format(page_number + 1))
            crawler.get_data_by_page(page_number + 1)
            time.sleep(1)
        crawler.save_data()
