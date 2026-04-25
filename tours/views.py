from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Tour, Category, TagPost


DIRECTIONS = [
    {'title': 'Городские экскурсии', 'slug': 'city'},
    {'title': 'Туры по Сибири', 'slug': 'siberia'},
    {'title': 'Туры выходного дня', 'slug': 'weekend'},
]


def index(request):
    selected_direction = request.GET.get('direction', '')
    selected_sort = request.GET.get('sort', 'new')

    tours = Tour.published.select_related('cat').prefetch_related('tags').all()

    if selected_direction in {'city', 'siberia', 'weekend'}:
        tours = tours.filter(direction=selected_direction)

    sort_map = {
        'new': '-time_create',
        'old': 'time_create',
        'title': 'title',
    }
    tours = tours.order_by(sort_map.get(selected_sort, '-time_create'))

    context = {
        'title': 'Главная страница',
        'company_name': 'Турагентство «Новосибирск-Тур»',
        'description': 'Подбор туров и экскурсий по Новосибирску и Сибири',
        'directions': DIRECTIONS,
        'tours': tours,
        'current_direction': None,
        'selected_direction': selected_direction,
        'selected_sort': selected_sort,
        'cat_selected': 0,
    }

    return render(request, 'tours/index.html', context=context)


def tour_detail(request, tour_slug):
    tour = get_object_or_404(
        Tour.published.select_related('cat', 'info').prefetch_related('tags'),
        slug=tour_slug
    )

    context = {
        'title': tour.title,
        'tour': tour,
        'tour_slug': tour_slug,
        'current_direction': tour.direction,
        'cat_selected': tour.cat_id,
    }

    return render(request, 'tours/tour_detail.html', context=context)


def category(request, cat_slug):
    category_obj = get_object_or_404(Category, slug=cat_slug)

    tours = Tour.published.select_related('cat').prefetch_related('tags').filter(
        cat_id=category_obj.pk
    ).order_by('-time_create')

    context = {
        'title': f'Категория: {category_obj.name}',
        'company_name': f'Категория: {category_obj.name}',
        'description': 'Список туров выбранной категории',
        'directions': DIRECTIONS,
        'tours': tours,
        'current_direction': None,
        'selected_direction': '',
        'selected_sort': 'new',
        'cat_selected': category_obj.pk,
    }

    return render(request, 'tours/index.html', context=context)


def show_tag_tourlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)

    tours = tag.tags.select_related('cat').prefetch_related('tags').filter(
        is_published=Tour.Status.PUBLISHED
    ).order_by('-time_create')

    context = {
        'title': f'Туры по тегу: {tag.tag}',
        'company_name': f'Туры по тегу: {tag.tag}',
        'description': 'Список туров, связанных с выбранным тегом',
        'directions': DIRECTIONS,
        'tours': tours,
        'current_direction': None,
        'selected_direction': '',
        'selected_sort': 'new',
        'cat_selected': None,
    }

    return render(request, 'tours/index.html', context=context)


def direction(request, dir_slug):
    direction_names = {
        'city': 'Городские экскурсии',
        'siberia': 'Туры по Сибири',
        'weekend': 'Туры выходного дня',
    }

    if dir_slug not in direction_names:
        raise Http404()

    tours = Tour.published.select_related('cat').prefetch_related('tags').filter(
        direction=dir_slug
    ).order_by('-time_create')

    context = {
        'title': direction_names[dir_slug],
        'direction_name': direction_names[dir_slug],
        'direction_slug': dir_slug,
        'current_direction': dir_slug,
        'tours': tours,
        'cat_selected': None,
    }

    return render(request, 'tours/direction.html', context=context)


def contacts(request):
    contact_data = {
        'address': 'г. Новосибирск, Красный проспект, 25',
        'phone': '+7 (383) 000-00-00',
        'email': 'info@nsk-tours.ru',
        'schedule': 'Пн–Пт: 10:00–19:00, Сб: 11:00–16:00',
    }

    context = {
        'title': 'Контакты',
        'contact_data': contact_data,
        'current_direction': None,
        'cat_selected': None,
    }

    return render(request, 'tours/contacts.html', context=context)


def prices(request):
    year = request.GET.get('year')
    if year and year.isdigit() and int(year) > 2026:
        return redirect('home')

    services = [
        {'name': 'Обзорная экскурсия по Новосибирску', 'price': '2500 руб.'},
        {'name': 'Экскурсия в Академгородок', 'price': '3200 руб.'},
        {'name': 'Тур выходного дня по области', 'price': '4500 руб.'},
        {'name': 'Индивидуальный тур по запросу', 'price': 'от 6000 руб.'},
    ]

    context = {
        'title': 'Цены',
        'services': services,
        'current_direction': None,
        'cat_selected': None,
    }

    return render(request, 'tours/prices.html', context=context)


def archive(request, year):
    context = {
        'title': f'Архив туров за {year} год',
        'year': year,
        'current_direction': None,
        'cat_selected': None,
    }

    return render(request, 'tours/archive.html', context=context)


def page_not_found(request, exception):
    context = {
        'title': 'Страница не найдена',
        'current_direction': None,
        'cat_selected': None,
    }

    return render(request, 'tours/404.html', context=context, status=404)