from django.contrib import admin

from .models import Category, Article, UserProfile, News

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(UserProfile)
admin.site.register(News)


