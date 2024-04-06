import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from bs4 import BeautifulSoup
from my_utils import save_list_to_txt_file

from urllib.parse import urlparse

from datetime import datetime

import os

OUTPUT_DIR = 'output'
class ProductScraper:
    def __init__(self, category_links={}):
        self.driver = webdriver.Chrome()
        self.category_links = category_links
        self.current_datetime = datetime.today().strftime('%Y%m%d_%H%M%S')

    def extract_tech_specs(self, soup):
        # print(soup)
        
        big_types = soup.find_all(class_="parameter-ttl")
        # print(big_types)
        tech_specs_dict = {}
        for big_type in big_types:
            big_type_name = big_type.text.strip()

            # print(big_type_name)

            tech_specs_dict[big_type_name] = {}
            sibling = big_type.find_next_sibling("ul")
            if sibling:
                for li in sibling.find_all("li"):
                    smaller_type = li.find("div", class_="ctLeft").text.strip(": \n")
                        
                    detail_tag = li.find("div", class_="ctRight")
                    circles = detail_tag.find_all("p", class_="circle")
                    if circles:
                        detail = [circle.text.strip() for circle in circles]
                    else:
                        detail = detail_tag.text.strip()

                    tech_specs_dict[big_type_name][smaller_type] = detail
                    
                    if smaller_type == "Hãng":
                        tech_specs_dict[big_type_name][smaller_type] = detail.replace(". Xem thông tin hãng", '').strip()

        # post preprocessing
        tech_specs_dict['Màn hình']['Màn hình rộng'] = tech_specs_dict['Màn hình']['Màn hình rộng'].replace("\"", " inch")

        # print(len(tech_specs_dict))
        return tech_specs_dict
    
    def extract_general_info(self, soup):
        # Name
        name = soup.find('section').find('h1').text

        # Colors
        colors_tag = soup.find('div', class_='box03 color group desk')

        if colors_tag:
            all_colors = [a_tag.get_text() for a_tag in colors_tag.find_all('a', class_='box03__item')]
            this_color = colors_tag.find('a', class_='box03__item item act').text

        else:
            all_colors = this_color = None


        # Versions
        versions_tag = soup.find('div', class_='box03 group desk')

        if versions_tag:

            all_versions = [a_tag.get_text() for a_tag in versions_tag.find_all('a', class_='box03__item')]
            this_version = versions_tag.find('a', class_='box03__item item act').text

        else: 
            all_versions = this_version = None

        # Prices
        price_tag = soup.find('div', class_='bs_price')

        if price_tag:
            present_price = price_tag.find('strong').text
            original_price = price_tag.find('em').text
            discount_percentage = price_tag.find('i').text.replace('(', '').replace(')', '').replace('-', '')
            promotion_end_date = soup.find('div', class_='bs_time').find_all('span')[1].text
        
        else:
            
            price_tag = soup.find('div', class_='price-one')
            if price_tag:
                present_price = price_tag.find('p', class_='box-price-present').text.strip()
                
                original_price_tag = price_tag.find('p', class_='box-price-old')
                if original_price_tag:
                    original_price = original_price_tag.text.strip()
                else: 
                    original_price = None
                    
                discount_percentage_tag = price_tag.find('p', class_='box-price-percent')
                if discount_percentage_tag:
                    discount_percentage = discount_percentage_tag.text.strip().replace('-', '')
                else: 
                    discount_percentage = None

                promotion_end_date_tag = soup.find('i', class_='pr-txt')
                if promotion_end_date_tag:
                    promotion_end_date = promotion_end_date_tag.text
                else:
                    promotion_end_date = None
            else:
                present_price = original_price = discount_percentage = promotion_end_date = None


        # Policies
        policy_tag = soup.find('div', class_='policy')
        policies = [p_tag.text.replace('Xem chi tiết', '').replace('Xem địa chỉ bảo hành', '').replace('Xem hình', '').strip() for p_tag in policy_tag.find_all('p')]

        # Promotion
        promotion_tags = soup.find_all('div', class_='divb-right')
        promotions = [p.text.replace("(Xem chi tiết tại đây)", '').replace("Xem chi tiết", '').strip() for p in promotion_tags]

        return {
            'name': name,
            # 'color': this_color,
            'all_color': all_colors,
            'storage': this_version,
            # 'color_versions': {'all_colors_version': all_colors, 'this_color_version': this_color},
            # 'storage_versions': {'all_storage_versions': all_versions, 'this_storage_version': this_version},
            # 'policies': policies,
            'prices': {'giá hiện tại': present_price, 'giá gốc': original_price, 'phần trăm giảm giá': discount_percentage, 'khuyến mãi áp dụng đến': promotion_end_date},
            # 'promotions': promotions
        }



    def scrape_category_links(self):
        product_urls = {}
        for category, category_link in self.category_links.items():
            self.driver.get(category_link)
            while True:
                try:
                    button = self.driver.find_element(By.CLASS_NAME, "view-more")
                    button.click()
                except (ElementNotInteractableException, ElementClickInterceptedException):
                    break

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            all_products = soup.find_all('a', class_='main-contain')
            product_urls[category] = ['https://thegioididong.com' + product['href'] for product in all_products]

        for category, urls in product_urls.items():
            save_list_to_txt_file(urls, os.path.join(os.path.join(OUTPUT_DIR, 'product_urls_list'), f'{category}_product_urls_list_{self.current_datetime}.txt'))

        return product_urls

    def scrape_product_info(self, category, product_url):
        self.driver.get(product_url)
    # try:
        button_chct = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-detail.btn-short-spec")))
        button_chct.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[text()='Hãng:']")))

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # product_name = urlparse(product_url).path.split("/")[-1]
        # save_to_txt_file(str(soup), f'debug/soup_{product_name}.txt')

        product_id = '-'.join(urlparse(product_url).path.split("/")[-2:])

        general_info = self.extract_general_info(soup)

        tech_specs = self.extract_tech_specs(soup)

        tien_ich = tech_specs.pop("Tiện ích")

        thong_tin_chung = tech_specs.pop('Thông tin chung')

        thong_so_ky_thuat = tech_specs
        
        # button = self.driver.find_element(By.ID, 'tab-article-gallery-0')
        # button.click()
        # soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # product_info = soup.find('div', class_='content-article').get_text().strip()

        rating_tag = soup.find('div', class_='point')
        if rating_tag:
            rating = rating_tag.p.text.strip()
        else:
            rating = "Chưa có đánh giá"

        reviews_tag = soup.find('a', class_ = 'total-cmtrt')
        if reviews_tag:
            n_reviews = reviews_tag.text.replace('đánh giá', '').strip()
        else:
            n_reviews = 0


        # product_info_dict = {
        #     'product_id': product_id,
        #     'url': product_url,
        #     'name': general_info['name'],
        #     'color_versions': general_info['color_versions'],
        #     'storage_versions': general_info['storage_versions'],
        #     'policies': general_info['policies'],
        #     'prices': general_info['price'],
        #     'promotions': general_info['promotions'],
        #     'tech_specs': tech_specs,
        #     'review': {'rating': rating, 'n_reviews': n_reviews}
        #     # 'info': product_info
        # }

        product_info_dict = {
            'product_id': product_id,
            'url': product_url,
            'tên sản phẩm': general_info['name'],
            'tất cả màu sắc': general_info['all_color'],
            # 'dung lượng lưu trữ': 
            # 'còn hàng'
            # 'thông tin chung: '
            'giá': general_info['prices'],
            "thông tin chung": thong_tin_chung,
            'thông số kỹ thuật': thong_so_ky_thuat,
            "tiện ích": tien_ich,
            'đánh giá': {'điểm đánh giá trung bình': rating, 'số lượng đánh giá': n_reviews}
        }
        

        with open(os.path.join(os.path.join(OUTPUT_DIR, 'product_data'), f'{category}_products_{self.current_datetime}.json'), 'a', encoding='utf-8') as outfile:
            json.dump(product_info_dict, outfile, ensure_ascii=False)
            outfile.write('\n')

    # except (TimeoutException, NoSuchElementException) as e:
        # print("Error processing:", product_url, "--", str(e))
    # except:
    #     print("Error processing:", product_url)

    #     with open(os.path.join(os.path.join(OUTPUT_DIR, 'product_urls_list'), f'{category}_error_products_list_{self.current_datetime}.txt'), 'a', encoding='utf-8') as outfile:
    #         json.dump(product_url, outfile, ensure_ascii=False)
    #         outfile.write('\n')
        # return None

    def scrape_all_products(self, product_urls=None):
        if product_urls == None:
            product_urls = self.scrape_category_links()
        # product_urls = ['https://thegioididong.com/may-tinh-bang/oppo-pad-neo-6gb']

        for category, urls in product_urls.items():
            print(f"Processing {len(urls)} products for category: {category}")
            for url in urls[:]:
                print("Processing:", url)
                try: 
                    self.scrape_product_info(category, url)
                except:
                    print("Error processing:", url)

                    with open(os.path.join(os.path.join(OUTPUT_DIR, 'product_urls_list'), f'{category}_error_products_list_{self.current_datetime}.txt'), 'a', encoding='utf-8') as outfile:
                        json.dump(url, outfile, ensure_ascii=False)
                        outfile.write('\n')
                    continue

        self.driver.quit()

if __name__ == "__main__":
    category_links = {
        # 'tablet': 'https://www.thegioididong.com/may-tinh-bang',
        # 'phone': 'https://www.thegioididong.com/dtdd',
        'laptop': 'https://www.thegioididong.com/laptop'
    }

    product_urls = {'phone': ['https://www.thegioididong.com/dtdd/samsung-galaxy-a25-6gb?code=0131491003941']}
    scraper = ProductScraper(category_links=category_links)
    scraper.scrape_all_products()
