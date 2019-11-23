from selenium import webdriver
from bs4 import BeautifulSoup
import requests as req
import re
import category


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
    size_call = []
    size_num = []
    size = ['XS','xs','S', 's', 'M', 'm', 'L', 'l', 'XL', 'xl', 'XXL', 'xxl']
    # 넘어온 리스트에서 중복된 문장 지우기
    content_list = orderedset(content_list)

    for i in content_list:
        mid_list.append(i.split('/') and i.replace("\\xa0", "") and i.split())

    # 수치, 항목 모두 다 떼고 리스트에 저장함. 인덱싱으로 필요 정보 따로 result에 옮겨 담기
    for k in mid_list:
        for j in size:
            if j in k:
                ary.append(k.index(j))
                size_call.append(j)

    for ins in range(len(ary)):
        if (ins == len(ary) - 1):
            size_num.append(k[ary[ins] + 1:])
        else:
            size_num.append(k[ary[ins] + 1:ary[ins + 1]]) #항목과 수치가 번갈아 나오지 않을때 사용
    
    
    result_list = [[0] for low in range(len(mid_list))]
    count = 0
    tmp = [0] * len(slist)
    
    for x in mid_list:
        for sl in slist:
            exitOuterLoop = False 
            for st in sl:
                sl = re.compile(st)
                for sh in x:
                    if sl.search(sh):
                        exitOuterLoop = True
                        store_id = x.index(sh)
                        if re.compile('[0-9]+').search(mid_list[count][store_id + 1]):
                            result_list[count].append(mid_list[count][store_id + 1])#size의 항목 다음번째 애를 result_list에 담아라
                        else:
                            tmp[store_id] = sh  #숫자가 아니면 tmp에 담아라
                        break
                if exitOuterLoop == True:
                    break
            if exitOuterLoop == False:
                result_list[count].append(0)
        result_list[count].insert(0, mid_list[count][0])
        count += 1
    
    alt = False
    for item in tmp:
        if item is not 0:
            alt = True
            break

    if alt == False:
        for key in result_list:
            del key[1]

        return result_list
    else:
        result_list = strange_ary(slist, size_num, tmp, size_call)
        print(result_list)
        return result_list

def strange_ary(slist, size_num, tmp, ary):
    result_list = [[0] for low in range(len(size_num))]
    for it in tmp:
        if it == 0:
            tmp.remove(it)
    
    for t in range(len(size_num)):
        for y in slist:
            exitOuterLoop = False 
            for y_tp in y:
                y = re.compile(y_tp)
                for x in range(len(tmp)):
                    if y.search(tmp[x]):
                        exitOuterLoop = True
                        result_list[t].append(size_num[t][x])
                        break
                if exitOuterLoop == True:
                    break
            if exitOuterLoop == False:
                result_list[t].append(0)
        result_list[t].insert(0, ary[t])

    for key in result_list:
        del key[1]
    
    return result_list


def textcrawling(str, fi_category):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    url = str
    response = req.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml", from_encoding='ANSI')
    dic_list = category.prepare_category(fi_category)
    search_list = prepare_index(category.prepare_category(fi_category))
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
    re_data = {}
    for item in result:
        re_data[item[0]] = {name: value for name, value in zip(dic_list, item[1:])}
    return re_data

# method for extracting thumbnail
def thumbnail_finder(categoryUrl, currentUrl):
    
    import requests
    import tldextract
    from urllib import parse
    from urllib.parse import urljoin

    def get_image_url(url):
        extracted = tldextract.extract(url)
        domain = "http://" + "{}.{}".format(extracted.domain, extracted.suffix)
        final_url = ""
        try:
            if url[0] == '/':
                url = parse.quote(url)
                if url[1] == '/':
                    address = "https:" + url
                else:
                    address = domain + url

            else:
                    address = url
            final_url = address
        except IndexError as e:
            print(e)
        return final_url

    # url = 'http://daybin.co.kr/product/list.html?cate_no=77'
    # purl = 'http://daybin.co.kr/product/detail.html?product_no=5429&cate_no=77&display_group=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    req = requests.get(categoryUrl, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    image_candidates = soup('a')
    for image in image_candidates:
        if urljoin(purl,image.get('href')) == currentUrl:
            if image.img:
                print(get_image_url(image.img['src']))
                return get_image_url(image.img['src'])
# if __name__ == '__main__':
#     #textcrawling("http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2", "PANTS")
#     textcrawling("https://store.musinsa.com/app/product/detail/957880/0", "PANTS")
# thumbnail_finder()