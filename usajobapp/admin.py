from django.contrib import admin
from .models import UsJobs,JobDetails, Salary,Cities,Images
    # , Type,
# Register your models here.
admin.site.register(UsJobs)
admin.site.register(JobDetails)
admin.site.register(Cities)
admin.site.register(Images)
admin.site.register(Salary)