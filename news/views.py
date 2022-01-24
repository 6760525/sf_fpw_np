from os import name
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Category, Post
from .models import BaseRegisterForm
from .models import Author
from .filters import PostFilter
from .forms import PostForm
from .forms import SubscribeCategory
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.generic import TemplateView
from django.core.cache import cache
 
class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-creation_time')
    paginate_by = 10
    form_class = PostForm
    
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
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
    model = Post  
    template_name = 'post.html'
    context_object_name = 'post'

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
    model = Post  
    template_name = 'search.html' 
    paginate_by = 10
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostDetailView(DetailView):
    template_name = 'post.html'
    quesryset = Post.objects.all()

class PostLimitView(TemplateView):
    template_name = 'post_limit.html'
    
    def post(self, request, *args, **kwargs):
        return redirect('/')
  
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    model = Post
    template_name = 'create.html'
    form_class = PostForm
    success_url = '/news/'
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        author = Author.objects.get(user=user)
        d_from = datetime.now().date()
        d_to = d_from+timedelta(days=1)
        posts = Post.objects.filter(author=author, creation_time__range=(d_from, d_to))
        if len(posts) > 3:
            return redirect('limit/')

        form = PostForm(request.POST)
        client_cat = request.POST.getlist('category')
        client_text = request.POST['text']
        client_title = request.POST['title']
        subscribers = []
        for c in client_cat:
            sub = Category.objects.get(pk=c)
            for u in sub.subscribers.all():
                if u not in subscribers:
                    subscribers.append(u)
        print(subscribers)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            post.save()
            
            for subscriber in subscribers:
                print(subscriber.email)
                if subscriber.email:
                    print(f'Sending notification to {subscriber.email}')
                    
                    html_content = render_to_string(
                        'notification_created.html', {
                            'id': post.id,
                            'user': subscriber,
                            'title': client_title,
                            'text': client_text[:50],
                        }
                    )
 
                    msg = EmailMultiAlternatives(
                        subject=f'Здравствуй, {subscriber}. Новая статья в твоём любимом разделе!',
                        body=f'{client_text[:50]}',
                        from_email='aturin@yandex.ru',
                        to=[subscriber.email, '6760525@gmail.com'],  
                    )
                    
                    msg.attach_alternative(html_content, "text/html")
                    msg.send() 
                    
            return redirect(post)
            
        return PostForm(request, 'create.html', {'form': form})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

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
    author = Author.objects.create(user=request.user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(request.user)
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
    

class SubscribeView(LoginRequiredMixin, FormView):
    form_class = SubscribeCategory
    template_name = 'subscribe.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        category_id = self.request.POST['category']
        category = Category.objects.get(pk=category_id)
        category.subscribers.add(user)
        category.save()
        return super().form_valid(form)    
        