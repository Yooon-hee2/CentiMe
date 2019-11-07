# https://github.com/jybaek/jamos-toolkit
from jamostoolkit import JamosSeparator
import time


class TypoRefiner():

    def __init__(self):
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
            '끝단'
        ]
        self.labels = [self._seperate(word) for word in self.words]
        self.max_distance = 3
        self.origin = ""

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

    def __call__(self, input):
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
