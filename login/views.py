from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def login(request):
    return render(request, 'login/login.html')
    # context = {'url' : 'C:/Users/yoonhee/Desktop/centime/CentiMe/login/templates/login/login.html'}
    # return JsonResponse(context)

def done(request):
    context={'message':"ok"}
    return JsonResponse(context)

#def check_login(request):

