import OCRApi
import table_size_finder
import text_refiner
import text_crawling
import text_size_finder
import image_classification
# ocr = OCRApi.OCRApi()

# #url = "http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2"
# url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'

# result = text_crawling.textcrawling(url)
# for i in result:
#     print(i)

# if not result:
#     import image_classification
#     table_list, line_list = image_classification.classification(url)

#     refiner = typo_refiner.TypoRefiner()

#     for image in image_list:
#         temp_data = ocr.detect_text(image)
#         for index in range(len(temp_data)):
#             temp_data[index][0] = refiner(temp_data[index][0])
#         searchdata = SearchColumnData.SearchColumnData(temp_data)
#         if searchdata.find_category_in_sizetable():
#             break

url = 'http://biznshoe.com/product/detail.html?product_no=3237&cate_no=56&display_group=1'
import image_classification
table_list, line_list = image_classification.classification(url)
category = 'TOP'

ocr = OCRApi.OCRApi()

result = 0

# for table image
for table in table_list:
    temp_data = ocr.detect_text(table)
    if temp_data:
        refiner = text_refiner.TextRefiner(temp_data)
        completed_data = refiner.concatenate()
        finder = table_size_finder.TableSizeFinder(category,completed_data)
        result = finder.find_category_in_sizetable()
        if result:
            break

if result == 0:
    for line in line_list:
        temp_data = ocr.detect_text(line)
        if temp_data:
            refiner = text_refiner.TextRefiner(temp_data)
            completed_data = refiner.concatenate()
            finder = text_size_finder.TextSizeFinder(category,completed_data)
            result = finder.find_category_in_size_image()
            if result:
                break
            
print(result)


