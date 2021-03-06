#코디샵 크롤링

import shutil
import time
import urllib.request
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def musinsa_crawling(page_num):
    main_url = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page='
    url = main_url + str(page_num)

    print(url)

    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(3)

    page_string = driver.page_source
    soup = BeautifulSoup(page_string, features="html.parser")

    item_list = soup.findAll('li', {'class': 'style-list-item'})
    for item in item_list:
        item_img = ""
        item_category = ""
        item_num = ""
        item_link = ""

        temp = item.find('img', {'class': 'style-list-thumbnail__img'})['src']
        item_img = 'https:' + temp
        print(item_img)

        item_category = item.find('span', {'class': 'style-list-information__text'}).get_text()
        print(item_category)

        item_num = item.find('a', {'class': 'style-list-item__link'})['onclick']
        item_num = item_num[8:-3]
        print(item_num)

        item_link += 'https://www.musinsa.com/app/styles/views/'
        item_link += str(item_num)
        item_link += '?use_yn_360=&style_type=&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date'
        print(item_link)

        Item_list.append((item_img, item_category, item_num, item_link))

    driver.close()


Item_list = []

#데이터 수집
for i in range(1, 116):
    musinsa_crawling(i)

# 이미지 저장
for i in range(len(Item_list)):
    image_url = Item_list[i][0]
    resp = requests.get(image_url, stream=True)
    local_file = open('D:\Sooo\img_data\\' + '코디' + Item_list[i][2] + '.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp

f = open('codi_data.csv', 'w')
f.write('이미지, 카테고리, 번호, 링크\n')

#데이터 저장
for i in range(len(Item_list)):
    f.write(Item_list[i][0] + ',' + Item_list[i][1] + ',' + Item_list[i][2] + ',' + Item_list[i][3] + '\n')

f.close()