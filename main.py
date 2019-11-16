import OCRApi
import table_size_finder
import text_refiner
import text_crawling
import text_size_finder

# ocr = OCRApi.OCRApi()

# #url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
# url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'

# result = text_crawling.textcrawling(url)
# for i in result:
#     print(i)

# if not result:
#     import image
#     image_list = image.true_image(image.get_image_url(url))

#     refiner = typo_refiner.TypoRefiner()

#     for image in image_list:
#         temp_data = ocr.detect_text(image)
#         for index in range(len(temp_data)):
#             temp_data[index][0] = refiner(temp_data[index][0])
#         searchdata = SearchColumnData.SearchColumnData(temp_data)
#         if searchdata.find_category_in_sizetable():
#             break


ocr = OCRApi.OCRApi()
temp_data = ocr.detect_text('http://daybin.co.kr/web/upload10/117-4.jpg')

refiner = text_refiner.TextRefiner(temp_data)
completed_data = refiner.concatenate()

# for table image

finder = table_size_finder.TableSizeFinder('PANTS',completed_data)
result = finder.find_category_in_sizetable()
 
# for text image
# finder = text_size_finder.TextSizeFinder('PANTS',completed_data)
# result = finder.find_category_in_size_image()

print(result)

