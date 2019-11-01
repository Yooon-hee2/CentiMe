class Jeans:
    def __init__(self):
        self.size = ""
        self.waist = 0
        self.hip = 0
        self.thigh = 0
        self.crotch = 0
        self.hem = 0
        self.length = 0

    def set_size_into(self,size, waist, hip, thigh, crotch, hem, length):
        self.size = size
        self.waist = waist
        self.hip = hip
        self.thigh = thigh
        self.crotch = crotch
        self.hem = hem
        self.length = length

    def print_size(self):
        print(['({},{},{},{},{},{},{})'.format(self.size, self.waist, self.hip, self.thigh, self.crotch, self.hem, self.length)])

