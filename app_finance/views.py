from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db.models import Sum
import json


from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import matplotlib.pyplot as plt

from .forms import *




@csrf_exempt
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:

		form = CreateUserForm()	
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				
				group = Group.objects.get(name='customer')
				user.groups.add(group)

				messages.success(request, 'Account was created for '+ username)

				return redirect('login')

		context = {'form':form}
		return render(request, 'app_finance/register.html', context)

def loginPage(request):
	username = None
	if request.user.is_authenticated:
		username = request.user.customer
		return redirect('home')
	else:

		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or password incorrect.')

		context = {}
		return render(request, 'app_finance/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):


	return render(request, 'app_finance/user.html')



@login_required(login_url='login')
def homeView(request):
    items = Finance.objects.filter(customer=request.user).order_by(Cast('month', IntegerField())).reverse()

    if request.method == 'POST':
        form = FinanceForm(request.POST, request=request) 
        if form.is_valid():
            finance_obj = form.save(commit=False)
            finance_obj.customer = request.user
            finance_obj.save()
            return redirect('home')
    else:
        form = FinanceForm(request=request) 

    expenses = Finance.objects.filter(customer=request.user).values('category').annotate(total=Sum('price'))
    sums = {expense['category']: expense['total'] for expense in expenses}
    
    sums_json = json.dumps(sums) 

    context = {'form': form, 'items': items, 'sums': sums, 'sums_json': sums_json, 
    	'sums_saving': sums.get('Saving', 0),
        'sums_food': sums.get('Food', 0),
        'sums_bills': sums.get('Bills', 0),
        'sums_rent': sums.get('Rent', 0),
        'sums_extra': sums.get('Extra', 0),}
    return render(request, 'app_finance/home.html', context)

@login_required(login_url='login')
def deleteView(request, pk):
    finance_obj = get_object_or_404(Finance, pk=pk)

    if request.method == 'POST':
        finance_obj.delete()
        return redirect('home')

    context = {'object': finance_obj}
    return render(request, 'app_finance/delete.html', context)


