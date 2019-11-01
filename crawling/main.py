from . import OCRApi
from . import SearchColumnData
from . import SortSizeData
from . import Dictionary
from . import typo_refiner
import time
from . import text_crawling

ocr = OCRApi.OCRApi()

url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
#url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'

result = text_crawling.textcrawling(url)
for i in result:
    print(i)

if not result:
    import image
    url_list = image.true_image(image.get_image_url(url))

    refiner = typo_refiner.TypoRefiner()

    for url in url_list:
        temp_data = ocr.detect_text(url)
        for index in range(len(temp_data)):
            temp_data[index][0] = refiner(temp_data[index][0])
        searchdata = SearchColumnData.SearchColumnData(temp_data)
        if searchdata.find_category_in_sizetable():
            break


# import image
# url_list = image.true_image(image.get_image_url(url))
#
# refiner = typo_refiner.TypoRefiner()
#
# for url in url_list:
#     temp_data = ocr.detect_text(url)
#     for index in range(len(temp_data)):
#         temp_data[index][0] = refiner(temp_data[index][0])
#     searchdata = SearchColumnData.SearchColumnData(temp_data)
#     if searchdata.find_category_in_sizetable():
#         break


# sort = SortSizeData.SortSizeData(4, searchdata)
# sort.sort_by_category()
# searchdata.is_same_column(Dictionary.index_dic['hem'])
# searchdata.find_category_in_sizetable()