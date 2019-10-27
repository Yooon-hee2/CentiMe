import urllib.request
from urllib import parse
import re
import tldextract
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import numpy as np
import urllib
import cv2
from keras.models import load_model

def get_image_url(url):
    #url = 'http://daybin.co.kr/product/detail.html?product_no=5348&cate_no=152&display_group=1'
    #url = 'http://unnilook.co.kr/product/%EB%8B%A4%EC%9E%89-pants/6116/category/119/display/2/'
    #url = 'https://cre-me.co.kr/product/%ED%81%AC%EB%9F%AC%EC%89%AC-%EC%9D%BC%EC%9E%90-%EB%8D%B0%EB%8B%98-%ED%8C%AC%EC%B8%A0/1143/category/42/display/1/'
    #url = 'http://maybnous.com/product/%EC%98%86-%EC%82%AC%EC%9D%B4%EB%93%9C%EB%B0%94-%EC%8A%A4%ED%82%A4%EB%8B%88%ED%8C%AC%EC%B8%A02colors%ED%95%98%EC%9D%B4%EC%9B%A8%EC%8A%A4%ED%8A%B8%ED%8A%B8%EC%9E%84%EC%AB%80%EC%AB%80%EC%8A%A4%ED%8C%90/3204/category/61/display/1/'
    #url = 'http://daldamore.co.kr/product/%EB%AA%A9%ED%8F%B4%EB%9D%BC-%ED%84%B0%ED%8B%80%EB%84%A5-%ED%8F%B4%EB%9D%BC%EB%8B%88%ED%8A%B8-%ED%8F%B4%EB%9D%BC%EB%84%A5-%EB%AA%A9%ED%8B%B0-%EC%8A%A4%ED%85%94%EB%9D%BC%ED%84%B0%ED%8B%80%EB%84%A5-%EC%9A%B855/5512/category/105/display/1/'
    #url = 'http://www.wvproject.co.kr/shop/shopdetail.html?branduid=996590&xcode=042&mcode=003&scode=&type=X&sort=manual&cur_code=042003&GfDT=bml8W10%3D'
    #url = 'https://heyboo.co.kr/product/detail.html?product_no=4406&cate_no=26&display_group=1'
    #url = 'http://black-up.kr/product/detail.html?product_no=14800&cate_no=1&display_group=4'
    #url = 'http://liveary.com/product/detail.html?product_no=6876&cate_no=44&display_group=2'
    #url = 'https://eurohomme.co.kr/product/detail.html?product_no=37634&cate_no=27&display_group=2'

    html = urllib.request.urlopen(url)
    extracted = tldextract.extract(url)
    domain = "http://" + "{}.{}".format(extracted.domain, extracted.suffix)
    #print(domain)
    encoding = html.headers['content-type'].split('charset=')[-1]
    #r = unicode(html.read(), encoding)
    soup = BeautifulSoup(html, 'html.parser')
    #regExp = re.compile('/([\w_-]+[.](jpg|png))(\w+)*$')
    #eee = soup.find_all("img", {"src":regExp})
    #print(eee)
    eee = soup.find_all("img")
    #print(eee)
    #file = open('image_url.txt','w')
    image_url = []

    for m in eee:
        string = m.get('src', 0)
        if string == 0:
            string = m.get('ec-data-src')
        img_src = string
        valid_img_src = re.findall('jpg|png', img_src)

        if valid_img_src:
            try:
                if string[0] == '/':
                    img_src = parse.quote(img_src)
                    if string[1] == '/':
                        address = "https:" + img_src
                    else:
                        address = domain + img_src

                else:
                    address = img_src

                ###print(address)
                image_url.append(address)
               # file.write(address + "\n")

            except IndexError as e:
                print(e)
    return image_url

###print(image_url)

from keras import backend as K
import tensorflow as tf

# def binary_focal_loss(gamma=2., alpha=.25):
#
#     def binary_focal_loss_fixed(y_true, y_pred):
#         """
#         :param y_true: A tensor of the same shape as `y_pred`
#         :param y_pred:  A tensor resulting from a sigmoid
#         :return: Output tensor.
#         """
#         pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
#         pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
#
#         epsilon = K.epsilon()
#         # clip to prevent NaN's and Inf's
#         pt_1 = K.clip(pt_1, epsilon, 1. - epsilon)
#         pt_0 = K.clip(pt_0, epsilon, 1. - epsilon)
#
#         return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1)) \
#                -K.sum((1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0))
#
#     return binary_focal_loss_fixed
#
#
# def categorical_focal_loss(gamma=2., alpha=.25):
#
#     def categorical_focal_loss_fixed(y_true, y_pred):
#         """
#         :param y_true: A tensor of the same shape as `y_pred`
#         :param y_pred: A tensor resulting from a softmax
#         :return: Output tensor.
#         """
#
#         # Scale predictions so that the class probas of each sample sum to 1
#         y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
#
#         # Clip the prediction value to prevent NaN's and Inf's
#         epsilon = K.epsilon()
#         y_pred = K.clip(y_pred, epsilon, 1. - epsilon)
#
#         # Calculate Cross Entropy
#         cross_entropy = -y_true * K.log(y_pred)
#
#         # Calculate Focal Loss
#         loss = alpha * K.pow(1 - y_pred, gamma) * cross_entropy
#
#         # Sum the losses in mini_batch
#         return K.sum(loss, axis=1)
#
#     return categorical_focal_loss_fixed

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

def true_image(image_url):
    X = []
    error_num = 0
    for i in image_url:
        try:
            image_temp = url_to_image(i)
            ###print("성공")
            resized_image = cv2.resize(image_temp, (224, 224))
            #resized_image = cv2.resize(image_temp, (150, 150))
            X.append(resized_image)

        except HTTPError as e:
            print(e)
            error_num += 1
        except cv2.error as e:
            print(e)

    X = np.array(X)
    X = X.astype(float)/255
    model = load_model('newVGGNet.h5')
    #model = load_model('newDenseNet1.h5',custom_objects={'categorical_focal_loss_fixed': categorical_focal_loss})
    prediction = model.predict(X)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    result = []
    cnt = 0
    for i in prediction:
        if i >= 0.5:
            ###print("True")
            result.append(image_url[cnt])
            # cv2.imshow('RE', X[cnt])
            # cv2.waitKey()
            # cv2.destroyAllWindows()
        # else :
        #     print("False")
        cnt += 1

    #print(result)
    return result

#true_image(get_image_url())