from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from stepik_project2.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=60, default='')
    location = models.CharField(max_length=120, default='', null=True, blank=True)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    employee_count = models.IntegerField(null=True, blank=True, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True,
                              related_name='company')

    def __str__(self):
        return f'{self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=20, default='', unique=True)
    title = models.CharField(max_length=40, default='')
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=60)
    specialty = models.ForeignKey(Specialty, on_delete=CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=CASCADE, related_name='vacancies')
    skills = models.TextField(default='', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.PositiveIntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='applications')

    def __str__(self):
        return f'{self.id}: {self.written_username}'


class Resume(models.Model):
    STATUS_CHOICES = [('NOT_LOOKING_FOR_JOB', 'Не ищу работу'),
                      ('CONSIDERING_PROPOSALS', 'Рассматриваю предложения'),
                      ('LOOKING_FOR_JOB', 'Ищу работу'),
                      ]
    GRADE_CHOICES = [('TRAINEE', 'Стажер'), ('JUNIOR', 'Джуниор'),
                     ('MIDDLE', 'Миддл'), ('SENOR', 'Сеньор'),
                     ('LEAD', 'ЛИД')
                     ]

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    status = models.CharField(max_length=21, choices=STATUS_CHOICES)
    salary = models.IntegerField(null=True, blank=True)
    specialty = models.CharField(max_length=35, null=True, blank=True)
    grade = models.CharField(max_length=7, choices=GRADE_CHOICES, null=True, blank=True)
    education = models.CharField(max_length=250, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    portfolio = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resume')
