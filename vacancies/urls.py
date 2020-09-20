from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from stepik_project2 import settings
from vacancies.views import MainView, VacancyCatView, VacancyListView, CompanyView, VacancyInfoView, \
    MyCompanyView, MyCompanyVacanciesView, MyLoginView, MySignupView, \
    MyCompanyCreateView, MyCompanyVacancyEditView, MyCompanyVacancyCreateView, ResumeView, SearchView, \
    ResumeEditView

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies_page'),
    path('vacancies/cat/<str:category_name>', VacancyCatView.as_view(), name='category_page'),
    path('companies/<int:id>', CompanyView.as_view(), name='company_page'),
    path('vacancies/<int:id>', VacancyInfoView.as_view(), name='vacancy_info'),

    path('mycompany/create/', MyCompanyCreateView.as_view(), name='my_company_create'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),

    path('mycompany/vacancies', MyCompanyVacanciesView.as_view(), name='my_company_vacancies'),

    path('mycompany/vacancies/<int:pk>', MyCompanyVacancyEditView.as_view(), name='my_company_vacancy_edit'),
    path('mycompany/vacancies/create/', MyCompanyVacancyCreateView.as_view(), name='my_company_vacancy_create'),

    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', MySignupView.as_view(), name='signup'),

    path('search/', SearchView.as_view(), name='search'),
    path('myresume/', ResumeView.as_view(), name='resume'),
    path('myresume/create/', ResumeEditView.as_view(), name='edit_resume'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
