from django.contrib import admin
from .forms import PostForm
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()

admin.site.register(Category)
admin.site.register(Post, PostAdmin)