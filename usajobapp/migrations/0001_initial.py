# Generated by Django 4.2.2 on 2023-07-06 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cities', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UsJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=10000)),
                ('Job_link', models.URLField(max_length=10000)),
                ('campany', models.CharField(max_length=1000)),
                ('Date_posted', models.DateField(max_length=100)),
                ('cities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_cities', to='usajobapp.cities')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_images', to='usajobapp.images')),
                ('job_salary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_salaries', to='usajobapp.salary')),
            ],
        ),
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=20000)),
                ('bold', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_details', to='usajobapp.usjobs')),
            ],
        ),
    ]
