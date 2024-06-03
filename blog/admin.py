from django.contrib import admin
from .models import Author, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post)
admin.site.register(Comment)