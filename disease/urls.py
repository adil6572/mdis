from django.contrib import admin
from django.urls import path, include
from disease.views.malaria import malaria
from disease.views.pnemonia import pnemonia_view
from disease.views.index import index
from disease.views.Tumor import brain_tumor


urlpatterns = [
    path("", index,name="index"),
    path("malaria-prediction", malaria,name="malaria"),
    path("pnemonia-prediction", pnemonia_view,name="pnemonia"),
    path("tumor-prediction", brain_tumor,name="tumor"),
    path("contact", malaria,name="contact"),

]
