import Text
import Dictionary
from collections import Counter

class SearchColumnData():
    def __init__(self, data_list):
        self.data_list = data_list

    def is_digit(self, str):
        try:
            tmp = float(str)
            if tmp > 5 :
                return True
        except ValueError:
            return False

    def find_category_in_sizetable(self):

        candidate_y_pos = []
        candidate_y_index = []

        for i, text in enumerate(self.data_list):
            for category_list in Dictionary.index_dict.values():
                for category in category_list:
                     if text[0] == category:
                        candidate_y_index.append(i)
                        candidate_y_pos.append((text[1].y_pos + text[3].y_pos)/2)
                        break


        # for i in range(len(candidate_y_pos)):
        #     print(candidate_y_pos[i], "size : ", len(candidate_y_pos))

        t_candidate_y_pos = [int(x // 5 * 5) for x in candidate_y_pos]

        # for i in range(len(t_candidate_y_pos)):
        #     print(t_candidate_y_pos[i])

        y_counter = Counter(t_candidate_y_pos)

        max_y_coordinate = []
        if len(y_counter) > 0:
            max_y_coordinate = max(list(y_counter.items()), key = lambda a : a[1])

        size_category_collections = []

        # 밑에 +- 5 나중에 수정할것
        if max_y_coordinate:
            for i in range(len(t_candidate_y_pos)):
                if t_candidate_y_pos[i] == max_y_coordinate[0] or t_candidate_y_pos[i] == max_y_coordinate[0] + 5 or \
                    t_candidate_y_pos[i] == max_y_coordinate[0]- 5:
                    size_category_collections.append(candidate_y_index[i])


        if (len(size_category_collections) < 4):
            print("it's not image about size")
            return False

        # self.is_same_column(size_category_collections)

        return self.is_same_column(size_category_collections)

    def is_same_column(self, size_category_name):

        same_column_data = []
        size_num_by_category = []

        for i in range(len(size_category_name)):
            temp, num_of_size, category_name = self.is_valid_location(size_category_name[i])
            if len(temp) > 0:
                same_column_data.append(temp)
                size_num_by_category.append(num_of_size)

        return same_column_data, size_num_by_category

        # self.is_one_word(same_column_index)
        # self.check_data_in_sizetable(same_column_index)

    def string_to_number(self, string):
        try:
            if int(string) < 150:
                return int(string)
            elif int(string) >= 150 and int(string) < 1000:
                return int(string)/10
            elif int(string) >= 1000:
                return int(string)/100
        except ValueError:
            return float(string) 


    def is_valid_location(self, index):

        def obtain_center(data):
            bounds = data[1:]
            x0 = bounds[0].x_pos
            y0 = bounds[0].y_pos
            x1 = bounds[2].x_pos
            y1 = bounds[2].y_pos
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2
            return x_center, y_center

        category = self.data_list[index][0]
        c_x_center, c_y_center = obtain_center(self.data_list[index])
        data_length = int(self.data_list[index][2].x_pos) \
            - int(self.data_list[index][1].x_pos)
        
        temp = []

        for i, data in enumerate(self.data_list):
            temp_x_center, temp_y_center = obtain_center(data)
            # print(data[0] , " : " , abs(c_x_center - temp_x_center))

            if temp_y_center > c_y_center and abs(c_x_center - temp_x_center) <= 35:
                data[0] = data[0].replace("cm", "")
                data[0] = data[0].replace("CM", "")
                data[0] = data[0].replace(',', '.')
                if self.is_digit(data[0]):
                    index_container = Text.Text()
                    index_container.category = self.data_list[index][0]
                    index_container.index = i
                    index_container.text = self.string_to_number(data[0])
                    index_container.height = temp_y_center
                    temp.append(index_container)
                

        

        if len(temp) > 1:
            trimmed_index = len(temp)
            for ii, elem in enumerate(temp):
                if ii > 0 and self.data_list[temp[ii].index][2].y_pos - self.data_list[temp[ii-1].index][2].y_pos > 200:
                    trimmed_index = ii
                    temp = temp[:trimmed_index]
                    break
        

    
        # print("category : " , self.data_list[index][0])
        # print([x.text for x in temp])
        return temp, len(temp), self.data_list[index][0]




    # def is_one_word(self, same_column_index):
    #      for i in range(len(same_column_index) - 1):
    #         if self.data_list[same_column_index[i]][1].y_pos == self.data_list[same_column_index[i + 1]][1].y_pos:
    #             self.data_list[same_column_index[i]][0] = self.data_list[same_column_index[i]][0] + self.data_list[same_column_index[i + 1]][0]
    #             # print(self.data_list[same_column_index[i]][0])
    #             del same_column_index[i+1]
    #             return same_column_index


    # def check_data_in_sizetable(self, same_column_index, category):

    #     if len(same_column_index) > 2 and category != "사이즈":
    #         trimmed_index = len(same_column_index)
    #         for i, elem in enumerate(same_column_index):
    #             if i > 0 and self.data_list[same_column_index[i].index][2].y_pos - self.data_list[same_column_index[i-1].index][2].y_pos > 200:
    #                 trimmed_index = i
    #                 break
            
    #         same_column_index = same_column_index[:trimmed_index]
            

    #     if category != "사이즈":
    #         for j in range(len(same_column_index)):
    #             print(same_column_index[j].index , "   " ,  same_column_index[j].text, self.data_list[same_column_index[j].index][2].y_pos)            