import uuid
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .forms import AddTourForm, AddTourModelForm, UploadFileForm
from .models import Tour, Category, TagPost, TourInfo
from .utils import DataMixin


class ToursHome(DataMixin, ListView):
    template_name = 'tours/index.html'
    context_object_name = 'tours'
    title_page = 'Главная страница'

    def get_queryset(self):
        selected_direction = self.request.GET.get('direction', '')
        selected_sort = self.request.GET.get('sort', 'new')

        tours = Tour.published.select_related('cat').prefetch_related('tags').all()

        if selected_direction in {'city', 'siberia', 'weekend'}:
            tours = tours.filter(direction=selected_direction)

        sort_map = {
            'new': '-time_create',
            'old': 'time_create',
            'title': 'title',
        }

        return tours.order_by(sort_map.get(selected_sort, '-time_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            company_name='Турагентство «Новосибирск-Тур»',
            description='Подбор туров и экскурсий по Новосибирску и Сибири',
            selected_direction=self.request.GET.get('direction', ''),
            selected_sort=self.request.GET.get('sort', 'new'),
            cat_selected=0,
        )


class TourDetailView(DataMixin, DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'

    def get_queryset(self):
        return Tour.published.select_related('cat', 'info').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=self.object.title,
            tour_slug=self.object.slug,
            current_direction=self.object.direction,
            cat_selected=self.object.cat_id,
        )


class TourCategoryView(DataMixin, ListView):
    template_name = 'tours/index.html'
    context_object_name = 'tours'
    allow_empty = False

    def get_queryset(self):
        self.category_obj = get_object_or_404(Category, slug=self.kwargs['cat_slug'])

        return Tour.published.select_related('cat').prefetch_related('tags').filter(
            cat_id=self.category_obj.pk
        ).order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=f'Категория: {self.category_obj.name}',
            company_name=f'Категория: {self.category_obj.name}',
            description='Список туров выбранной категории',
            cat_selected=self.category_obj.pk,
        )


class TagTourListView(DataMixin, ListView):
    template_name = 'tours/index.html'
    context_object_name = 'tours'
    allow_empty = False

    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])

        return self.tag.tags.select_related('cat').prefetch_related('tags').filter(
            is_published=Tour.Status.PUBLISHED
        ).order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=f'Туры по тегу: {self.tag.tag}',
            company_name=f'Туры по тегу: {self.tag.tag}',
            description='Список туров, связанных с выбранным тегом',
            cat_selected=None,
        )


class DirectionTourListView(DataMixin, ListView):
    template_name = 'tours/direction.html'
    context_object_name = 'tours'
    allow_empty = False

    direction_names = {
        'city': 'Городские экскурсии',
        'siberia': 'Туры по Сибири',
        'weekend': 'Туры выходного дня',
    }

    def get_queryset(self):
        self.direction_slug = self.kwargs['dir_slug']

        if self.direction_slug not in self.direction_names:
            raise Http404()

        return Tour.published.select_related('cat').prefetch_related('tags').filter(
            direction=self.direction_slug
        ).order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=self.direction_names[self.direction_slug],
            direction_name=self.direction_names[self.direction_slug],
            direction_slug=self.direction_slug,
            current_direction=self.direction_slug,
            cat_selected=None,
        )


class ContactsView(DataMixin, TemplateView):
    template_name = 'tours/contacts.html'
    title_page = 'Контакты'

    extra_context = {
        'contact_data': {
            'address': 'г. Новосибирск, Красный проспект, 25',
            'phone': '+7 (383) 000-00-00',
            'email': 'info@nsk-tours.ru',
            'schedule': 'Пн–Пт: 10:00–19:00, Сб: 11:00–16:00',
        },
    }


class PricesView(DataMixin, TemplateView):
    template_name = 'tours/prices.html'
    title_page = 'Цены'

    def get(self, request, *args, **kwargs):
        year = request.GET.get('year')

        if year and year.isdigit() and int(year) > 2026:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        services = [
            {'name': 'Обзорная экскурсия по Новосибирску', 'price': '2500 руб.'},
            {'name': 'Экскурсия в Академгородок', 'price': '3200 руб.'},
            {'name': 'Тур выходного дня по области', 'price': '4500 руб.'},
            {'name': 'Индивидуальный тур по запросу', 'price': 'от 6000 руб.'},
        ]

        return self.get_mixin_context(
            context,
            services=services,
        )


class ArchiveView(DataMixin, TemplateView):
    template_name = 'tours/archive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = self.kwargs['year']

        return self.get_mixin_context(
            context,
            title=f'Архив туров за {year} год',
            year=year,
        )


class AddTourFormView(DataMixin, FormView):
    form_class = AddTourForm
    template_name = 'tours/add_tour_form.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление тура через обычную форму'

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        tags = data.pop('tags')

        tour = Tour.objects.create(**data)
        tour.tags.set(tags)

        TourInfo.objects.get_or_create(tour=tour)

        return super().form_valid(form)


class AddTourModelFormView(DataMixin, CreateView):
    form_class = AddTourModelForm
    template_name = 'tours/add_tour_model_form.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление тура через ModelForm'

    def form_valid(self, form):
        response = super().form_valid(form)

        TourInfo.objects.get_or_create(tour=self.object)

        return response


class UpdateTourView(DataMixin, UpdateView):
    model = Tour
    form_class = AddTourModelForm
    template_name = 'tours/add_tour_model_form.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'tour_slug'
    title_page = 'Редактирование тура'


class DeleteTourView(DataMixin, DeleteView):
    model = Tour
    template_name = 'tours/tour_confirm_delete.html'
    context_object_name = 'tour'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'tour_slug'
    title_page = 'Удаление тура'


def handle_uploaded_file(uploaded_file):
    upload_dir = settings.BASE_DIR / 'uploads'
    upload_dir.mkdir(exist_ok=True)

    original_name = Path(uploaded_file.name)
    file_name = original_name.stem
    file_ext = original_name.suffix
    random_suffix = uuid.uuid4().hex

    new_file_name = f'{file_name}_{random_suffix}{file_ext}'
    file_path = upload_dir / new_file_name

    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return new_file_name


class UploadFileView(DataMixin, View):
    title_page = 'Загрузка файла'

    def get(self, request):
        form = UploadFileForm()

        context = self.get_mixin_context(
            {
                'form': form,
                'success_message': None,
            }
        )

        return render(request, 'tours/upload_file.html', context=context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        success_message = None

        if form.is_valid():
            saved_file_name = handle_uploaded_file(form.cleaned_data['file'])
            success_message = f'Файл успешно загружен: {saved_file_name}'

        context = self.get_mixin_context(
            {
                'form': form,
                'success_message': success_message,
            }
        )

        return render(request, 'tours/upload_file.html', context=context)


def page_not_found(request, exception):
    context = {
        'title': 'Страница не найдена',
        'current_direction': None,
        'cat_selected': None,
    }

    return render(request, 'tours/404.html', context=context, status=404)