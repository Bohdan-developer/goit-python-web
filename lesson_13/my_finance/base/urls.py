from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path("about", views.about, name='about'),
    path("report", views.report, name='report'),
    path("add", views.add, name='add'),
    path("report/<str:filter_btn>", views.report_filter, name="report_filter"),
    path("report/<str:flag>", views.daterange_filter, name="daterange_filter")
]
