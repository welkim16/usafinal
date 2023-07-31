import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.shortcuts import render
from selenium.common import TimeoutException
from rest_framework import viewsets
from rest_framework.response import Response
from .models import UsJobs, JobDetails, Salary, Cities, Images,User
from .serializers import UsJobSerializer, JobDtailSerializer, SalarySerializer, CitiesSerializer, ImageSerializer, UserSerializer

from rest_framework import viewsets,status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here
url = 'https://www.glassdoor.com/Job/united-states-all-jobs-SRCH_IL.0,13_IN1_KO14,17.htm?sortBy=date_desc'
#
driver = webdriver.Chrome()
driver.get(url)

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MainCol")))
time.sleep(2)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

list = soup.find_all('li', class_='react-job-listing css-108gl9c eigr9kq3')
for main in list:
        url1 = 'https://www.glassdoor.com'
        jb_title = main.find('div', class_='job-title mt-xsm').text.strip()
        jb_link = url1 + main.find('a', class_='d-flex justify-content-between p-std jobCard')['href']
        jb_campany = main.find('div', class_='job-search-8wag7x').text.strip()
        dr = main.find('div', class_='d-flex align-items-end ml-xsm listing-age')
        if dr:
            duration = dr.text.strip()
            current_date = datetime.now()
            if duration.endswith("h"):
                hours = int(duration.split("h")[0].strip())
                posted_date = current_date - timedelta(hours=hours)
            elif duration.endswith("d"):
                days = int(duration.split("d")[0].strip())
                posted_date = current_date - timedelta(days=days)
            elif duration == "30d":
                posted_date = current_date - timedelta(days=30)
            elif duration == "30d+":
                posted_date = current_date - timedelta(days=60)  # Assuming 60 days for "30d+"
            else:
                continue

        div_element = main.find('div', class_='d-flex job-search-1sohcmw')
        if div_element is not None:
            img_elements = div_element.find_all('img')
            for img_element in img_elements:
                img_src = img_element['src']
                if len(img_src) >= 2:
                    imgs_name = img_src

                    if not Images.objects.filter(image=imgs_name).exists():
                        new_img = Images(image=imgs_name)
                        new_img.save()
        else:
            continue


        job_cities = main.find('div', class_='location mt-xxsm').text.strip()
        if len(job_cities) >= 2:
            job_city_name = job_cities

            if not Cities.objects.filter(cities=job_city_name).exists():
                new_job_city = Cities(cities=job_city_name)
                new_job_city.save()

        sub_divs = main.find('div', class_='salary-estimate')
        if sub_divs is not None:
            jb_salary_text = sub_divs.text.strip()
            if jb_salary_text:
                js, _ = Salary.objects.get_or_create(salary=jb_salary_text)
                jb_salary = js
            else:
                jb_salary = None
        else:
            continue

        job_city, _ = Cities.objects.get_or_create(cities=job_city_name)
        imgs, _ = Images.objects.get_or_create(image=imgs_name)

        if not UsJobs.objects.filter(Job_link=jb_link).exists():
            # Job does not exist, save it to the database
            usajb = UsJobs(
                Title=jb_title,
                Job_link=jb_link,
                campany=jb_campany,
                Date_posted=posted_date,
                job_salary=jb_salary,
                cities=job_city,
                images=imgs)
            usajb.save()

            # Save other related details
            # ...
        else:
            # Job already exists in the database, skip saving
            continue

        driver.get(jb_link)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#JobDescriptionContainer")))
        except TimeoutException:
            print("Page loading timed out. Skipping this job listing.")
            continue

        soup_link = BeautifulSoup(driver.page_source, "html.parser")
        if soup_link is not None:
            page = soup_link.find_all('div', class_='desc css-58vpdc ecgq1xb5')
            if page is not None:
                for element in page:
                    det = JobDetails()
                    det.job = usajb
                    det.details = element.get_text().strip()
                    det.save()
                    # Process the details here, such as printing or storing them
                    # print(details)


            # elif page:
            #     paragraphs = page.find_all('p')
            #     if paragraphs is not None:
            #         for para in paragraphs:
            #             details = para.get_text().strip()
            #             print(details)
            #     else:
            #         continue

            else:
                continue


        else:
            continue

        for element in page:
            bold_txt = element.find_all('div', class_='desc css-58vpdc ecgq1xb5')
            for b in bold_txt:
                bold_tag = b.find_all('b')
                content = b.get_text()
                if bold_tag:
                    job_detail = JobDetails(job=usajb, details=content, bold=True)
                else:
                    job_detail = JobDetails(job=usajb, details=content, bold=False)
                job_detail.save()

driver.close()


class UsJobViewSet(viewsets.ModelViewSet):
    serializer_class = UsJobSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        fields = ['id', 'Title', 'Job_link', 'campany' , 'Date_posted', ]
        queryset = UsJobs.objects.values(*fields)

        return queryset

class UsJobViewSet(viewsets.ModelViewSet):
    serializer_class = UsJobSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        fields = ['id', 'Title', 'Job_link']
        queryset = UsJobs.objects.values(*fields)

        return queryset

class page(PageNumberPagination):
    page_size = 10

class UsJobsViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthenticated,
    queryset = UsJobs.objects.all()
    serializer_class = UsJobSerializer
    pagination_class = page

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # params request
        id = request.query_params.get('id')
        Title = request.query_params.get('Title')
        cities = request.query_params.get('cities')
        campany = request.query_params.get('campany')

        # Get JSON body from the request
        filters = request.data
        id_json = filters.get('id')
        Title_json = filters.get('Title')
        cities_json = filters.get('cities')
        campany_json = filters.get('campany')

        # Apply filters based on the specified fields
        if id or id_json:
            queryset = queryset.filter(id__icontains=id or id_json)
        if Title or Title_json:
            queryset = queryset.filter(Title__icontains=Title or Title_json)
        if cities or cities_json:
            queryset = queryset.filter(cities__icontains= cities or cities_json)
        if campany or campany_json:
            queryset = queryset.filter(campany__icontains=campany or campany_json)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class JobDetailViewSet(viewsets.ModelViewSet):

    queryset = JobDetails.objects.all()
    serializer_class = JobDtailSerializer


class CitiesViewSet(viewsets.ModelViewSet):

    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer


class SalaryViewSet(viewsets.ModelViewSet):

    queryset = Salary.objects.all()
    serializer_class = SalarySerializer


class ImageViewSet(viewsets.ModelViewSet):

    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Hash the password using the user's built-in algorithm
            password = validated_data['password']
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password
            # Save the user with the hashed password
            user = serializer.save()
            response_data = {
                'message': 'User registered successfully',
                'username': user.username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @method_decorator(csrf_exempt, name='dispatch')
# from django.views.decorators.csrf import csrf_protect
# @method_decorator(csrf_protect, name='create')
class LoginViewSet(viewsets.ViewSet):
    def create(self, request):

        #
        email = request.data.get('email')
        password = request.data.get('password')

        # Perform authentication
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # User is authenticated, log in
            login(request, user)
            token = RefreshToken.for_user(user)
            # data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response({'message': 'Login successful', "access": str(token.access_token)})
            # return Response({'message': 'Login successful'})

        else:
            # Invalid credentials
            return Response({'message': 'Invalid username or password'}, status=401)

        # user=User.objects.filter(email=email).first()
        # if  user is None:
        #     raise AuthenticationFailed("User not Found !")
        # if not user.check_password(password):
        #     raise AuthenticationFailed("incorrect password")
        # return Response(User)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['user_id'] = user.id
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer