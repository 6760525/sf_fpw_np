from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Category, Post
from .filters import PostFilter
from .forms import PostForm
from .models import BaseRegisterForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-creation_time')
    paginate_by = 10
    form_class = PostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()  # добавим переменную текущей даты time_now
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
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
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
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
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostDetailView(DetailView):
    template_name = 'post.html'
    quesryset = Post.objects.all()
    
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    permission_required = ('news.add_post', )
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'create.html'
    form_class = PostForm
    permission_required = ('news.change_post', )
 
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    
   
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/' 
    
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = BaseRegisterForm
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile.html'
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=self.request.user.id)
    