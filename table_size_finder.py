from collections import Counter

class Text:
    def __init__(self):
            self.category = ""
            self.index = 0
            self.text = ""
            self.height = 0

class TableSizeFinder():
    
    def __init__(self, category_type, data_list):
        self.data_list = data_list
        self.size_list = []
        self.size_number_list = []
        self.category_type = category_type
        self.result = {}
        self.ocr_dict = { 'length': ['총길이', '총장', '총기장', '전체길이'], 'bust': ['가슴', '품'],  'shoulder': ['어깨'], 'armhole': ['암홀', '팔통'],
                 'waist': ['허리'], 'hip': ['엉덩이', '힙'], 'hem': ['밑단', '끝단', '밑폭', '발목'], 'crotch_rise': ['밑위'],
                'sleeve': ['소매', '팔', '팔길이'], 'sleevewidth': ['소매', '팔둘레', '팔뚝단면', '팔단면'], 
                 'thigh': ['허벅지']}

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
            for category_list in self.ocr_dict.values():
                for category in category_list:
                     if text[0] == category:
                        candidate_y_index.append(i)
                        candidate_y_pos.append((text[1].y_pos + text[3].y_pos)/2)
                        break


        t_candidate_y_pos = [int(x // 5 * 5) for x in candidate_y_pos]

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

        same_column_data = []
        size_num_by_category = []

        for i in range(len(size_category_collections)):
            temp, num_of_size, category_name = self.is_valid_location(size_category_collections[i])
            if len(temp) > 0:
                same_column_data.append(temp)
                size_num_by_category.append(num_of_size)

        self.size_list = same_column_data
        self.size_number_list = size_num_by_category
        self.sort_by_category()
       
        return self.result

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
        
        temp = []

        for i, data in enumerate(self.data_list):
            temp_x_center, temp_y_center = obtain_center(data)
            # print(data[0] , " : " , abs(c_x_center - temp_x_center))

            if temp_y_center > c_y_center and abs(c_x_center - temp_x_center) <= 35:
               
                data[0] = data[0].replace("cm", "")
                data[0] = data[0].replace("CM", "")
                data[0] = data[0].replace(',', '.')
                if self.is_digit(data[0]):
                    index_container = Text()
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

        return temp, len(temp), self.data_list[index][0]

    def sort_by_category(self):

        self.missing_data_finder()
        
        size_name = ['S', 'M', 'L', 'XL' , '2XL']
        
        complete_size_dict = {}

        # for yoonhee in range(len(self.size_list)):
        #     if self.size_list[yoonhee]:
        #         print(self.size_list[yoonhee][0].category)
        #         for jj in range(len(self.size_list[yoonhee])):
        #             print(self.size_list[yoonhee][jj].text)
        
        if self.category_type == 'OUTER' or self.category_type == 'TOP':
            dict_without_size = {'bust' : 0, 'shoulder' : 0, 'armhole' : 0, 'sleeve' : 0, 'sleevewidth' : 0, 'length' : 0}
        if self.category_type == 'SKIRT':
            dict_without_size = {'waist' : 0, 'hip' : 0, 'hem' : 0, 'length' : 0}
        if self.category_type == 'PANTS':
            dict_without_size = {'waist' : 0, 'hip' : 0, 'thigh' : 0, 'hem' : 0, 'crotch_rise' : 0, 'length' : 0}
        if self.category_type == 'OPS':
            dict_without_size = {'waist' : 0,'bust' : 0, 'shoulder' : 0, 'armhole' : 0, 'sleeve' : 0, 'sleevewidth' : 0, 'hip' : 0, 'length' : 0}

        if len(self.size_list[0]) > 1:
            for num in range(len(self.size_list[0])):
                dict_without_size = {}
                for n in range(len(self.size_list)):
                    for category_title, category_name in self.ocr_dict.items():
                        for category in category_name:
                            if category == self.size_list[n][num].category:
                                dict_without_size[category_title] = self.size_list[n][num].text
                complete_size_dict[size_name[num]] = dict_without_size
        else:
            dict_without_size = {}
            for n in range(len(self.size_list)):
                for category_title, category_name in self.ocr_dict.items():
                    for category in category_name:
                        if category == self.size_list[n][num].category:
                            dict_without_size[category_title] = self.size_list[n][num].text
            complete_size_dict['FREE'] = dict_without_size
        
        self.result = complete_size_dict

    def missing_data_finder(self):

        cnt = Counter(self.size_number_list)
        mode = cnt.most_common(1)
        # print("mode : " , mode)
        complete_size_category = 0
        # find category that size datas are missing
        for yoonhee in range(len(self.size_list)):
            if len(self.size_list[yoonhee]) == mode[0][0]: 
                complete_size_category = yoonhee
            elif len(self.size_list[yoonhee]) < mode[0][0]:
                self.add_missing_data(mode[0][0], yoonhee, complete_size_category, mode[0][0] - len(self.size_list[yoonhee]))


    def add_missing_data(self, maximum_size, missing_index, complete_index, missing_number):

        if missing_number == 0 or maximum_size == 1:
            return 0

        print("missing index : ", missing_index)
        temp = []

        for i, complete_y in enumerate(self.size_list[complete_index]):
            for j, missing_y in enumerate(self.size_list[missing_index]):
                if missing_y.height <= complete_y.height + 5 \
                    and missing_y.height >= complete_y.height - 5:
                    temp.append(i)
                    break

        temp_container = Text()
        temp_container.category = self.size_list[missing_index][0].category

        missing_index_in_category = 0
        
        for index,x in enumerate(temp):
            if index != x:
                missing_index_in_category = index
                break

        temp_container.height = self.size_list[complete_index][missing_index_in_category].height

        if missing_index_in_category == 0:
            if maximum_size == 2:
                temp_container.text = self.size_list[missing_index][1].text - 1
                self.size_list[missing_index].insert(0, temp_container)

            else:
                gap = self.size_list[missing_index][1].text - self.size_list[missing_index][0].text
                temp_container.text = self.size_list[missing_index][0].text - gap
                self.size_list[missing_index].insert(0, temp_container)

        elif missing_index_in_category == maximum_size - 1:
            if maximum_size == 2:
                temp_container.text = self.size_list[missing_index][0].text + 1
                self.size_list[missing_index].insert(1, temp_container)

            else:
                gap = self.size_list[missing_index][1].text - self.size_list[missing_index][0].text
                temp_container.text = self.size_list[missing_index][missing_index_in_category - 1].text + gap
                self.size_list[missing_index].insert(missing_index_in_category, temp_container)

        elif maximum_size > 2 and missing_index_in_category != 0 and missing_index_in_category != maximum_size - 1:
            temp_container.text = (self.size_list[missing_index][missing_index_in_category - 1].text + self.size_list[missing_index][missing_index_in_category + 1].text)/2
            self.size_list[missing_index].insert(missing_index_in_category, temp_container)


           