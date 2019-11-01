#카테고리 파싱 후 리턴
from selenium import webdriver
from bs4 import BeautifulSoup
import requests as req
import re

def prepare_category(dic_val):
    searching_dic = {'outer': ['아우터', 'OUTER', '자켓', '코트', '가디건'],
                     'top': [],
                     'skirt': [],
                     'pants': ['BOTTOM', 'PANTS', '바지', '하의'],
                     'ops': []}  # 카테고리 딕셔너리 만들기

    for dic, val in searching_dic.items():
        for vl in val:
            if vl == dic_val:
                sh = dic

    cate_dic = {'outer': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'top': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'skirt': ['waist', 'hip', 'hem', 'length'],
                'pants': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
                'ops': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']}
    # 카테고리 항목 딕셔너리
    # return cate_dic[sh]
    return cate_dic["pants"]


def category_parse():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    url = str
    response = req.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml", from_encoding='ANSI')

    category = soup.find(href=url)
    if category:
        category = category.string
    else:
        domain = re.sub(r'(http(S)?:\/\/)([0-9a-zA-Z\-]+\.*)+[a-z0-9]{2,4}','',url)
        category = soup.find(href=domain).string

    return category
