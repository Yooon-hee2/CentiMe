
from collections import Counter

class TextSizeFinder():

    def __init__(self, category_type, data_list):
        self.data_list = data_list
        self.category_type = category_type

    def is_digit(self, str):
        try:
            tmp = float(str)
            if tmp > 5 :
                return True
        except ValueError:
            return False

    def find_category_in_size_image(self):

        ocr_dict = { 'length': ['총길이', '총장', '총기장', '전체길이'], 'bust': ['가슴', '가슴단면' '품'],  'shoulder': ['어깨', '어깨단면'], 'armhole': ['암홀', '팔통', '암홀단면'],
                 'waist': ['허리단면'], 'hip': ['엉덩이', '힙단면'], 'hem': ['밑단', '끝단', '밑폭', '발목'], 'crotch_rise': ['밑위'],
                'sleeve': ['소매길이', '팔', '팔길이'], 'sleevewidth': ['소매', '팔둘레', '팔뚝단면', '팔단면'], 
                 'thigh': ['허벅지', '허벅지단면']}
    
        candidate_y_pos = []
        candidate_y_index = []

        for i, text in enumerate(self.data_list):
            for category_list in ocr_dict.values():
                for category in category_list:
                     if text[0] == category:
                        candidate_y_index.append(i)
                        candidate_y_pos.append((text[1].y_pos + text[3].y_pos)/2)
                        break

        if (len(candidate_y_pos) < 4):
            #print("it's not image about size text")
            return False

        t_candidate_y_pos = [int(x // 6 * 6) for x in candidate_y_pos]

        y_counter = Counter(t_candidate_y_pos)
        y_value_group = []

        for counter_item in y_counter.items():
            if counter_item[1] > 3:
                y_value_group.append(counter_item[0])

        size_category_collections = {}
        size_category_order = []

        for size_group in y_value_group:
            y_pos_list = []
            temp_size_category_order=[]
            for index, y_pos in enumerate(t_candidate_y_pos):
                if size_group == y_pos or size_group + 6 == y_pos or size_group - 6 == y_pos:
                    y_pos_list.append(candidate_y_index[index])
                    temp_size_category_order.append(self.data_list[candidate_y_index[index]][0])
            size_category_order.append(temp_size_category_order)
            size_category_collections[size_group] = y_pos_list

        
        size_data_list = []
        for group in size_category_collections.items():
            temp_size_data_list = []
            for i, data in enumerate(self.data_list):
                y_center = (data[1].y_pos + data[3].y_pos)/2
                data[0] = data[0].replace("cm", "")
                data[0] = data[0].replace("CM", "")
                data[0] = data[0].replace(',', '.')
                data[0] = data[0].replace('am', "")
                data[0] = data[0].replace('-', "")
                if group[0] == (y_center // 6 * 6) or  group[0] == (y_center // 6 * 6) + 6 or group[0] == (y_center // 6 * 6) - 6:
                    if self.is_digit(data[0]):
                        temp_size_data_list.append(data[0])
            size_data_list.append(temp_size_data_list)

        size_name = ['S', 'M', 'L', 'XL' , '2XL']

        dict_without_size = {}
        complete_size_dict = {}

        if self.category_type == 'OUTER' or self.category_type == 'TOP':
            dict_without_size = {'bust' : 0, 'shoulder' : 0, 'armhole' : 0, 'sleeve' : 0, 'sleevewidth' : 0, 'length' : 0}
        if self.category_type == 'SKIRT':
            dict_without_size = {'waist' : 0, 'hip' : 0, 'hem' : 0, 'length' : 0}
        if self.category_type == 'PANTS':
            dict_without_size = {'waist' : 0, 'hip' : 0, 'thigh' : 0, 'hem' : 0, 'crotch_rise' : 0, 'length' : 0}
        if self.category_type == 'OPS':
            dict_without_size = {'waist' : 0,'bust' : 0, 'shoulder' : 0, 'armhole' : 0, 'sleeve' : 0, 'sleevewidth' : 0, 'hip' : 0, 'length' : 0}

        if len(size_data_list) > 1:
            for j, size_list in enumerate(size_data_list):
                temp_dict = dict(dict_without_size)
                for jj, size in enumerate(size_list):
                    for category_title, category_name in ocr_dict.items():
                        for category in category_name:
                            if category == size_category_order[j][jj]:
                                temp_dict[category_title] = size
                complete_size_dict[size_name[j]] = temp_dict
        else:
            for n, size_list in enumerate(size_data_list):
                temp_dict = dict(dict_without_size)
                for m, size in enumerate(size_list):
                    for category_title, category_name in ocr_dict.items():
                        for category in category_name:
                            if category == size_category_order[n][m]:
                                temp_dict[category_title] = size
                complete_size_dict['FREE'] = temp_dict

        return complete_size_dict