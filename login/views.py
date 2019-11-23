from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def done(request):
    context={'message':"success"}
    # return render(request,'login/done.html'), JsonResponse(context)
    # return render(request,'login/done.html', {'message' : "success"})
    return render(request,'login/done.html')


#def check_login(request):

