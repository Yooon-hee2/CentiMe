from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from crawling.models import Category
from clothes.models import Product, Outer, Top, Skirt, Pants, Ops
from clothes.serializer import ProductSerializer, OpsSerializer, OuterSerializer, TopSerializer, SkirtSerializer, PantsSerializer
from rest_framework.decorators import action
from django.views.generic import ListView, DetailView
import parser
import category

def main(request):
    cate = category.category_parse()
    url_parsed, size_data_all = parser.parse(0, cate)
    return render(request, 'crawling/home.html', {'re_dic':size_data_all})
#########카테고리어찌담아올지 생각해############

def CrawlingStore(request):
    cate = category.category_parse()
    sel_fit = request.GET['fit']
    sel_size = request.GET['size']
    url_parsed, size, data_dic = parser.parse(sel_size, cate)  #입력된 사이즈의 정보들만 가져옴
    save_val = list(data_dic.values())
    
    if cate == 'OUTER':
        query = Category.objects.filter(category=cate).first()
        Outer.objects.create(url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=size, bust=save_val[0],
        shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5])
    elif cate == 'TOP':
        query = Category.objects.filter(category=cate).first()
        Top.objects.create(url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=size, bust=save_val[0],
        shoulder=save_val[1],armhole=save_val[2],sleeve=save_val[3], sleevewidth=save_val[4],length=save_val[5])
    elif cate == 'SKIRT':
        query = Category.objects.filter(category=cate).first()
        Skirt.objects.create(url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=size, waist=save_val[0],
        hip=save_val[1], hem=save_val[2], length=save_val[3])
    elif cate == 'PANTS':
        query = Category.objects.filter(category=cate).first()
        Pants.objects.create(url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=size, waist=save_val[0],
        hip=save_val[1], thigh=save_val[2], hem=save_val[3],crotch_rise=save_val[4],length=save_val[5]) 
    elif cate == 'OPS':
        query = Category.objects.filter(category=cate).first()
        Ops.objects.create(url = url_parsed, user = request.user, fit=sel_fit, feature=query, size=size, waist=save_val[0],
        shoulder=save_val[1], armhole=save_val[2], sleeve=save_val[3], sleevewidth=save_val[4], hip=save_val[5], length=save_val[6])

    return HttpResponseRedirect(reverse('crawling:main'))
      