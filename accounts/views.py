from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.
def login_view(request):
 if request.method=="POST":
  username=request.POST.get("username")
  password=request.POST.get("password")
  remember_me=request.POST.get("remember_me")
  # print("login requestted")
  # print("data",request.POST)

  user=authenticate(request,username=username,password=password)
  if user is not None:
    login(request , user)
    if remember_me is None:
      request.session.set_expiry(0)
    
    return redirect ("table_view_url")
    

  else:
   
    messages.error(request ,"Invalid credentails")
    return redirect ("login_url")

  

 return render(request,'accounts/login.html')


def logout_view(request):
  logout(request)
  return redirect("login_url")
