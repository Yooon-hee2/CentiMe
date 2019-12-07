import OCRApi
import table_size_finder
import text_refiner
import text_crawling
import text_size_finder
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

def parse(sel_size, find_category, current_url, category_url):
    #ocr = OCRApi.OCRApi()
    url = current_url
    thumbnail_url = text_crawling.thumbnail_finder(category_url, current_url)
    #url = "https://store.musinsa.com/app/product/detail/957880/0"
    #url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
    #url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'
    #url = "https://www.daybin.co.kr/product/detail.html?product_no=5428&cate_no=152&display_group=1"
    #url = "https://www.daybin.co.kr/product/detail.html?product_no=5273&cate_no=152&display_group=1"
    result = text_crawling.textcrawling(url, find_category)
    #result = ''
    if not result:
        import image_classification
        ocr = OCRApi.OCRApi()
        table_list, line_list = image_classification.classification(url)
        #print("text no")
        # for table image
        for table in table_list:
            temp_data = ocr.detect_text(table)
            if temp_data:
                refiner = text_refiner.TextRefiner(temp_data)
                completed_data = refiner.concatenate()
                finder = table_size_finder.TableSizeFinder(find_category,completed_data)
                result = finder.find_category_in_sizetable()
                if result:
                    break

            if result == 0:
                for line in line_list:
                    temp_data = ocr.detect_text(line)
                    if temp_data:
                        refiner = text_refiner.TextRefiner(temp_data)
                        completed_data = refiner.concatenate()
                        finder = text_size_finder.TextSizeFinder(find_category,completed_data)
                        result = finder.find_category_in_size_image()
                        if result:
                            break
    key_list = list(result.keys())
    # if sel_size == 0:
    #     return url, result
    # sel_num=0
    # for li in key_list:
    #     if li == sel_size:
    #         sel_num = key_list.index(li)
    #         break
    # re_result = result[key_list[sel_num]]
    #print(result)
    return url, key_list, result, thumbnail_url

# if __name__ == '__main__':
#      #textcrawling("http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2", "PANTS")
#     parse(0, "PANTS")
    