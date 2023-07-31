from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import UsJobsViewSet,JobDetailViewSet,SalaryViewSet,CitiesViewSet,ImageViewSet,LoginViewSet,UserViewSet,CustomTokenObtainPairView

us = routers.DefaultRouter()
us.register(r'usajobs',UsJobsViewSet,basename='usajobTitle')
us.register(r'jobdetails', JobDetailViewSet)
us.register(r'jobsalary', SalaryViewSet)
us.register(r'listcities', CitiesViewSet)
us.register(r'listimages',ImageViewSet )
us.register(r'login', LoginViewSet, basename='user-login')
us.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('',include(us.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]