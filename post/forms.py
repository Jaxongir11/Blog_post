from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'status', 'category']
        exclude = ['slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
