import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time
import text_crawling
import text_size_finder

ocr = OCRApi.OCRApi()

# #url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
# url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'

# result = text_crawling.textcrawling(url)
# for i in result:
#     print(i)

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



# 표이미지일때
# refiner = typo_refiner.TypoRefiner()
# temp_data = ocr.detect_text('http://knocklady.com/web/upload/NNEditor/20190826/20190823_%ED%81%B4%EB%A1%9C%EC%A0%80%EC%B9%B4%EA%B3%A0%EC%A1%B0%EA%B1%B0%ED%8C%AC%EC%B8%A0_4_shop1_185726.jpg')
# for index in range(len(temp_data)):
#     temp_data[index][0] = refiner(temp_data[index][0])
# searchdata = SearchColumnData.SearchColumnData(temp_data)

# size_list, size_number_list = searchdata.find_category_in_sizetable()


# sort = SortSizeData.SortSizeData(4, temp_data, size_list, size_number_list)
# sort.sort_by_category()

# 줄글이미지일때
refiner = typo_refiner.TypoRefiner()
temp_data = ocr.detect_text('https://dododaily.com/web/upload/NNEditor/20190923/3017%E1%84%89%E1%85%A1%E1%86%BC%E1%84%89%E1%85%A61_shop1_160924.jpg')
for index in range(len(temp_data)):
    temp_data[index][0] = refiner(temp_data[index][0])
searchdata = text_size_finder.TextSizeFinder(temp_data)
searchdata.find_category_in_size_image()