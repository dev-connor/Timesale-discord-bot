from bs4 import BeautifulSoup
import requests
import re

# https://www.musinsa.com/categories/item/018?d_cat_cd=018&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=Y&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure=
url = 'https://www.musinsa.com/categories/item/018'
params = {
    'd_cat_cd':'018',
    'list_kind':'small',
    'sort':'pop_category',
    'page':'1',
    'display_cnt':'90',
    'timesale_yn':'Y',
}
headers = {
    'user-agent': "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'"
}

response = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(response.text,'html.parser')
list_box = soup.find('div', class_='list-box')
item_boxes = list_box.find_all('li', class_='li_box')
price_pattern = re.compile(r'[\d,]+원')

for item_box in item_boxes:
    item_title = item_box.find('p', class_='item_title').findChild('a')
    brand = item_title.text

    item_link = item_box.find('p',class_='list_info').findChild('a')
    name = item_link.text.strip()
    url = item_link['href']

    item_price = item_box.find('p',class_='price')
    prices = price_pattern.findall(item_price.text)

    item = {
        'brand': brand,
        'name': name,
        'url': url,
        'original_price': prices[0],
        'sale_price': prices[1],
    }
    print(item)
