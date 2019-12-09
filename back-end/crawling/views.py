from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from crawling.models import Category
from clothes.models import Product, Outer, Top, Skirt, Pants, Ops
from clothes.serializer import ProductSerializer, OpsSerializer, OuterSerializer, TopSerializer, SkirtSerializer, PantsSerializer
from rest_framework.decorators import action
from django.views.generic import ListView, DetailView
import extratorr
import category
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from urllib.parse import unquote

def main(request):
    extracted_size_dict = {}
    url_parsed = ""
    thumbnail = ""
    size_name_list = {}
    cate = ""
    if request.method == 'GET':
        #url_data = json.loads( request.body)
        current_url = unquote(request.GET['url_send'])
        category_url = unquote(request.GET['category_url'])
        cate = category.category_parse(category_url)
        request.session['category'] = cate
        #url_parsed, size_data_all = extratorr.parse(0, cate, current_url, category_url)
        url_parsed, size_name_list, extracted_size_dict, thumbnail = extratorr.parse(0, cate, current_url, category_url)
        request.session['url'] = url_parsed
        request.session['thumbnail'] = thumbnail
        request.session['size_dict'] = extracted_size_dict
        context = {'re_dic':extracted_size_dict}
        return JsonResponse(context)


def cate(request):
    if request.method == 'GET':
        #url_data = json.loads( request.body)
        current_url = unquote(request.GET['url_send'])
        category_url = unquote(request.GET['category_url'])
        cate = category.category_parse(category_url)
        context = {'cate':cate}
        return JsonResponse(context)
         
#########카테고리어찌담아올지 생각해############
@csrf_exempt     
def PersonalStore(request): #추천할때 사이즈 없는걸로 쿼리해서 추천
    jsondata = {}       
    res = {}
    if request.method == 'POST':
        personal_data = json.loads(request.body)
        cate = personal_data['sel_category']
        data_dic = json.loads(personal_data['data'])
        save_val = list(data_dic.values())
        if cate == 'OUTER':
            query = Category.objects.filter(category=cate).first()
            Outer.objects.create(user = request.user, feature=query, bust=save_val[0],
            shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5], fit = save_val[6])
        elif cate == 'TOP':
            query = Category.objects.filter(category=cate).first()
            Top.objects.create(user = request.user, feature=query, bust=save_val[0],
            shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5], fit = save_val[6])
        elif cate == 'SKIRT':
            query = Category.objects.filter(category=cate).first()
            Skirt.objects.create(user = request.user, feature=query, waist=save_val[0],
            hip=save_val[1], hem=save_val[2], length=save_val[3], fit = save_val[4])
        elif cate == 'PANTS':
            query = Category.objects.filter(category=cate).first()
            Pants.objects.create(user = request.user, feature=query, waist=save_val[0],
            hip=save_val[1], thigh=save_val[2], hem=save_val[3],crotch_rise=save_val[4],length=save_val[5], fit = save_val[6]) 
        elif cate == 'OPS':
            query = Category.objects.filter(category=cate).first()
            Ops.objects.create(user = request.user, feature=query, waist=save_val[0],
            shoulder=save_val[1], armhole=save_val[2], sleeve=save_val[3], sleevewidth=save_val[4], hip=save_val[5], length=save_val[6], fit = save_val[7])
        
        res['result'] = 'Create post successful!'
        return JsonResponse(res)


@csrf_exempt
def CrawlingStore(request):
    response_data={}
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        sel_cate = unquote(jsondata['category_url'])
        sel_tab = unquote(jsondata['url_send'])
        sel_fit = jsondata['fit']
        sel_size = jsondata['size']
        cate = request.session['category']
        size_dic_temp = request.session['size_dict']
        size_dict = size_dic_temp[sel_size]
        thumbnail = request.session['thumbnail']
        url_parsed = request.session['url']
        save_val = list(size_dict.values())
        #url_parsed, size, data_dic, thumbnail = extratorr.parse(sel_size, cate, sel_tab, sel_cate)  #입력된 사이즈의 정보들만 가져옴

        if cate == 'OUTER':
            query = Category.objects.filter(category=cate).first()
            Outer.objects.create(thumbnail = thumbnail, url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=sel_size, bust=save_val[0],
            shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5])
        elif cate == 'TOP':
            query = Category.objects.filter(category=cate).first()
            Top.objects.create(thumbnail = thumbnail, url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=sel_size, bust=save_val[0],
            shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5])
        elif cate == 'SKIRT':
            query = Category.objects.filter(category=cate).first()
            Skirt.objects.create(thumbnail = thumbnail, url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=sel_size, waist=save_val[0],
            hip=save_val[1], hem=save_val[2], length=save_val[3])
        elif cate == 'PANTS':
            query = Category.objects.filter(category=cate).first()
            Pants.objects.create(thumbnail = thumbnail, url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=sel_size, waist=save_val[0],
            hip=save_val[1], thigh=save_val[2], hem=save_val[3],crotch_rise=save_val[4],length=save_val[5]) 
        elif cate == 'OPS':
            query = Category.objects.filter(category=cate).first()
            Ops.objects.create(thumbnail = thumbnail, url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=sel_size, waist=save_val[0],
            shoulder=save_val[1], armhole=save_val[2], sleeve=save_val[3], sleevewidth=save_val[4], hip=save_val[5], length=save_val[6])
        
        response_data['result'] = 'Create post successful!'
        return JsonResponse(response_data)
      