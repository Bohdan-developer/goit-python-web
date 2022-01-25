from .models import Costs, Income, DateRange

from django.forms import ModelForm, TextInput, DateTimeInput, NumberInput


class CostsForm(ModelForm):
    class Meta:
        model = Costs
        fields = ["category", "list", "costs", "date"]
        widgets = {
            "category": TextInput(attrs={"placeholder": "Category"}),
            "list": TextInput(attrs={"placeholder": "Description"}),
            "costs": NumberInput(attrs={"placeholder": "Price"}),
            "date": DateTimeInput(attrs={"type": "datetime-local"})
        }


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ["category", "list", "income", "date"]
        widgets = {
            "category": TextInput(attrs={"placeholder": "Category"}),
            "list": TextInput(attrs={"placeholder": "Description"}),
            "income": NumberInput(attrs={"placeholder": "Price"}),
            "date": DateTimeInput(attrs={"type": "datetime-local"})
        }


class DateRangeForm(ModelForm):
    class Meta:
        model = DateRange
        fields = ["start", "end"]
        widgets = {
            "start": DateTimeInput(attrs={"type": "datetime-local"}),
            "end": DateTimeInput(attrs={"type": "datetime-local"})
        }
