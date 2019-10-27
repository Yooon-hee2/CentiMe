import OCRApi
import SearchColumnData
import SortSizeData
import Dictionary
import typo_refiner
import time


ocr = OCRApi.OCRApi()


# url_list = 아현함수()

# refiner = typo_refiner.TypoRefiner()
# for url in enumerate(url_list):
#     searchdata = SearchColumnData.SearchColumnData(ocr.detect_text(url))
#     searchdata.find_category_in_sizetable()

all_data = ocr.detect_text("https://warmgray.co.kr/warmgray/PT/TIDPT112/TIDPT112_c.jpg")

# print(refiner("믿위"))

# searchdata = SearchColumnData.SearchColumnData(all_data)
# searchdata.find_category_in_sizetable()

# sort = SortSizeData.SortSizeData(4, searchdata)
# sort.sort_by_category()
# searchdata.find_category_in_sizetable()
