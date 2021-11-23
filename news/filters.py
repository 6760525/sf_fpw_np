from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter
from django import forms
from .models import Author, Category
 

class DateInput(forms.DateInput):
    input_type = 'date'
 
# создаём фильтр
class PostFilter(FilterSet):
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('title', '')
        super().__init__(data, *args, **kwargs)
            
    title = CharFilter('title',
                               label='Заголовок содержит:', 
                               lookup_expr='icontains',
                               )

    author = ModelMultipleChoiceFilter('author',
                               label='Автор(ы):', 
                               lookup_expr='exact',
                               queryset=Author.objects.all()
                               )

    category = ModelMultipleChoiceFilter('category',
                               label='Категории:', 
                               lookup_expr='exact',
                               queryset=Category.objects.all()
                               )
    creation_time = DateFilter('creation_time',
                               label='Дата публикации позже:', 
                               lookup_expr='gt',
                               widget=DateInput(attrs={'class': 'DateInput'})
                               )
