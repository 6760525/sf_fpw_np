from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(author=self, type=Post.article)
        # суммарный рейтинг каждой статьи автора умножается на 3;
        rating = 3 * posts.aggregate(Sum('rating'))['rating__sum']
        # суммарный рейтинг всех комментариев автора;
        rating += Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        # суммарный рейтинг всех комментариев к статьям автора
        rating += Comment.objects.filter(post__in=posts.values('pk')).aggregate(Sum('rating'))['rating__sum']

        self.rating = rating
        self.save()

    def __str__(self):
        return f'{self.user}'

class Category(models.Model):
    category = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.category}'

class Post(models.Model):
    
    article = 'AR'
    news = 'NE'

    TYPES = [
        (article, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    type = models.CharField(max_length=2,
                            choices=TYPES,
                            default=news)
    creation_time = models.DateTimeField(auto_now_add=True, )
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '\u2026'
    
    def __str__(self):
        return f'{self.title}: {self.text[:200]}'
    
    def get_absolute_url(self):
        return f'/news/{self.id}' 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True, )
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )
        

class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

class SocialSignupForm(SignupForm):
    
    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
    
    def signup(self, request, user):
        user = super(SocialSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user.save()
        return user
    
