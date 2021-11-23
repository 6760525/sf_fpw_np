from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


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
