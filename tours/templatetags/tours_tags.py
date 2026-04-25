from django import template
from django.db.models import Count, Q

from tours.models import Tour, Category, TagPost

register = template.Library()


directions_data = [
    {'title': 'Городские экскурсии', 'slug': 'city'},
    {'title': 'Туры по Сибири', 'slug': 'siberia'},
    {'title': 'Туры выходного дня', 'slug': 'weekend'},
]


@register.inclusion_tag('tours/includes/directions_menu.html')
def show_directions(current_direction=None):
    return {
        'directions': directions_data,
        'selected_slug': current_direction,
    }


@register.inclusion_tag('tours/includes/categories_menu.html')
def show_categories(cat_selected=0):
    categories = Category.objects.annotate(
        total=Count(
            'tours',
            filter=Q(tours__is_published=Tour.Status.PUBLISHED)
        )
    ).filter(total__gt=0)

    return {
        'categories': categories,
        'cat_selected': cat_selected,
    }


@register.inclusion_tag('tours/includes/tags_menu.html')
def show_all_tags():
    tags = TagPost.objects.annotate(
        total=Count(
            'tags',
            filter=Q(tags__is_published=Tour.Status.PUBLISHED)
        )
    ).filter(total__gt=0).order_by('tag')

    return {
        'tags': tags,
    }


@register.inclusion_tag('tours/includes/popular_tours.html')
def show_popular_tours(count=3):
    tours = Tour.published.all()[:count]
    return {'tours': tours}