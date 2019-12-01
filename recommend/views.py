from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from crawling.models import Category
from clothes.models import Product, Outer, Top, Skirt, Pants, Ops
from clothes.serializer import ProductSerializer, OpsSerializer, OuterSerializer, TopSerializer, SkirtSerializer, PantsSerializer
from rest_framework.decorators import action
from django.views.generic import ListView, DetailView
from django.apps import apps
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import extratorr
import category
import operator
import numpy as np
from datetime import *
import arrow
from urllib.parse import unquote


def recommend_main(request):
    query = Pants.objects.all().values()[5]
    query = query['date']
    query = query.strftime("%Y-%m-%d") 
    return render(request, 'recommend/sizerecommend.html', {'query':query})


def error_calc(parsedkey_list, parsedvalue_list, storedvalue_list):
    error_dic = {}
    chosen = {}
    reco = {}
    cnt = 0
    for dic in parsedvalue_list:
        item = []
        item_re = []
        dic_list = list(dic.values())
        for c_li in range(len(storedvalue_list)):
            for d_li in range(len(dic_list)):
                if c_li == d_li:
                    item.append(abs(float(storedvalue_list[c_li]) - float(dic_list[d_li])))
                    item_re.append((float(storedvalue_list[c_li]) - float(dic_list[d_li])))
                    break
        chosen[parsedkey_list[cnt]] = {name: value for name, value in zip(list(dic.keys()),item_re)}
        error_dic[parsedkey_list[cnt]] = sum(item)
        cnt += 1
    i = sorted(error_dic.items(), key=lambda x: x[1])
    var = i[0][1]
    cnt = 0
    for re_item in i:
        if re_item[1] == var:
            reco[i[cnt][0]] = chosen[i[cnt][0]]
        cnt += 1
    return reco

def trend_recommend(request):
    if request.method == 'GET':
        current_url = unquote(request.GET['url_send'])
        category_url = unquote(request.GET['category_url'])
        fit = request.GET['fit']
        cate = category.category_parse(category_url)
        url_parsed, key_set, size_data_all, thumbnail_temp = extratorr.parse(0, cate, current_url, category_url)
        #key_set = list(size_data_all.keys())
        value_set = list(size_data_all.values())  #딕셔너리 리스트
        query = Category.objects.filter(category=cate).first().category
        clothes_info = apps.get_model('clothes', query)
        clothes_info = clothes_info.objects.filter(user=request.user, fit=fit).order_by('id').values()
    
        parsed = list(value_set[0].keys()) #허리, 총장, 밑위 등
        mydate = datetime.today()
        mydate_trans = mydate.strftime("%Y-%m-%d")
        first = clothes_info[0]
        firstdate = first['date'].strftime("%Y-%m-%d")
        calc_list = []

        for key in parsed:  #허리
            date_list = []
            size_list = []
            for i in range(len(clothes_info)):
                query_obj = clothes_info[i]
                query = query_obj['date']
                query = query.strftime("%Y-%m-%d")
                date1 = arrow.get(firstdate)   
                date2 = arrow.get(query)
                difference = (date2 - date1).days
                for k, vl in query_obj.items():
                    if k == key:
                        size_list.append(vl)
                        date_list.append(difference)
        
            p = np.polyfit(date_list, size_list, 4)
            day = (arrow.get(mydate_trans) - arrow.get(firstdate)).days
            predict = np.polyval(p, day)
       
            calc_list.append(round(predict,2))
        reco = error_calc(key_set, value_set, calc_list)
        if len(reco) == 1:
            context = {'reco': reco}
            return JsonResponse(context)          
        else:
            if fit == "보통핏":
                context = {'reco': reco[list(reco.keys())[0]]}
                return JsonResponse(context)

            else:
                context = {'reco': reco[list(reco.keys())[-1]]}
                return JsonResponse(context)


