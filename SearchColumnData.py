import Text
import Dictionary
from collections import Counter

class SearchColumnData:
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

        for i in range(len(self.data_list)):
            for j in range(len(Dictionary.index_dict['length'])):
                if self.data_list[i][0] == Dictionary.index_dict['length'][j]:
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)
            for j in range(len(Dictionary.index_dict['waist'])):
                if self.data_list[i][0] == Dictionary.index_dict['waist'][j]:
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)    
            for j in range(len(Dictionary.index_dict['crotch_rise'])):
                if self.data_list[i][0] == Dictionary.index_dict['crotch_rise'][j]:
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)
            for j in range(len(Dictionary.index_dict['thigh'])):
                if self.data_list[i][0] == Dictionary.index_dict['thigh'][j]:
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)
            for j in range(len(Dictionary.index_dict['hip'])):
                if self.data_list[i][0] == Dictionary.index_dict['hip'][j]:
                    # print("hello", i)
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)
            for j in range(len(Dictionary.index_dict['hem'])):
                if self.data_list[i][0] == Dictionary.index_dict['hem'][j]:
                    candidate_y_index.append(i)
                    candidate_y_pos.append(self.data_list[i][1].y_pos)


        # for i in range(len(candidate_y_pos)):
        #     print(candidate_y_pos[i], "size : ", len(candidate_y_pos))

        if(len(candidate_y_pos) < 5):
            return False

        t_candidate_y_pos = [int(x // 5 * 5) for x in candidate_y_pos]

        # for i in range(len(t_candidate_y_pos)):
        #     print(t_candidate_y_pos[i])

        y_counter = Counter(t_candidate_y_pos)

        max_y_coordinate = max(list(y_counter.items()), key = lambda a : a[1])
        # print("max : " , max_y_coordinate)

        size_category_collections = []

        # 밑에 +- 5 나중에 수정할것
        for i in range(len(t_candidate_y_pos)):
            if t_candidate_y_pos[i] == max_y_coordinate[0] or t_candidate_y_pos[i] == max_y_coordinate[0] + 5 or \
                t_candidate_y_pos[i] == max_y_coordinate[0]- 5:
                size_category_collections.append(candidate_y_index[i])

        for i in range(len(size_category_collections)):
            print(size_category_collections[i], "size",len(size_category_collections) )
        
        self.is_same_column(size_category_collections)

        # return candidate_y_index

    def is_same_column(self, size_category_name):

        for name in size_category_name:
            print("hi", name)
        
    #     # standard_index = 0
       
        # for i in range(len(self.data_list)):
        #     for j in range(len(size_category_name)):
        #         if self.data_list[i][0] == size_category_name[j]:
        #             standard_index = i
        #             print(size_category_name[j])
        #             break;

        # print(size_category_name , "is")

        same_column_index = []

        for i in range(len(size_category_name)):

            temp = self.is_valid_location(size_category_name[i])
            same_column_index = temp

        # self.is_one_word(same_column_index)

        # for i in range(len(same_column_index)):
        #     print(same_column_index[i].text)
        
        # self.check_data_in_sizetable(same_column_index)

        # same_column_data = []
        # for i in range(len(same_column_index)):
        #     # print(self.data_list[same_column_index[i]][0])
        #     if(size_category_name == "사이즈"):
        #         same_column_data.append(same_column_index[i])
        #     else:
        #         same_column_data.append(same_column_index[i].text)


        #     # if i == 0:
        #     #     same_column_data.append(same_column_index[i].text)
        #     #     # print(self.data_list[same_column_index[i]][0])

        #     # #의미 없는 숫자 누락, 예를 들면 수치와 완전히 무관하게 커진 숫자 혹은 작은 숫자. 
        #     # else:
        #     #     if self.string_to_number(same_column_index[i].text) >= self.string_to_number(same_column_index[i-1].text) \
        #     #     and self.string_to_number(same_column_index[i].text) < self.string_to_number(same_column_index[i-1].text) + 10:
        #     #         # print("correct : " , self.data_list[same_column_index[i]][0])
        #     #         same_column_data.append(same_column_index[i].text)


        # # for i in range(len(same_column_data)):
        # #     print(same_column_data[i])

        
        # return same_column_data

    def string_to_number(self, string):
        try:
            return int(string)
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

            if temp_y_center > c_y_center and abs(c_x_center - temp_x_center) <= 20 \
                and self.is_digit(data[0].replace(',', '.')):
                    index_container = Text.Text()
                    index_container.index = i
                    index_container.text = data[0].replace(',', '.')
                    temp.append(index_container)

        if len(temp) > 1:
            trimmed_index = len(temp)
            for ii, elem in enumerate(temp):
                if ii > 0 and self.data_list[temp[ii].index][2].y_pos - self.data_list[temp[ii-1].index][2].y_pos > 200:
                    trimmed_index = ii
                    temp = temp[:trimmed_index]
                    break
        
        # temp = temp[:trimmed_index]
        
        if len(temp) > 1:
            print("category : " , self.data_list[index][0])
            print([x.text for x in temp])
            return temp

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