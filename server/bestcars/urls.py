from django.contrib import admin
from django.urls import path,include
from cars.views import home
urlpatterns=[path("admin/",admin.site.urls),path("",home),path("",include("cars.urls"))]