def recent_recommend(request):  #기본 추천 - 절대값 결과 두개 일 때, 저장된 핏이 보통이면 작은거 추천, 저장된 핏이 오버면 둘 중에 큰거 추천하기
    if request.method == 'GET':
        current_url = unquote(request.GET['url_send'])
        category_url = unquote(request.GET['category_url'])
        fit = request.GET['fit']
        cate = category.category_parse(category_url)
        url_parsed, key_set, size_data_all, thumbnail_temp = extratorr.parse(0, cate, current_url, category_url)

        #key_set = list(size_data_all.keys())
        value_set = list(size_data_all.values())  #딕셔너리 리스트
        query = Category.objects.filter(category=cate).first().category
        clothes_info = apps.get_model('clothes', query)
        clothes_info = clothes_info.objects.filter(user=request.user, fit=fit).order_by('-id').values()[0]
        calc_keys = []
        calc_list = []
        for k, vl in clothes_info.items():
            if k in list(value_set[0].keys()):
                calc_keys.append(k)
                calc_list.append(vl)
        
        reco = error_calc(key_set, value_set, calc_list)
        if len(reco) == 1:
            context = {'reco': reco, 'category':cate}
            return JsonResponse(context)          
        else:
            if fit == "보통핏":
                context = {'reco': reco[list(reco.keys())[0]], 'category':cate}
                return JsonResponse(context)

            else:
                context = {'reco': reco[list(reco.keys())[-1]], 'category':cate}
                return JsonResponse(context)

def all_list(request):
    if request.method == 'GET':
        current_url = unquote(request.GET['url_send'])
        category_url = unquote(request.GET['category_url'])
        fit = request.GET['fit']
        cate = category.category_parse(category_url)
        url_parsed, key_set, size_data_all, thumbnail_temp = extratorr.parse(0, cate,current_url, category_url)
        #key_set = list(size_data_all.keys())
        value_set = list(size_data_all.values())  #딕셔너리 리스트
        query = Category.objects.filter(category=cate).first().category
        clothes_info = apps.get_model('clothes', query)
        clothes_info = list(clothes_info.objects.all().filter(user=request.user, fit=fit).order_by('-id').values())
        calc_list = []
        date_list = []
        thumburl_list = []
        res = []
        for cnt in range(len(clothes_info)):
            calc_item = []
            for k, vl in clothes_info[cnt].items():
                if k in list(value_set[0].keys()):
                    calc_item.append(vl)
            date = clothes_info[cnt]
            thumb = clothes_info[cnt]
            if thumb['thumbnail']:
                thumbnail = thumb['thumbnail']
            else:
                thumbnail = cate
            registerdate = date['date'].strftime("%Y-%m-%d")
            date_list.append(registerdate)
            thumburl_list.append(thumbnail)
            calc_list.append(calc_item)

        reco_dic = {}
        for i in range(len(calc_list)):
            reco = error_calc(key_set, value_set, calc_list[i])
            if len(reco) == 1:
                reco = reco
            else:
                if fit == "보통핏":
                    reco = reco[list(reco.keys())[0]]
                else:
                    reco = reco[list(reco.keys())[-1]]
            res.append(list(reco.values()))

        for ct in range(len(date_list)):
            reco_dic[ct] = [date_list[ct], calc_list[ct], res[ct], thumburl_list[ct]]
        context = {'reco_dic':reco_dic}
        return JsonResponse(context)

@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        jsondata = json.loads(request.body)
        category = jsondata['cate']
        fit = jsondata['fit']
        del_pk = jsondata['del_data']
        query = Category.objects.filter(category=category).first().category
        clothes_info = apps.get_model('clothes', query)
        clothes_id = list(clothes_info.objects.all().filter(user=request.user, fit=fit).order_by('-id').values())
        tmp = clothes_id[int(del_pk)]['id']
       
        clothes_info.objects.all().filter(user=request.user, fit=fit)[id==tmp].delete()
        
        context = {'success':"success"}
        return JsonResponse(context)

