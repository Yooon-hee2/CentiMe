from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def done(request):
    context={'message':"ok"}
    return JsonResponse(context)