from django.shortcuts import render, redirect
from .models import Costs, Income
from .forms import CostsForm, IncomeForm, DateRangeForm
from datetime import datetime, timedelta
# Create your views here.


def index(request):
    costs = Costs.objects.all()
    income = Income.objects.all()
    context = {"costs": costs, "income": income, "title": "Home"}
    return render(request, "base/index.html", context=context)


def about(request):
    context = {"title": "About"}
    return render(request, "base/about.html",  context=context)


def add(request):
    if request.method == "POST":
        form_costs = CostsForm(request.POST)
        form_income = IncomeForm(request.POST)
        if form_costs.is_valid():
            form_costs.save()
            return redirect("index")
        elif form_income.is_valid():
            form_income.save()
            return redirect("index")

    form_costs = CostsForm()
    form_income = IncomeForm()
    context = {"title": "Add", "form_costs": form_costs, "form_income": form_income}
    return render(request, "base/add.html", context=context)


def report(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start")
            end_date = form.cleaned_data.get("end")

    form = DateRangeForm()
    context = {"title": "Report", "form": form}

    return render(request, "base/report.html", context=context)


def report_filter(request, filter_btn):
    costs = Costs.objects.all()
    income = Income.objects.all()
    sum_costs = 0
    sum_income = 0
    day = datetime.now() - timedelta(minutes=60*24)
    month = datetime.now() - timedelta(minutes=60*24*30)

    if filter_btn == "all_costs":
        for el in costs:
            sum_costs += el.costs
        context = {"title": "Report", "costs": costs, "sum_costs": sum_costs, "filter": "All Time Expense Filter"}
        return render(request, "base/report.html", context=context)

    elif filter_btn == "all_income":
        for el in income:
            sum_income += el.income
        context = {"title": "Report", "income": income, "sum_income": sum_income, "filter": "All Time Income Filter"}
        return render(request, "base/report.html", context=context)

    elif filter_btn == "day_costs":
        costs = costs.filter(date__gte=day)
        for el in costs:
            sum_costs += el.costs
        context = {"title": "Report", "costs": costs, "sum_costs": sum_costs, "filter": "Daily expense filter"}
        return render(request, "base/report.html", context=context)

    elif filter_btn == "day_income":
        income = income.filter(date__gte=day)
        for el in income:
            sum_income += el.income
        context = {"title": "Report", "income": income, "sum_income": sum_income, "filter": "Daily income filter"}
        return render(request, "base/report.html", context=context)

    elif filter_btn == "month_costs":
        costs = costs.filter(date__gte=day)
        for el in costs:
            sum_costs += el.costs
        context = {"title": "Report", "costs": costs, "sum_costs": sum_costs, "filter": "Monthly expense filter"}
        return render(request, "base/report.html", context=context)

    elif filter_btn == "month_income":
        income = income.filter(date__gte=month)
        for el in income:
            sum_income += el.income
        context = {"title": "Report", "income": income, "sum_income": sum_income, "filter": "Monthly income filter"}
        return render(request, "base/report.html", context=context)


def daterange_filter(request, flag):
    # costs = Costs.objects.all()
    # income = Income.objects.all()
    # sum_costs = 0
    # sum_income = 0
    if request.method == "POST":
        if flag =="costs":
            print("OK")

    #     form = DateRangeForm(request.POST)
    #     if form.is_valid():
    #         start_date = form.cleaned_data.get("start")
    #         end_date = form.cleaned_data.get("end")





