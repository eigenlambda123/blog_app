from django.contrib import admin
from .models import Post, Profile

admin.site.register(Post)
admin.site.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    fields = ('title', 'content', 'author', 'image', 'created_at', 'updated_at')  # Add 'image' here
    readonly_fields = ('created_at', 'updated_at')

