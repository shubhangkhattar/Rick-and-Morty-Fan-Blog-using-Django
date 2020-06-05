from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Mark published"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')
make_draft.short_description = "Mark Draft"


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','publish','created','updated']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['status','publish','created','updated','author']
    search_fields = ['title','author','body']
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    actions = [make_published,make_draft]

class CommentAdmin(admin.ModelAdmin):
    # readonly_fields = ['post']
    list_display = ['name','created','updated','active']
    list_filter = ['active']
    search_fields = ['name','body']


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
