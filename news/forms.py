from django.forms import ModelForm, Form, TextInput, Textarea, Select, SelectMultiple
from django.forms.models import ModelChoiceField
from .models import Post
from .models import Category


# Создаём модельную форму
class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'text', 'type', 'category']
        widgets = {
            'title': TextInput(attrs={"class": "form-control"}),
            'text': Textarea(attrs={"class": "form-control", "rows": 5}),
            'type': Select(attrs={"class": "form-control"}),
            'category': SelectMultiple(attrs={"class": "form-control"}),
        }
        labels = {'title': 'Заголовок',
                  'text': 'Текст статьи/новости',
                  'type': 'Тип',
                  'category': 'Категория(и)'}

class SubscribeCategory(Form):
    category = ModelChoiceField(queryset=Category.objects.all())
