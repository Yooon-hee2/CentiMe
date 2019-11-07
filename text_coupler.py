
import time


class TextCoupler():

    def __init__(self, data_list):
        
        self.prefix_words = [
            '총',
            '팔',
            '소매',
        ]

        self.suffix_words = [
            '길이',
            '기장',
        ]

        self.data_list = data_list

    def calculate_distance(self, prefix_index, suffix_index):

        def obtain_center(data):
            bounds = data[1:]
            x0 = bounds[0].x_pos
            y0 = bounds[0].y_pos
            x1 = bounds[2].x_pos
            y1 = bounds[2].y_pos
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2
            return x_center, y_center

        prefix_x, prefix_y = obtain_center(self.data_list[prefix_index])
        suffix_x, suffix_y = obtain_center(self.data_list[suffix_index])

        # print(prefix_x, prefix_y)
        # print(suffix_x, suffix_y)
        if abs(prefix_x - suffix_x) <= 40 and abs(prefix_y - suffix_y) <= 10:
            return True

        else:
            return False


    def concatenate(self):

        prefix_candidate = []
        suffix_candidate = []

        for i, text in enumerate(self.data_list):
            if text[0] in self.prefix_words:
                prefix_candidate.append(i)

            if text[0] in self.suffix_words:
                suffix_candidate.append(i)

        delete_index = []

        for prefix_word in prefix_candidate:
            for suffix_word in suffix_candidate:
                if self.calculate_distance(prefix_word, suffix_word):
                    self.data_list[prefix_word][0] = self.data_list[prefix_word][0] + self.data_list[suffix_word][0]
                    self.data_list[prefix_word][2] = self.data_list[suffix_word][2]
                    self.data_list[prefix_word][3] = self.data_list[suffix_word][3]
                    delete_index.append(suffix_word) 

        self.data_list = [x for i, x in enumerate(self.data_list) if i not in delete_index]

        
        return self.data_list

