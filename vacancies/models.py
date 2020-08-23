from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Company(models.Model):
    name = models.CharField(max_length=60, default='')
    location = models.CharField(max_length=120, default='')
    logo = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    employee_count = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f'{self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=20, default='', unique=True)
    title = models.CharField(max_length=40, default='')
    picture = models.CharField(max_length=40, default='')


class Vacancy(models.Model):
    title = models.CharField(max_length=60)
    specialty = models.ForeignKey(Specialty, on_delete=CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=CASCADE, related_name='vacancies')
    skills = models.TextField(default='')
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
