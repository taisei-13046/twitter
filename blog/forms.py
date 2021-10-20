from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 2, 'cols': 70, 'placeholder': 'ここに入力'}
            ),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 2, 'cols': 70, 'placeholder': 'ここに入力'}
            ),
        }
