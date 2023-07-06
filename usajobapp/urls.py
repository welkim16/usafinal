from django.urls import path,include
from rest_framework import routers
from .views import UsJobsViewSet,JobDetailViewSet,SalaryViewSet,CitiesViewSet,ImageViewSet

us = routers.DefaultRouter()
us.register(r'usajobs',UsJobsViewSet,basename='usajobTitle')
us.register(r'jobdetails', JobDetailViewSet)
us.register(r'jobsalary', SalaryViewSet)
us.register(r'listcities', CitiesViewSet)
us.register(r'listimages',ImageViewSet )

urlpatterns = [
    path('',include(us.urls))
]