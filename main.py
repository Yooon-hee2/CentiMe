import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time
import text_crawling

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




refiner = typo_refiner.TypoRefiner()
temp_data = ocr.detect_text('http://monody88.jpg2.kr/upload/191010/%EC%B9%BC%EB%A6%AC%EC%95%84%20%EC%BB%B7%ED%8C%85%20%EC%8A%AC%EB%A6%BC%EC%9D%BC%EC%9E%90%20%EB%8D%B0%EB%8B%98/info.jpg')
for index in range(len(temp_data)):
    temp_data[index][0] = refiner(temp_data[index][0])
searchdata = SearchColumnData.SearchColumnData(temp_data)

size_list, size_number_list = searchdata.find_category_in_sizetable()


sort = SortSizeData.SortSizeData(4, temp_data, size_list, size_number_list)
sort.sort_by_category()
# searchdata.is_same_column(Dictionary.index_dic['hem'])
# searchdata.find_category_in_sizetable()