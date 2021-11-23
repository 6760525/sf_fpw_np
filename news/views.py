from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from .models import Category, Post
from .filters import PostFilter
from .forms import PostForm
import datetime
 
 
class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    #context_object_name = 'news'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-creation_time')
    paginate_by = 10
    form_class = PostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()  # добавим переменную текущей даты time_now
        
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if form.is_valid(): 
            form.save()
 
        return super().get(request, *args, **kwargs)
    
  
class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'post.html'  # название шаблона будет product.html
    context_object_name = 'post'  # название объекта. в нём будет

class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostsSearch(FilteredListView):
    filterset_class = PostFilter
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    paginate_by = 10
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetailView(DetailView):
    template_name = 'post.html'
    quesryset = Post.objects.all()
    
class PostCreateView(CreateView):
    template_name = 'create.html'
    form_class = PostForm
    
class PostUpdateView(UpdateView):
    template_name = 'create.html'
    form_class = PostForm
 
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    