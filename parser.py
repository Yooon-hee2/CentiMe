import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time
import text_crawling
import category
import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstone.settings")
import django
django.setup()
from crawling.models import Category
from clothes.models import Outer, Top, Skirt, Pants, Ops
from django.conf.global_settings import AUTH_USER_MODEL

# def parse(sel_size, find_category, current_url, category_url): //윤희
def parse(sel_size, find_category):
    #ocr = OCRApi.OCRApi()

    #url = current_url //윤희

    #thumbnail = text_crawling.thumbnail_finder(category_url, current_url) 윤희 썸네일 url 받아오는 부분

    url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
    #url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1' 

    result = text_crawling.textcrawling(url, find_category)
    key_list = list(result.keys())

    # if not result:
    #     import image
    #     url_list = image.true_image(image.get_image_url(url))

    #     refiner = typo_refiner.TypoRefiner()

    #     for url in url_list:
    #         temp_data = ocr.detect_text(url)
    #         for index in range(len(temp_data)):
    #             temp_data[index][0] = refiner(temp_data[index][0])
    #         searchdata = SearchColumnData.SearchColumnData(temp_data)
    #         if searchdata.find_category_in_sizetable():
    #             break

    if sel_size == 0:
        return url, result
    sel_num=0
    for li in key_list:
        if li == sel_size:
            sel_num = key_list.index(li)
            break
    re_result = result[key_list[sel_num]]
    return url, key_list[sel_num], re_result

def temp():
    print()
    