import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time
import image

ocr = OCRApi.OCRApi()



url_list = image.true_image(image.get_image_url())

refiner = typo_refiner.TypoRefiner()

for url in url_list:
    searchdata = SearchColumnData.SearchColumnData(ocr.detect_text(url))
    if searchdata.find_category_in_sizetable():
        break



# print(refiner("믿위"))

# for text_item in all_data:
#     text_item[0] = refiner(text_item[0])
# #     print(text_item[0])

# sort = SortSizeData.SortSizeData(4, searchdata)
# sort.sort_by_category()
# searchdata.is_same_column(Dictionary.index_dic['hem'])
# searchdata.find_category_in_sizetable()
