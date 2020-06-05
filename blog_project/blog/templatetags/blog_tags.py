from blog.models import Post
from django import template
from django.db.models import Count

register = template.Library()

@register.simple_tag(name='total_posts')
def total_posts_tag():
    return Post.objects.count()


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count = 2):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=2):
    return Post.objects.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
