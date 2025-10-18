from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    # Static categories - no need for database
    categories = ['Food', 'Transportation', 'Shopping', 'Entertainment', 
                  'Bills', 'Healthcare', 'Education', 'Other']
    
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    
    # Fix: Use get_or_create to handle missing UserPreference
    user_preference, created = UserPreference.objects.get_or_create(
        user=request.user,
        defaults={'currency': 'USD'}  # Default currency
    )
    currency = user_preference.currency
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    # Static categories - no need for database
    categories = ['Food', 'Transportation', 'Shopping', 'Entertainment', 
                  'Bills', 'Healthcare', 'Education', 'Other']
    
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)
        
        if not category:
            messages.error(request, 'Please select a category')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    # Static categories - no need for database
    categories = ['Food', 'Transportation', 'Shopping', 'Entertainment', 
                  'Bills', 'Healthcare', 'Education', 'Other']
    
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        if not category:
            messages.error(request, 'Please select a category')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
    # Get ALL expenses for testing
    expenses = Expense.objects.filter(owner=request.user)
    
    finalrep = {}
    
    # Get all unique categories
    for expense in expenses:
        category = expense.category
        amount = float(expense.amount)
        
        if category in finalrep:
            finalrep[category] += amount
        else:
            finalrep[category] = amount
    
    print(f"Total expenses: {expenses.count()}")
    print(f"Final report: {finalrep}")
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)    


def stats_view(request):
    return render(request, 'expenses/stats.html')