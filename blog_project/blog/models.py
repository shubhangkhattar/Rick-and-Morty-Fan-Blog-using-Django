from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.

class Post(models.Model):

        STATUS_CHOICES = (('draft','Draft'),('published','Published'))
        slug = models.SlugField(max_length = 256,unique_for_date='publish')

        title = models.CharField(max_length = 256,verbose_name='Title')
        author = models.ForeignKey(User,related_name='blog_posts',verbose_name = 'Author',on_delete=models.DO_NOTHING)
        body = models.TextField(verbose_name='Post')
        publish = models.DateTimeField(default = timezone.now,verbose_name='Publish Date/Time')
        created = models.DateTimeField(auto_now_add = True)
        updated = models.DateTimeField(auto_now = True)
        status = models.CharField(max_length = 10,choices = STATUS_CHOICES , default='draft',verbose_name='Post Status')
        tags = TaggableManager()

        class Meta:
            ordering = ('-publish',)

        def __str__(self):
            return str(self.title + " : " + str(self.author))


        def get_absolute_url(self):
            return reverse('post_detail',args=[self.publish.year,self.slug,self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32,verbose_name = 'Name')
    body = models.TextField(verbose_name = 'Comment')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)
