from django.urls import path

from vacancies.views import MainView, VacancyCatView, VacancyListView, CompanyView, VacancyInfoView

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies_page'),
    path('vacancies/cat/<str:category_name>', VacancyCatView.as_view(), name='category_page'),

    path('companies/<int:id>', CompanyView.as_view(), name='company_page'),
    path('vacancies/<int:id>', VacancyInfoView.as_view(), name='vacancy_info'),
]
