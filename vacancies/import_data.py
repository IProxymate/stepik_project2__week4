from vacancies.data import jobs, companies, specialties
from vacancies.models import Company, Specialty, Vacancy


def import_data():
    place_holder = 'https://place-hold.it/100x60'
    for i in companies:
        Company.objects.create(name=i['title'], logo=place_holder)

    for code in specialties:
        Specialty.objects.create(code=code['code'], title=code['title'], picture=place_holder)

    for vacancy in jobs:
        specialty = Specialty.objects.get(code=vacancy['cat'])
        company = Company.objects.get(name=vacancy['company'])
        Vacancy.objects.create(title=vacancy['title'], specialty=specialty, company=company,
                               description=vacancy['desc'],
                               salary_min=vacancy['salary_from'], salary_max=vacancy['salary_to'])


if __name__ == '__main__':
    import_data()
