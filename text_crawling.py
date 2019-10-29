from selenium import webdriver
from bs4 import BeautifulSoup
import requests as req
import re


def prepare_category(dic_val):
    searching_dic = {'outer': ['아우터', 'OUTER', '자켓', '코트', '가디건'],
                     'top': [],
                     'skirt': [],
                     'pants': ['BOTTOM', 'PANTS', '바지', '하의'],
                     'ops': []}  # 카테고리 딕셔너리 만들기

    for dic, val in searching_dic.items():
        for vl in val:
            if vl == dic_val:
                sh = dic

    cate_dic = {'outer': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'top': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'skirt': ['waist', 'hip', 'hem', 'length'],
                'pants': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
                'ops': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']}
    # 카테고리 항목 딕셔너리
    # return cate_dic[sh]
    return cate_dic["pants"]


def prepare_index(list):
    index_dic = {'bust': ['가슴+', '품'], 'shoulder': ['어깨+'], 'armhole': ['암홀+', '팔통+', '팔단면', '소매품'],
                 'sleeve': ['소매+', '팔+', '전체팔길이'], 'sleevewidth': ['소매+', '팔둘레', '팔뚝단면', '팔단면'],
                 'length': ['총장+', '총길이+', '총+', '전체길이', '기장'],
                 'waist': ['허리+'], 'hip': ['엉덩이+', '힙+'], 'hem': ['밑단+', '치마밑단', '바지밑단', '끝단'], 'crotch_rise': ['밑위+'],
                 'thigh': ['허벅지+']}
    # 항목별 포괄 단어 딕셔너리

    return ([index_dic[key] for key in list])


def remove_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)
    return cleantext


def orderedset(list):
    or_set = set()
    res = []
    for e in list:
        if e not in or_set:
            res.append(e)
            or_set.add(e)

    return res


def split_word(slist, content_list):
    mid_list = []
    ary = []
    size_num = []
    size = ['S', 's', 'M', 'm', 'L', 'l', 'XL', 'xl', 'XXL', 'xxl']
    # 넘어온 리스트에서 중복된 문장 지우기
    content_list = orderedset(content_list)

    for i in content_list:
        mid_list.append(i.split('/') and i.replace("\\xa0", "") and i.split())

    # 수치, 항목 모두 다 떼고 리스트에 저장함. 인덱싱으로 필요 정보 따로 result에 옮겨 담기

    for k in mid_list:
        for j in size:
            if j in k:
                ary.append(k.index(j))

    for ins in range(len(ary)):
        if (ins == len(ary) - 1):
            size_num.append(k[ary[ins] + 1:])
        else:
            size_num.append(k[ary[ins] + 1:ary[ins + 1]])

    result_list = [[0] for low in range(len(mid_list))]
    count = 0
    tmp = [0] * len(slist)
    for x in mid_list:
        for sl in slist:
            for st in sl:
                sl = re.compile(st)
                for sh in x:
                    if sl.search(sh):
                        store_id = x.index(sh)
                        if re.compile('[0-9]+').search(mid_list[count][store_id + 1]):
                            result_list[count].append(mid_list[count][store_id + 1])
                        else:
                            tmp[store_id] = sh
        result_list[count].insert(0, mid_list[count][0])
        count += 1
    if result_list:
        for line in result_list:
            if line[-1] == line[-2]:
                line.remove(line[-1])

        for key in result_list:
            for kd in key:
                if kd == 0:
                    key.remove(kd)

        return result_list
    else:
        result_list = strange_ary(slist, size_num, tmp)
        return result_list


def strange_ary(slist, size_num, tmp):
    result_list = [[0] for low in range(len(size_num))]
    for t in range(len(size_num)):
        for y in slist:
            for y_tp in y:
                y = re.compile(y_tp)
                for x in range(len(tmp)):
                    if tmp[x] != 0:
                        if y.search(tmp[x]):
                            result_list[t].append(size_num[t][x - 1])

                break
    for key in result_list:
        for kd in key:
            if kd == 0:
                key.remove(kd)
    return result_list


def textcrawling(str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    url = str
    response = req.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml", from_encoding='ANSI')

    # category = soup.find(href=url)
    # if category:
    #     category = category.string
    # else:
    #     domain = re.sub(r'(http(S)?:\/\/)([0-9a-zA-Z\-]+\.*)+[a-z0-9]{2,4}','',url)
    #     category = soup.find(href=domain).string

    search_list = prepare_index(prepare_category("pants"))
    str_list = []
    query = ["기장", "총길이+", "총장+", "총기장+", "전체길이+"]
    for i in query:
        tf = soup.find_all(text=re.compile(i))
        if (tf != None):
            for j in tf:
                k = j.parent.name
                if (k == "td" or k == "tr" or k == "th"):
                    tf = soup.find(text=re.compile(j)).find_parent('table')
                elif (j.parent.find_parent('td') or j.parent.find_parent('tr') or j.parent.find_parent('th')):
                    tf = soup.find(text=re.compile(j)).find_parent('table')
                elif (j.parent.find_parent('p')):
                    tf = soup.find(text=re.compile(j)).find_parent('p')
                # elif (j.parent.find_parent('p').find_previous_sibling('p')):
                #     tf = soup.find(text=re.compile(j)).find_parent('p').find_previous_sibling('p')
                #     print(tf)
                else:
                    tf = j.parent

                str_list.append(tf.text)
    # print(remove_tag(''.join(str_list))) 치수랑 수치랑 다른 곳에 있어서 잘 나뉘지 않을때 사용할 것

    result = split_word(search_list, str_list)
    print(search_list)
    return result
