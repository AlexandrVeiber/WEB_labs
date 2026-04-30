from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Tour, Category, TagPost, TourInfo


class TransportFilter(admin.SimpleListFilter):
    title = 'Тип транспорта'
    parameter_name = 'transport'

    def lookups(self, request, model_admin):
        return [
            ('walk', 'Пешая экскурсия'),
            ('bus', 'Автобус'),
            ('microbus', 'Микроавтобус'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'walk':
            return queryset.filter(info__transport='Пешая экскурсия')
        if self.value() == 'bus':
            return queryset.filter(info__transport='Автобус')
        if self.value() == 'microbus':
            return queryset.filter(info__transport='Микроавтобус')
        return queryset


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'tour_photo',
        'cat',
        'price',
        'time_create',
        'is_published',
        'brief_description',
        'places_info',
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ('-time_create', 'title')
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'description', 'cat__name')
    list_filter = (TransportFilter, 'cat', 'is_published')

    fields = (
        'title',
        'slug',
        'description',
        'photo',
        'tour_photo',
        'duration',
        'price',
        'direction',
        'cat',
        'tags',
        'is_published',
    )
    readonly_fields = ('tour_photo',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)

    @admin.display(description='Фото')
    def tour_photo(self, tour):
        if tour.photo:
            return mark_safe(
                f"<img src='{tour.photo.url}' width='70' style='border-radius: 8px;'>"
            )
        return 'Без фото'

    @admin.display(description='Краткое описание')
    def brief_description(self, tour):
        return f'Описание: {len(tour.description)} символов'

    @admin.display(description='Свободные места')
    def places_info(self, tour):
        if hasattr(tour, 'info'):
            return tour.info.places_count
        return 'Нет данных'

    @admin.action(description='Опубликовать выбранные туры')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Tour.Status.PUBLISHED)
        self.message_user(
            request,
            f'Опубликовано туров: {count}.',
            messages.SUCCESS
        )

    @admin.action(description='Снять выбранные туры с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Tour.Status.DRAFT)
        self.message_user(
            request,
            f'Снято с публикации туров: {count}.',
            messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(TourInfo)
class TourInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'transport', 'accommodation', 'places_count')
    list_display_links = ('id', 'tour')