from django.db import models
from django.contrib.auth.models import User

article = 'AR'
news = 'NS'

POST_TYPE = [
    (article, 'Статья'),
    (news, 'Новости')
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(post__author=self)
        comments_rating = Comment.objects.filter(user=self.user)
        comments_posts_rating = Comment.objects.filter(post__author=self)
        for p in posts_rating:
            posts_rating += p.rating
        for c in comments_rating:
            posts_rating += c.rating
        for cp in comments_posts_rating:
            posts_rating += cp.rating

        self.rating = posts_rating * 3 + comments_rating + comments_posts_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

class Post(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=36,
                                 choices=POST_TYPE)
    creation_date = models.DateTimeField(auto_now_add=True)
    topic_name = models.CharField(max_length=80, unique=True)
    post_text = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:124]

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
