import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.shortcuts import render
from selenium.common import TimeoutException
from rest_framework import viewsets
from rest_framework.response import Response
from .models import UsJobs, JobDetails, Salary, Cities, Images
from .serializers import UsJobSerializer, JobDtailSerializer, SalarySerializer, CitiesSerializer, ImageSerializer

# Create your views here

# url = 'https://www.glassdoor.com/Job/united-states-all-jobs-SRCH_IL.0,13_IN1_KO14,17.htm?sortBy=date_desc'
for i in range(1,2):
    url='https://www.glassdoor.com/Job/united-states-all-jobs-SRCH_IL.0,13_IN1_KO14,17.htm?sortBy=date_desc'+str(i)
    driver = webdriver.Chrome()
    driver.get(url)


    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MainCol")))
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    main_div_list = soup.find_all('li', class_='react-job-listing css-108gl9c eigr9kq3')

    for main in main_div_list:
        sub_div = main.find('div', class_='job-search-3x5mv1')

        if sub_div:
            url1 = 'https://www.glassdoor.com'
            jb_title = sub_div.find('div', class_='job-title mt-xsm').text.strip()
            jb_link = url1 + sub_div.find('a', class_='d-flex justify-content-between p-std jobCard')['href']
            jb_campany = sub_div.find('div', class_='job-search-8wag7x').text.strip()
            dr = sub_div.find('div', class_='d-flex align-items-end ml-xsm listing-age')
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

            div_element = sub_div.find('div', class_='d-flex job-search-1sohcmw')
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


            job_cities = sub_div.find('div', class_='location mt-xxsm').text.strip()
            if len(job_cities) >= 2:
                job_city_name = job_cities

                if not Cities.objects.filter(cities=job_city_name).exists():
                    new_job_city = Cities(cities=job_city_name)
                    new_job_city.save()

            sub_divs = sub_div.find('div', class_='salary-estimate')
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
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#JobDescriptionContainer")))
            except TimeoutException:
                print("Page loading timed out. Skipping this job listing.")
                continue
            soup_link = BeautifulSoup(driver.page_source, "html.parser")
            page = soup_link.find('div', class_='desc css-c43yjn ecgq1xb5')
            # pg = page.find('div')
            if page.get_text().strip() is not None:
                details=page.get_text().strip()
                det = JobDetails(details=details)
                det.job = usajb
                det.save()
                pg = page.find('div')
                if pg is not None:
                    details=pg.text.strip()
                    det = JobDetails(details=details)
                    det.job = usajb
                    det.save()

                    listing = pg.find('ul')
                    if listing is not None:
                        list_items = listing.find_all('li')  # Use find_all() to get all the list items
                        for item in list_items:
                            det=JobDetails()
                            det.job = usajb
                            det.details = item.text.strip()
                            det.save()
                else:
                    listing = page.find('ul')
                    if listing is not None:
                        list_items = listing.find_all('li')  # Use find_all() to get all the list items
                        for item in list_items:
                            det=JobDetails()
                            det.job = usajb
                            det.details = item.text.strip()
                            det.save()
            # elif page is not None:
            #     para =page.find_all('p').text.strip()
            #     for par in para:
            #         details = par.text.strip()
            #         print(details)
            else:
                pg = page.find('div')
                if pg is not None:
                    details=pg.get_text().strip()
                    det = JobDetails(details=details)
                    det.job = usajb
                    det.save()
                elif pg:
                    listing = page.find('ul')
                    if listing is not None:
                        details = pg.get_text().strip()
                        det = JobDetails(details=details)
                        det.job = usajb
                        det.save()
                        list_items = listing.find_all('li')  # Use find_all() to get all the list items
                        for item in list_items:
                            det=JobDetails()
                            det.job =usajb
                            det.details = item.text.strip()
                            det.save()
                else:
                    para =pg.find('p')
                    if para is not None:
                        details = pg.get_text().strip()
                        det = JobDetails(details=details)
                        det.job = usajb
                        det.save()
            # insrting bolds in dtails
            bold_txt = page.find_all('div') or page.find_all('p') or page.find_all('ul')
            for b in bold_txt:
                bold_tag = b.find_all('b')
                content = b.get_text()
                if bold_tag:
                    job_detail = JobDetails(job=usajb, details=content, bold=True)
                else:
                    job_detail = JobDetails(job=usajb, details=content, bold=False)
                job_detail.save()





    driver.close()


class UsJobsViewSet(viewsets.ModelViewSet):

    queryset = UsJobs.objects.all()
    serializer_class = UsJobSerializer


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
