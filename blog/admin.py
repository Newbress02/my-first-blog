from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Photo



class PhotoInline(admin.TabularInline):
    model = Photo

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin.site.register(Post, PostAdmin)