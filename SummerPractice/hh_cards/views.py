from django.shortcuts import render, redirect
from hh_cards.models import HHCard
from django.db.models import Q
import requests
import json
# Create your views here.


def index(request):
    organisation = request.GET.get('organisation')
    position = request.GET.get('position')
    salary = request.GET.get('salary')
    city = request.GET.get('city')
    query = Q()
    if organisation and organisation != '':
        query &= Q(organisation__icontains=organisation)
    if position and position != '':
        query &= Q(position__icontains=position)
    if salary:
        query &= Q(salary__gte=salary)
    if city and city != '':
        query &= Q(city__icontains=city)
    vacancies = HHCard.objects.filter(query)
    return render(request, 'index.html', {'vacancies': vacancies})



def parse_post(request):
    organisation = request.POST.get('organisation')
    position = request.POST.get('position')
    salary = request.POST.get('salary')
    city = request.POST.get('city')
    HHCard.objects.all().delete()
    try:
        filters = ''
        salfilter = ''
        if organisation and organisation != '':
            filters += f'company_name:{organisation} '
        if position and position != '':
            filters += f'name:{position} '
        if city and city != '':
            filters += f'{city} '
        text_filter = ''
        if filters != '':
            text_filter = f'&text={filters}'
        if salary and salary != '':
            salfilter = f'&salary={salary}'
        req = requests.get(f'https://api.hh.ru/vacancies?per_page=0{text_filter}{salfilter}')
        req.raise_for_status()
        data = req.json()
        pages = data['found'] // 100
        for page in range(pages):
            req = requests.get(f'https://api.hh.ru/vacancies?page={page}&per_page=100{text_filter}{salfilter}')
            req.raise_for_status()
            data = req.json()
            if 'items' in data:
                for item in data['items']:
                    organisation = item.get('employer', {}).get('name', '')
                    position = item.get('name')
                    city = item.get('area', {}).get('name', '')
                    salary = item.get('salary', {})
                    if salary:
                        salary_from = salary.get('from', 0.0)
                    else:
                        salary_from = 0.0
                    new_card = HHCard(organisation=organisation,
                                      position=position, salary=salary_from,
                                      city=city)
                    new_card.save()
    except requests.exceptions.RequestException as e:
        print(f"Request failed on page {page}: {e}")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON on page {page}")
    return redirect('/')


def parse(request):
    if request.method == 'POST':
        return parse_post(request)
    return render(request, 'parser.html')
