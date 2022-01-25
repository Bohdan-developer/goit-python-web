from django.db import models


class Costs(models.Model):
    category = models.CharField(max_length=50)
    list = models.CharField(max_length=150)
    costs = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.category} - {self.list}: {self.costs}$, {self.date}"


class Income(models.Model):
    category = models.CharField(max_length=50)
    list = models.CharField(max_length=150)
    income = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.category} - {self.list}: {self.income}$, {self.date}"


class DateRange(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
