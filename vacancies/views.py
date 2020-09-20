from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from vacancies.forms import SignupForm, ApplicationForm, MyCompanyForm, MyCompanyVacancyForm, ResumeForm
from vacancies.models import Specialty, Company, Vacancy, Application, Resume


def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не существует =(')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера')


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all().annotate(number_of_vacancies=Count('vacancies'))
        companies = Company.objects.all()
        return render(request, 'index.html', context={'specialties': specialties, 'companies': companies})


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class VacancyCatView(View):
    def get(self, request, category_name):
        category_name = get_object_or_404(Specialty, code=category_name)
        vacancies = Vacancy.objects.filter(specialty=category_name)
        return render(request, 'vacancies/vacancies.html', context={'category': category_name, 'vacancies': vacancies})


class CompanyView(View):
    def get(self, request, id):
        company = get_object_or_404(Company, pk=id)
        vacancies = Vacancy.objects.filter(company=company)
        return render(request, 'company.html', context={'vacancies': vacancies, 'company': company})


class VacancyInfoView(View):
    def get(self, request, id):
        vacancy = get_object_or_404(Vacancy, pk=id)
        return render(request, 'vacancies/vacancy.html', context={'vacancy': vacancy})

    def post(self, request, id):
        vacancy = get_object_or_404(Vacancy, pk=id)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            written_username = data['written_username']
            written_phone = data['written_phone']
            written_cover_letter = data['written_cover_letter']

            # проверить, есть ли в базе юзер
            if request.user.is_authenticated:
                user = User.objects.get(id=request.user.id)
                Application.objects.create(written_username=written_username, written_phone=written_phone,
                                           written_cover_letter=written_cover_letter, vacancy=vacancy, user=user)
                return render(request, 'vacancies/send_vacancy_success.html', )
            else:
                form.add_error('written_username', 'Для отправки заявки необходимо войти в учетную запись')

        return render(request, 'vacancies/vacancy.html', context={'vacancy': vacancy, 'form': form})


class MyCompanyCreateView(View):
    def get(self, request):
        user = request.user

        if user.company.all():
            return redirect('my_company')
        return render(request, 'my_company/company-create.html')

    def post(self, request):
        Company.objects.create(name='Введите название Вашей компании', owner=request.user)
        return redirect('my_company')


class MyCompanyView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        try:
            company = Company.objects.get(owner=user.id)
            return render(request, 'my_company/mycompany.html', context={'company': company})

        except Company.DoesNotExist:
            return redirect('my_company_create')

        return render(request, 'my_company/mycompany.html')

    def post(self, request):
        form = MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            user = request.user
            company = Company.objects.get(owner=user)

            company.name = data['name']
            company.location = data['location']
            company.employee_count = data['employee_count']
            company.description = data['description']
            company.logo = data['logo']

            company.save()

        else:
            form.add_error('name', 'Имя компании должно быть заполнено!')
            return render(request, 'my_company/mycompany.html', context={'form': form})

        return redirect('my_company')


class MyCompanyVacanciesView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    model = Vacancy
    template_name = 'my_company/my_company_vacancies_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company.first()
        mycompany_vacancies = Vacancy.objects.filter(company=company).annotate(count=Count('applications'))
        context['mycompany_vacancies'] = mycompany_vacancies
        return context


class MyCompanyVacancyEditView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'my_company/my_company_vacancy_edit.html'
    model = Vacancy
    form_class = MyCompanyVacancyForm
    context_object_name = 'my_vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['applications'] = Application.objects.filter(vacancy=self.object.id)
        return context

    def get_success_url(self):
        return reverse('my_company_vacancy_edit', args=[self.object.id])


class MyCompanyVacancyCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'my_company/my_company_vacancy_create.html'
    model = Vacancy
    form_class = MyCompanyVacancyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        return context

    def get_success_url(self):
        return reverse('my_company_vacancy_edit', args=[self.object.id])

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        vacancy.company = Company.objects.get(owner=self.request.user.id)
        vacancy.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login-signup/login.html'


class MySignupView(CreateView):
    form_class = SignupForm
    template_name = 'login-signup/signup.html'
    success_url = '/login'

    def form_valid(self, form):
        form.save()
        return super(MySignupView, self).form_valid(form)


class ResumeView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        try:
            resume = Resume.objects.get(user=request.user.id)
            resume_form = ResumeForm(instance=resume)
            return render(
                request, 'resume/resume.html', context={'form': resume_form})
        except Resume.DoesNotExist:
            return render(request, 'resume/resume-create.html')

    def post(self, request):
        form = ResumeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            resume = Resume.objects.get(user=request.user.id)

            resume.name = data['name']
            resume.surname = data['surname']
            resume.status = data['status']
            resume.specialty = data['specialty']
            resume.salary = data['salary']
            resume.grade = data['grade']
            resume.education = data['education']
            resume.experience = data['experience']
            resume.portfolio = data['portfolio']

            resume.save()
        else:
            form.add_error('name', 'Что-то заполнили неверно!')
            print(form.errors)
            return render(
                request, 'resume/resume.html', context={'form': form})

        return redirect('resume')


class ResumeEditView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = ResumeForm()
        return render(request, 'resume/resume-edit.html', context={'form': form})

    def post(self, request):
        form = ResumeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Resume.objects.create(name=data['name'], surname=data['surname'], status=data['status'],
                                  salary=data['salary'], specialty=data['specialty'], grade=data['grade'],
                                  education=data['education'], experience=data['experience'],
                                  portfolio=data['portfolio'], user=request.user)
            return redirect('resume')
        return render(request, 'resume/resume-edit.html', context={'form': form})


class SearchView(View):
    def get(self, request):
        search = request.GET.get('s', '')
        vacancies = Vacancy.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if vacancies:
            return render(request, 'vacancies/vacancy-list.html', context={'vacancies': vacancies})
        else:
            return render(request, 'not-found404.html')
