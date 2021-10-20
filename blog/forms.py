from django import forms
from .models import Post


class PostFormBase(forms.ModelForm):
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


class PostCreateForm(PostFormBase):
    pass


class PostUpdateForm(PostFormBase):
    pass
