from jamostoolkit import JamosSeparator
import time


class TextRefiner():

    def __init__(self, data_list):
        self.words = [
            '허리',
            '엉덩이',
            '힙',
            '허벅지',
            '밑단',
            '밑위',
            '총기장',
            '총길이',
            '기장',
            '총장',
            '전체길이',
            '끝단',
            '총',
            '암홀'
        ]

        self.prefix_words = [
            '총',
            '팔',
            '소매',
            '전체'
        ]

        self.suffix_words = [
            '길이',
            '기장',
        ]

        self.labels = [self._seperate(word) for word in self.words]
        self.max_distance = 3
        self.origin = ""
        self.data_list = data_list


    def _seperate(self, s):
        self.origin = s
        jamos = JamosSeparator(s)
        jamos.run()
        return ''.join(jamos.get()).replace('_', '')

    # https://lovit.github.io/nlp/2018/08/28/levenshtein_hangle/
    # 이 구현체는 어절단위가 아닌 자모 단위로 edit distance를 계산
    def _obtain_dist(self, input, target):
        if len(input) < len(target):
            return self._obtain_dist(target, input)

        if len(input) == 0:
            return len(target)

        previous_row = range(len(target) + 1)
        for i, c1 in enumerate(input):
            current_row = [i + 1]
            for j, c2 in enumerate(target):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))

            previous_row = current_row
        return previous_row[-1]

    def typo_refiner(self, input):
        ret = self.words[0]
        seperated = self._seperate(input)
        # min_distance = len(seperated) + self.max_distance
        for i, label in enumerate(self.labels):
            dist = self._obtain_dist(seperated, label)
            if dist < 2:
                # min_distance = dist
                ret = self.words[i]
                return ret

            else:
                ret = self.origin
        return ret

        
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

        if abs(prefix_x - suffix_x) <= 40 and abs(prefix_y - suffix_y) <= 10:
            return True

        else:
            return False


    def concatenate(self):

        for m, index in enumerate(self.data_list):
            self.data_list[m][0] = self.typo_refiner(index[0])

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