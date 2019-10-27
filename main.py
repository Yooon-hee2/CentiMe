import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time


ocr = OCRApi.OCRApi()

all_data = ocr.detect_text("https://warmgray.co.kr/warmgray/PT/TIDPT112/TIDPT112_c.jpg")

refiner = typo_refiner.TypoRefiner()
# print(refiner("믿위"))

# for text_item in all_data:
#     text_item[0] = refiner(text_item[0])
# #     print(text_item[0])


searchdata = SearchColumnData.SearchColumnData(all_data)
searchdata.find_category_in_sizetable()

# sort = SortSizeData.SortSizeData(4, searchdata)
# sort.sort_by_category()
# searchdata.is_same_column(Dictionary.index_dic['hem'])
# searchdata.find_category_in_sizetable()
