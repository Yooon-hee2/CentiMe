import SearchColumnData
import Jeans
import Dictionary


class SortSizeData:
    def __init__(self, category_num, search):
        self.category_num = category_num
        self.search = search

    def sort_by_category(self):
        if self.category_num == 4:
            self.sort_jeans_data()

    def sort_jeans_data(self):

        # for i in range(len(self.search.is_same_column("허리"))):
        #     jeans = Jeans.Jeans()
        #     jeans.set_size_into("S", self.search.is_same_column("허리")[i], self.search.is_same_column("엉덩이")[i],self.search.is_same_column("허벅지")[i],
        #                         self.search.is_same_column("밑단")[i], self.search.is_same_column("밑위")[i], self.search.is_same_column("기장")[i])
        #     jeans.print_size()

        print("총길이")
        self.search.is_same_column(Dictionary.index_dic['length'])
        print("허리")
        self.search.is_same_column(Dictionary.index_dic['waist'])
        print("엉덩이")
        self.search.is_same_column(Dictionary.index_dic['hip'])
        print("밑위")
        self.search.is_same_column(Dictionary.index_dic['crotch_rise'])
        print("허벅지")
        self.search.is_same_column(Dictionary.index_dic['thigh'])
        print("밑단")
        self.search.is_same_column(Dictionary.index_dic['hem'])
        # print("사이즈")
        # self.search.is_same_column("사이즈")


        # jeans = Jeans.Jeans()
        # jeans.set_size_into("S", self.search.is_same_column("허리")[0], self.search.is_same_column("엉덩이")[0],self.search.is_same_column("허벅지")[0],
        #                         self.search.is_same_column("밑단")[0], self.search.is_same_column("밑위")[0], self.search.is_same_column("총장")[0])
        # jeans.print_size()
        # jeans = Jeans.Jeans()
        # jeans.set_size_into("M", self.search.is_same_column("허리")[1], self.search.is_same_column("엉덩이")[1],self.search.is_same_column("허벅지")[1],
        #                         self.search.is_same_column("밑단")[1], self.search.is_same_column("밑위")[1], self.search.is_same_column("총장")[1])
        # jeans.print_size()
        # jeans = Jeans.Jeans()
        # jeans.set_size_into("L", self.search.is_same_column("허리")[2], self.search.is_same_column("엉덩이")[2],self.search.is_same_column("허벅지")[2],
        #                         self.search.is_same_column("밑단")[2], self.search.is_same_column("밑위")[2], self.search.is_same_column("총장")[2])
        # jeans.print_size()
        # jeans = Jeans.Jeans()
        # jeans.set_size_into("XL", self.search.is_same_column("허리")[3], self.search.is_same_column("엉덩이")[3],self.search.is_same_column("허벅지")[3],
        #                         self.search.is_same_column("밑단")[3], self.search.is_same_column("밑위")[3], self.search.is_same_column("총장")[3])
        # jeans.print_size()
