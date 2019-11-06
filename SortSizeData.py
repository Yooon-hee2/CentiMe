import SearchColumnData
import Jeans
import Dictionary
import Text
from collections import Counter


class SortSizeData():
    def __init__(self, category_num, data_list, size_list, size_number_list):
        self.category_num = category_num
        self.data_list = data_list
        self.size_list = size_list
        self.size_number_list = size_number_list

    def sort_by_category(self):

        self.missing_data_finder()

        if self.category_num == 4:
            complete_size_dict = {'waist' : 0, 'hip' : 0, 'thigh' : 0, 'hem' : 0, 'crotch_rise' : 0, 'length' : 0}

            size_name = ['S', 'M', 'L', 'XL' , '2XL']

            for size_by_category in self.size_list:
                for category_title, category_name in Dictionary.index_dict.items():
                    for category in category_name:
                        if category == size_by_category[0].category:
                            for sizes in size_by_category:
                                complete_size_dict[category_title] = sizes.text
                        
            print(complete_size_dict)

        return complete_size_dict

    def missing_data_finder(self):

        cnt = Counter(self.size_number_list)
        mode = cnt.most_common(1)
        print("mode : " , mode)

        # #for print before add missing size data
        # for yoonhee in range(len(self.size_list)):
        #     if self.size_list[yoonhee]:
        #         print(self.size_list[yoonhee][0].category)
        #         # for jj in range(0, mode[0][0]):
        #         for jj in range(len(self.size_list[yoonhee])):
        #             print(self.size_list[yoonhee][jj].text)
        complete_size_category = 0
        # find category that size datas are missing
        for yoonhee in range(len(self.size_list)):
            if len(self.size_list[yoonhee]) == mode[0][0]: 
                complete_size_category = yoonhee
            elif len(self.size_list[yoonhee]) < mode[0][0]:
                self.add_missing_data(mode[0][0], yoonhee, complete_size_category, mode[0][0] - len(self.size_list[yoonhee]))
    

      #for print
        for yoonhee in range(len(self.size_list)):
            if self.size_list[yoonhee]:
                print(self.size_list[yoonhee][0].category)
                for jj in range(0, mode[0][0]):
                # for jj in range(len(self.size_list[yoonhee])):
                    print(self.size_list[yoonhee][jj].text)



    def add_missing_data(self, maximum_size, missing_index, complete_index, missing_number):

        if missing_number == 0 or maximum_size == 1:
            return 0

        print("missing index : ", missing_index)

        # for iiiii in range(len(self.size_list[complete_index])):
        #     print(self.size_list[complete_index][iiiii].height)

        # for iii in range(len(self.size_list[missing_index])):
        #     print(self.size_list[missing_index][iii].height)


        temp = []

        for i, complete_y in enumerate(self.size_list[complete_index]):
            for j, missing_y in enumerate(self.size_list[missing_index]):
                if missing_y.height <= complete_y.height + 5 \
                    and missing_y.height >= complete_y.height - 5:
                    temp.append(i)
                    break


        temp_container = Text.Text()
        temp_container.category = self.size_list[missing_index][0].category

        missing_index_in_category = 0
        
        for index,x in enumerate(temp):
            if index != x:
                missing_index_in_category = index
                break

        temp_container.height = self.size_list[complete_index][missing_index_in_category].height

        if missing_index_in_category == 0:
            if maximum_size == 2:
                print("1")
                temp_container.text = self.size_list[missing_index][1].text - 1
                self.size_list[missing_index].insert(0, temp_container)

            else:
                print("2")
                gap = self.size_list[missing_index][1].text - self.size_list[missing_index][0].text
                temp_container.text = self.size_list[missing_index][0].text - gap
                self.size_list[missing_index].insert(0, temp_container)

        elif missing_index_in_category == maximum_size - 1:
            if maximum_size == 2:
                print("3")
                temp_container.text = self.size_list[missing_index][0].text + 1
                self.size_list[missing_index].insert(1, temp_container)

            else:
                print("4")
                gap = self.size_list[missing_index][1].text - self.size_list[missing_index][0].text
                temp_container.text = self.size_list[missing_index][missing_index_in_category - 1].text + gap
                self.size_list[missing_index].insert(missing_index_in_category, temp_container)

        elif maximum_size > 2 and missing_index_in_category != 0 and missing_index_in_category != maximum_size - 1:
            print("5")
            temp_container.text = (self.size_list[missing_index][missing_index_in_category - 1].text + self.size_list[missing_index][missing_index_in_category + 1].text)/2
            self.size_list[missing_index].insert(missing_index_in_category, temp_container)







