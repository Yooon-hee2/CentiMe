from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def done(request):
    return render(request,'login/done.html')

def check_login(request):
    if request.user.is_anonymous:
        context = {'message' : "anonymous"}
        return JsonResponse(context)

    else:
        context = {'message' : 'already logined'}
        return JsonResponse(context)
