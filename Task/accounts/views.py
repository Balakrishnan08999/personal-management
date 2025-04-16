from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, Category
from .forms import IncomeForm, ExpenseForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
        else:
            messages.error(request, 'Invalid credentials, please try again.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def home(request):
    return render(request, 'home.html')


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('view_incomes')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})

# View for adding expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('view_expenses')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

# View for listing all income entries
@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'view_incomes.html', {'incomes': incomes})

# View for listing all expense entries
@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'view_expenses.html', {'expenses': expenses})

# View for editing income
@login_required
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('view_incomes')
    else:
        form = IncomeForm(instance=income)
    
    return render(request, 'edit_income.html', {'form': form})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('view_expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form})

# View for deleting income
@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    income.delete()
    messages.success(request, 'Income deleted successfully!')
    return redirect('view_incomes')

# View for deleting expense
@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('view_expenses')