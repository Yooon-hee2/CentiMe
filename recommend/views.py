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
import json
import parser
import category
import operator


def recommend_main(request):
    return render(request, 'recommend/sizerecommend.html')

def recent_recommend(request):  #기본 추천 - 절대값 결과 두개 일 때, 저장된 핏이 보통이면 작은거 추천, 저장된 핏이 오버면 둘 중에 큰거 추천하기
    jsonrequest = {}
    responselist = {}
    jsondata = request.GET['fit']
    fit = jsondata
    cate = category.category_parse("https://m.ba-on.com/product/list.html?cate_no=35") #카테고리 파싱 및 js 캐시 저장 구현 필요 
    url_parsed, size_data_all = parser.parse(0, cate)
    key_set = list(size_data_all.keys())
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
    error_dic = {}
    chosen = {}
    reco = {}
    cnt = 0
    for dic in value_set:
        item = []
        item_re = []
        dic_list = list(dic.values())
        for c_li in range(len(calc_list)):
            for d_li in range(len(dic_list)):
                if c_li == d_li:
                    item.append(abs(calc_list[c_li] - float(dic_list[d_li])))
                    item_re.append((calc_list[c_li] - float(dic_list[d_li])))
                    break
        chosen[key_set[cnt]] = {name: value for name, value in zip(list(dic.keys()),item_re)}
        error_dic[key_set[cnt]] = sum(item)
        cnt += 1
    i = sorted(error_dic.items(), key=lambda x: x[1])
    var = i[0][1]
    cnt = 0
    for re_item in i:
        if re_item[1] == var:
            reco[i[cnt][0]] = chosen[i[cnt][0]]
        cnt += 1
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


class PantsRecommendListView(ListView):
    model = Pants
    template_name = 'recommend/sizerecommend.html'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = Outer.objects.filter(user=self.request.user)
        return queryset
