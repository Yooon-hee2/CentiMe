from bs4 import BeautifulSoup
import requests as req
import re

searching_dic = {'OUTER': ['아우터', 'OUTER', '자켓', '코트', '가디건', 'KNIT', 'CARDIGAN', 'KNIT & CARDIGAN'],
                     'TOP': ['TOP', 'top', 'KNIT', 'knit', '상의', '탑', 'SHIRTS', 'BLOUSE','셔츠', '블라우스', 'BLOUSE & SHIRTS'],
                     'SKIRT': ['SKIRT','스커트','skirt'],
                     'PANTS': ['BOTTOM', 'bottom', 'pants', 'PANTS', '바지', '하의','팬츠'],
                     'OPS': ['DRESS','드레스','dress','OPS','ops', '원피스']}  # 카테고리 딕셔너리 만들기
cate_dic = {'OUTER': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'TOP': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
                'SKIRT': ['waist', 'hip', 'hem', 'length'],
                'PANTS': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
                'OPS': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']}
def prepare_category(dic_val):
    for dic, val in searching_dic.items():
        for vl in val:
            if vl == dic_val:
                sh = dic
    # 카테고리 항목 딕셔너리
    # return cate_dic[sh]
    return cate_dic[sh]

def category_parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    #url = str
    # url = "https://m.ba-on.com/product/list.html?cate_no=35"
    response = req.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml", from_encoding='ANSI')
    category = soup.find(href=url)
    if category:
        if category.string:
            category = category.string
        else:
            trans = "".join(filter(str.isdigit, url))
            s_trans = "/product/list.html?cate_no=" + trans
            category = soup.find(href=s_trans).string

    else:
        domain = re.sub(r'(http(s)?:\/\/)([0-9a-zA-Z\-]+\.*)+[a-z0-9]{2,4}', '', url)
        category = soup.find(href=domain).string
        if not category:
            try :
                trans = filter(str.isdigit,str(domain))
                s_trans = "/product/list.html?cate_no=" + trans
                category = soup.find(href=s_trans).string

            except:
                title = soup.find('title')
                category = re.sub('[=+,#/\?:^$@*\"※~&%ㆍ!』│\\‘|\(\)\[\]\<\>`\'…》0-9a-zA-Z\-]', '', str(title))
                category = category.split()[0]
    
    for dic_key, val in searching_dic.items():
        for vl in val:
            if vl == category.upper():
                sh = dic_key
    return sh



