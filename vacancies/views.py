from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views import View

from vacancies.models import Specialty, Company, Vacancy


def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не существует =(')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера')


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        return render(request, 'index.html', context={'specialties': specialties, 'companies': companies})


class VacancyListView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancy-list.html', context={'vacancies': vacancies})


class VacancyCatView(View):
    def get(self, request, category_name):
        category_name = get_object_or_404(Specialty, code=category_name)
        vacancies = Vacancy.objects.filter(specialty=category_name)
        print(len(vacancies))
        return render(request, 'vacancies.html', context={'category': category_name, 'vacancies': vacancies})


class CompanyView(View):
    def get(self, request, id):
        company = get_object_or_404(Company, pk=id)
        vacancies = Vacancy.objects.filter(company=company)
        print(vacancies)
        return render(request, 'company.html', context={'vacancies': vacancies, 'company': company})


class VacancyInfoView(View):
    def get(self, request, id):
        vacancy = get_object_or_404(Vacancy, pk=id)
        print(vacancy)
        return render(request, 'vacancy.html', context={'vacancy': vacancy})
