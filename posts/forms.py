from django import forms
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
#from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Post
from taggit.forms import TagWidget


def make_slug(instance, new_slug=None):
    """Function for creating unique slugs"""

    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    # check if there exists a post with existing slug
    q = Post.objects.filter(slug=slug)
    if q.exists():
        new_slug = "-".join([slug, get_random_string(4, "0123456789")])
        return make_slug(instance, new_slug=new_slug)
    return slug

"""
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'created', 'updated', 'published')
        widgets = {
            'body': CKEditorUploadingWidget(),
            'snippet': CKEditorUploadingWidget(config_name='small'),
        }
"""

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ( "slug", "author", "created", "updated", "published")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Type your title here...",
                    "class": "form-control",
                }
            ),
            "category": forms.SelectMultiple(
                attrs={"required": True, "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "allow_comments": forms.CheckboxInput(attrs={"class": "form-control"}),
            "tags": TagWidget(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        slug = cleaned_data.get("slug")

        if not slug and title:
            print(title)
            cleaned_data["slug"] = slugify(title)
            cleaned_data["published"] = timezone.now()
            cleaned_data["updated"] = timezone.now()
            print(cleaned_data)

        return cleaned_data

    def save(self, commit=True):
        print(commit)
        instance = super().save(commit=False)
        instance.slug = make_slug(instance)

        if commit:
            instance.save()
            self.save_m2m()
        return instance
