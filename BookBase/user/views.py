from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from .models import Sell
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return HttpResponseRedirect('/user/login/')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'registration/signup.html',{
                                            'user_form':user_form,
                                            'profile_form':profile_form,
                                            'registered':registered
                                        })
def sell(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author =request.POST.get('author')
        description =request.POST.get('desc')
        price =request.POST.get('price')
        sellModel = Sell()
        sellModel.title = title
        sellModel.author = author
        sellModel.description = description
        sellModel.price = price
        sellModel.user_id = request.user

        sellModel.save()
        context = {'title':title,'author':author,'desc':description,'price':price}
        print(str(title)+str(author)+str(description)+str(price))

        return render(request,'sell.html', context)
    else:
        return render(request, 'sell.html', {})