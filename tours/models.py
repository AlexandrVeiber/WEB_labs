from django.db import models
from django.urls import reverse


class PublishedTourManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=self.model.Status.PUBLISHED
        )


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Tour(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название тура')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Продолжительность'
    )
    price = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Стоимость'
    )
    direction = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Направление'
    )
    
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    
    cat = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='tours',
        verbose_name='Категория'
    )

    tags = models.ManyToManyField(
        'TagPost',
        blank=True,
        related_name='tags',
        verbose_name='Теги'
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения'
    )
    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name='Статус публикации'
    )

    objects = models.Manager()
    published = PublishedTourManager()

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'tour_slug': self.slug})

    def get_direction_title(self):
        directions = {
            'city': 'Городские экскурсии',
            'siberia': 'Туры по Сибири',
            'weekend': 'Туры выходного дня',
        }
        return directions.get(self.direction, self.direction)

    def __str__(self):
        return self.title
    
    
class TourInfo(models.Model):
    tour = models.OneToOneField(
        'Tour',
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name='Тур'
    )
    transport = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Транспорт'
    )
    accommodation = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Проживание'
    )
    places_count = models.IntegerField(
        default=0,
        verbose_name='Количество свободных мест'
    )

    class Meta:
        verbose_name = 'Дополнительная информация о туре'
        verbose_name_plural = 'Дополнительная информация о турах'

    def __str__(self):
        return f'Информация о туре: {self.tour.title}'