from rest_framework import serializers
from  .models import UsJobs, JobDetails,Salary, Cities, Images
    # ,Type



class JobDtailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields ='__all__'

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields ='__all__'

# class JbImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=JbImage
#         fields='__all__'
# class TypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Type
#         fields ='__all__'
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images
        fields ='__all__'
class UsJobSerializer(serializers.ModelSerializer):
    # job_location = LocationSerializer()
    # job_type = TypeSerializer()
    job_salary = SalarySerializer()
    cities = CitiesSerializer()
    images =ImageSerializer()
    # jb_images =JbImageSerializer
    job_details = JobDtailSerializer(many=True)


    class Meta:
        model = UsJobs
        fields = ['id', 'Title', 'Job_link', 'campany','Date_posted', 'cities', 'job_salary','images', 'job_details']
