from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def login(request):
    return render(request, 'login/login.html')
    # context = {'url' : 'C:/Users/yoonhee/Desktop/centime/CentiMe/login/templates/login/login.html'}
    # return JsonResponse(context)

def done(request):
    #context={'message':"ok"}
    #return JsonResponse(context)
    return render(request, 'login/done.html')
#def check_login(request):

def check_login(request):
    if request.user.is_anonymous:
        context = {'message' : "anonymous"}
        return JsonResponse(context)

    else:
        context = {'message' : 'already logined'}
        return JsonResponse(context)
