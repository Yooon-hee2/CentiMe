import Dictionary
from collections import Counter

class TextSizeFinder():

    def __init__(self, data_list):
        self.data_list = data_list

    def is_digit(self, str):
        try:
            tmp = float(str)
            if tmp > 5 :
                return True
        except ValueError:
            return False

    def find_category_in_size_image(self):
    
        candidate_y_pos = []
        candidate_y_index = []

        for i, text in enumerate(self.data_list):
            for category_list in Dictionary.index_dict.values():
                for category in category_list:
                     if text[0] == category:
                        print(text[0])
                        candidate_y_index.append(i)
                        candidate_y_pos.append((text[1].y_pos + text[3].y_pos)/2)
                        break

        if (len(candidate_y_pos) < 4):
            print("it's not image about size")
            return False

        print(candidate_y_index)
        # for i in range(len(candidate_y_pos)):
        #     print(candidate_y_pos[i], "size : ", len(candidate_y_pos))

        t_candidate_y_pos = [int(x // 6 * 6) for x in candidate_y_pos]

        y_counter = Counter(t_candidate_y_pos)
        y_value_group = []

        for counter_item in y_counter.items():
            if counter_item[1] > 3:
                y_value_group.append(counter_item[0])

        print(y_counter)

        size_category_collections = {}
        size_category_order = []

        for size_group in y_value_group:
            y_pos_list = []
            for index, y_pos in enumerate(t_candidate_y_pos):
                if size_group == y_pos or size_group + 6 == y_pos or size_group - 6 == y_pos:
                    y_pos_list.append(candidate_y_index[index])
                    size_category_order.append(self.data_list[candidate_y_index[index]][0])
            size_category_collections[size_group] = y_pos_list

        print(size_category_collections)

        return self.extract_size_data(size_category_collections, size_category_order)

    def extract_size_data(self, size_collection, size_category_order):

        size_data_list = []
        for group in size_collection.items():
            for i, data in enumerate(self.data_list):
                y_center = (data[1].y_pos + data[3].y_pos)/2
                data[0] = data[0].replace("cm", "")
                data[0] = data[0].replace("CM", "")
                data[0] = data[0].replace(',', '.')
                data[0] = data[0].replace('am', "")
                data[0] = data[0].replace('-', "")
                if group[0] == (y_center // 6 * 6) or  group[0] == (y_center // 6 * 6) + 6 or group[0] == (y_center // 6 * 6) - 6:
                    if self.is_digit(data[0]):
                        size_data_list.append(data[0])

        print(size_data_list)

        complete_size_dict = {'waist' : [], 'hip' : [], 'thigh' : [], 'hem' : [], 'crotch_rise' : [], 'length' : []}

        size_name = ['S', 'M', 'L', 'XL' , '2XL']

        for j, category_order in enumerate(size_category_order):
            for category_title, category_name in Dictionary.index_dict.items():
                for category in category_name:
                    if category == category_order:
                            complete_size_dict[category_title].append(size_data_list[j])
    

        print(complete_size_dict)