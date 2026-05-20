DIRECTIONS = [
    {'title': 'Городские экскурсии', 'slug': 'city'},
    {'title': 'Туры по Сибири', 'slug': 'siberia'},
    {'title': 'Туры выходного дня', 'slug': 'weekend'},
]


class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.extra_context = self.extra_context.copy()

        if self.title_page:
            self.extra_context['title'] = self.title_page

        self.extra_context.setdefault('directions', DIRECTIONS)
        self.extra_context.setdefault('current_direction', None)
        self.extra_context.setdefault('cat_selected', None)

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context['directions'] = DIRECTIONS
        context['current_direction'] = None
        context['cat_selected'] = None
        context['selected_direction'] = ''
        context['selected_sort'] = 'new'

        context.update(kwargs)

        return context