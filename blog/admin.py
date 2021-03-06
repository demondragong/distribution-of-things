from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'author', 'slug', 'status','image_path')
    list_display = ('title', 'slug', 'status', 'created_on', 'updated_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)