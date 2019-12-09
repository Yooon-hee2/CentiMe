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
import ssl

def get_image_url(url):
    html = urllib.request.urlopen(url)
    extracted = tldextract.extract(url)
    domain = "http://" + "{}.{}".format(extracted.domain, extracted.suffix)
    soup = BeautifulSoup(html, 'html.parser')
    eee = soup.find_all("img")
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
                image_url.append(address)

            except IndexError as e:
                print(e)
    return image_url


def url_to_image(url):
    context = ssl._create_unverified_context()
    resp = urllib.request.urlopen(url, context=context)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def image_list(image_url):
    image_list = []
    for i in image_url:
        try:
            image_temp = url_to_image(i)
            image_list.append(image_temp)
        except HTTPError as e:
            print(e)
        except cv2.error as e:
            print(e)
    return image_list


def preprocess(image):
    img = np.copy(image)
    blue_threshold = 255
    green_threshold = 255
    red_threshold = 255
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]
    thresholds = (image[:, :, 0] != bgr_threshold[0]) \
                 | (image[:, :, 1] != bgr_threshold[1]) \
                 | (image[:, :, 2] != bgr_threshold[2])
    img[thresholds] = [0, 0, 0]
    gray_image = ~img
    return gray_image


def dilate(gray_image):
    kernel = np.ones((7, 7), np.uint8)
    dilation_image = cv2.dilate(gray_image, kernel, iterations=6)
    return dilation_image


def canny(dilation_image):
    edge_image = cv2.Canny(np.asarray(dilation_image), 100, 200)
    return edge_image


def draw_boundingbox(edge_image, image):
    contours_dict = []
    boundingbox_image = np.copy(image)
    contours, hierarchy = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(boundingbox_image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
        contours_dict.append({'contour': contour, 'x': x, 'y': y, 'w': w, 'h': h, 'cx': x + (w / 2), 'cy': y + (h / 2)})
    #cv2.imwrite("boundingRect1.jpg", boundingbox_image)
    return contours_dict


# def temp_image(image):
#     height, width, channel = image.shape
#     temp_image = np.zeros((height, width, channel), dtype=np.uint8)
#     return temp_image


def possible_box(contours_dict):
    MIN_WIDTH, MIN_HEIGHT = 30, 30
    possible_contours = []
    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        if d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)
    return possible_contours


def draw_possible_contours(possible_contours, image):
    height, width, channel = image.shape
    temp_image = np.zeros((height, width, channel), dtype=np.uint8)
    for d in possible_contours:
        cv2.rectangle(temp_image, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=1)
    #cv2.imwrite("this is temp.jpg", temp_image)
    return temp_image


def crop_image(possible_contours, crop_list, image):
    count = 0
    for d in possible_contours:
        image_copy = np.copy(image)
        crop_image = image_copy[d['y']:d['y']+d['h'], d['x']:d['x']+d['w']]
        count += 1
        crop_list.append(crop_image)
    #    cv2.imwrite("crop image_" + str(count) + ".jpg", crop_image)
    #     cv2.rectangle(image, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(0, 0, 255),
    #                   thickness=2)
    # cv2.imwrite("crop imagedkdkkdd.jpg", image)
        # cv2.imshow('ccc', crop_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


# def resize_image(crop_list):
#     for i in crop_list:
#         cv2.imshow('resize', i)
#         cv2.waitKey(0)
#         resized_image = cv2.resize(i, (224, 224))
#
#         resize_list.append(resized_image)
#
#     return resize_list

def classification (url):
    list_of_image = image_list(get_image_url(url))
    crop_list = []
    resize_list = []
    # cv2.imshow('RE', list_of_image[0])
    # cv2.waitKey(0)]
    cnt = 0
    for get_list in list_of_image:
        image_origin = get_list
        row, col = image_origin.shape[:2]
        bottom = image_origin[row - 2:row, 0:col]
        bordersize = 20
        image = cv2.copyMakeBorder(image_origin, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                   borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        try:
            image_gray = preprocess(image)
            image_dilation = dilate(image_gray)
            image_edge = canny(image_dilation)
            contours_dict = draw_boundingbox(image_edge, image)
            possible_contours = possible_box(contours_dict)
            image_temp = draw_possible_contours(possible_contours, image)
            gray = cv2.cvtColor(image_temp, cv2.COLOR_RGB2GRAY)
            ret, dst = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            contours_dict1 = draw_boundingbox(dst, image)
            possible_contours1 = possible_box(contours_dict1)
            crop_image(possible_contours1, crop_list, image)
        except:
            pass
        #resize_image(crop_list)
        #print(resize_list)
        # cv2.imshow('crop', crop_list[cnt])
        # cnt += 1
    #print(len(crop_list))
    for i in crop_list:
        resized_image = cv2.resize(i, (224, 224))
        resize_list.append(resized_image)


    resize_list = np.array(resize_list)
    resize_list = resize_list.astype(float)/255
    model = load_model('./new_crop_VGGNet.h5')
    model._make_predict_function()
    prediction = model.predict(resize_list)

    table = []
    line = []
    cnt = 0
    for i in prediction:
        argmax = np.argmax(i)
        if argmax == 1:
            # print("line")
            # cv2.imshow('line', crop_list[cnt])
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            line.append(crop_list[cnt])
        elif argmax == 2:
            # print("table")
            # cv2.imshow('table', crop_list[cnt])
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            table.append(crop_list[cnt])
        cnt += 1

    return table, line
