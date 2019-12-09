from bs4 import BeautifulSoup
import requests as req
import re
import category


def prepare_index(list):
    index_dic = {'bust': ['가슴+', '품'], 'shoulder': ['어깨+'], 'armhole': ['암홀+', '팔통+', '팔단면', '소매품'],
                 'sleeve': ['소매길이', '팔+', '전체팔길이', '팔길이', '팔소매'], 'sleevewidth': ['소매단면', '팔둘레', '팔뚝단면', '팔단면', '팔통', '소매너비', '소매둘레'],
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

def text_num_split(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return [item[:index], item[index:]]

def split_word(slist, content_list):
    mid_list = []
    ary = []
    size_call = []
    size_num = []
    size = ['XS', 'xs', 'S', 's', 'M', 'm', 'L', 'l', 'XL', 'xl', 'XXL', 'xxl', 'one', 'ONE', 'free', 'FREE']
    # 넘어온 리스트에서 중복된 문장 지우기
    content_list = orderedset(content_list)
   
    for i in range(len(content_list)):
        text = re.sub('[=+,#/\?:^$@*\"※~&%ㆍ!』│\\‘|\(\)\[\]\<\>`\'…》cm]', '', content_list[i])
        # print("text ; ", text)
        mid_list.append(text.replace('/', "") and text.replace('\\xa0', '') and text.split())
    #print(mid_list)
    trash = []
    safe = []
    check = 0
    for check in range(len(mid_list)):
        cnt = 0
        for check_list in slist:    
            out = False
            for check_item in check_list:
                for sh_item in mid_list[check]:
                    if re.compile(check_item).search(sh_item):
                        cnt += 1
                        out = True
                        break
                if out == True:
                    break
            if cnt >= 3:
                safe.append(mid_list[check])
                break
        if cnt < 3:
            trash.append(mid_list[check])           
    mid_list = safe
    re_safe = []
    for m_list in range(len(mid_list)):
        count = 0
        for it in mid_list[m_list]:
            if re.compile('[0-9]+').search(it):
                count += 1
        if count >= 4:
            re_safe.append(mid_list[m_list])
        
    mid_list = re_safe
    #print(mid_list)
    if mid_list:
        if len(mid_list[0][2])>3:
            for item in mid_list:
                for st in item[1:]:
                    #print(st)
                    if re.findall("\d+", st):
                        num = re.findall("\d+", st)
                        item.insert(item.index(st) + 1, str(num[0]))
    #print(mid_list)


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
            size_num.append(k[ary[ins] + 1:ary[ins + 1]])  # 항목과 수치가 번갈아 나오지 않을때 사용

    result_list = [[0] for low in range(len(mid_list))]
    count = 0
    # tmp = [0] * len(slist) ####여기를 바꿨어요
    tmp = []
    if mid_list:
        tmp2 = [0] * len(mid_list[0])
    for x in mid_list:
        for sl in slist:
            exitOuterLoop = False
            for st in sl:
                sl = re.compile(st)
                for sh in x:
                    if sl.search(sh):
                        exitOuterLoop = True
                        store_id = x.index(sh)
                        try:
                            if re.compile('[0-9]+').search(mid_list[count][store_id + 1]):
                                result_list[count].append(mid_list[count][store_id + 1])  # size의 항목 다음번째 애를 result_list에 담아라
                            else:
                                # tmp[store_id] = sh  # 숫자가 아니면 tmp에 담아라 ###여기를 바꿨어요
                                tmp.append(sh)
                                tmp2[x.index(sh)] = sh
                            break
                        except IndexError:
                            pass
                if exitOuterLoop == True:
                    break
            if exitOuterLoop == False:
                result_list[count].append(0)
        result_list[count].insert(0, mid_list[count][0])
        # result_list[count].insert(0, size_call[count])
        count += 1
    #print(tmp2)
    alt = False
    for item in tmp:
        if item is not 0:
            alt = True
            break
    
    if alt == False:
        for key in result_list:
            del key[1]
        
        result_list = modify_result(result_list, size_call)
        return result_list
    else:
        result_list = strange_ary(slist, size_num, tmp, size_call)
        
        result_list = arrange_list(slist,tmp2,size_num, size_call)
        result_list = modify_result(result_list, size_call)
        #print(result_list)
        return result_list


def arrange_list(slist, tmp2, size_num, size_call):
    chg = []
    
    tmp2_ch = []
    for i in tmp2:
        if i != 0:
            tmp2_ch.append(i)
    
    for it in range(len(size_num)):
        line = []
        for i in size_num[it]:
            if re.findall("\d+", i):
                line.append(i)
        chg.append(line)
    
    
    
    result = [[0]* len(slist) for low in range(len(size_num))]
    re_li = [[0] * len(slist)]
    for i in range(len(size_num)):
        for item in range(len(slist)):
            for ditem in slist[item]:
                for itr in range(len(size_num)):
                    for it in range(len(tmp2_ch)):
                        if re.compile(ditem).search(tmp2_ch[it]):
                            #print(tmp2_ch[it])
                            result[itr][item] = chg[itr][it]

    for idx in range(len(result)):
        result[idx].insert(0, size_call[idx])
    return result               
                
    
def strange_ary(slist, size_num, tmp, ary):
    tmp_result = []
    result_list = [[0] for low in range(len(size_num))]

    for it in tmp:
        if it != 0:
            tmp_result.append(it)
    
    for t in range(len(size_num)):
        for y in slist:
            exitOuterLoop = False
            for y_tp in y:
                y = re.compile(y_tp)
                for x in range(len(tmp_result)):
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


def modify_result(result_list, size_call):
    del_list = []
    for i in range(len(result_list)):
        if result_list[i].count(0) > 2:
            del_list.append(i)
    for i in del_list:
        del result_list[i]
        i-=1
    for i in range(len(result_list)):
        for j in range(len(result_list[i])):
            if type(result_list[i][j]) == str:
                text = re.sub('[가-힣]+', '', result_list[i][j])
                result_list[i][j] = text

    if len(result_list) == 1:
            result_list[0][0] = 'one size'
    else:
        for i in range(len(result_list)):
            result_list[i][0] = size_call[i]
    #print(result_list)
    return result_list

def textcrawling(str, fi_category):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    url = str
    response = req.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml", from_encoding='ANSI')
    print(soup)
    dic_list = category.prepare_category(fi_category)
    search_list = prepare_index(category.prepare_category(fi_category))
    str_list = []
    
    query = ["기장", "총길이+", "총장+", "총기장+", "전체길이+", "총"]

    for i in query:
        tf = soup.find_all(text=re.compile(i))
        if (tf != None):
            for j in tf:
                k = j.parent.name
                if (k == "td" or k == "tr" or k == "th"):
                    try :
                        tf = soup.find(text=re.compile(j)).find_parent('table')
                    except AttributeError:
                        pass
                elif (j.parent.find_parent('td') or j.parent.find_parent('tr') or j.parent.find_parent('th')):
                    try :
                        tf = soup.find(text=re.compile(j)).find_parent('table')
                    except AttributeError:
                        pass
                elif (j.parent.find_parent('p')):
                    try :
                        tf = j.parent.find_parent('p')
                    except AttributeError:
                        pass
                    # tf = soup.find(text=re.compile(j)).find_parent('p')

                # elif (j.parent.find_parent('p').find_previous_sibling('p')):
                #     tf = soup.find(text=re.compile(j)).find_parent('p').find_previous_sibling('p')
                #     print(tf)
                else:
                    tf = j.parent

                str_list.append(tf.text)

    # print(remove_tag(''.joi,n(str_list))) 치수랑 수치랑 다른 곳에 있어서 잘 나뉘지 않을때 사용할 것
    # print("str_list : ", str_list)
    # print("search list  ; ", search_list)
    result = split_word(search_list, str_list)


    #print(result)
    re_data = {}
    for item in result:
        re_data[item[0]] = {name: value for name, value in zip(dic_list, item[1:])}
    
    return re_data

# method for extracting thumbnail 썸네일추출
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

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    req = requests.get(categoryUrl, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    image_candidates = soup('a')
    for image in image_candidates:
        if image.get('href') and urljoin(currentUrl,image.get('href')) == currentUrl:
            if image.img:
                return get_image_url(image.img['src'])




# if __name__ == '__main__':
#     #textcrawling("http://ba-on.com/product/detail.html?product_no=2011&cate_no=35&display_group=2", "PANTS")
#     textcrawling("https://store.musinsa.com/app/product/detail/957880/0", "PANTS")
    