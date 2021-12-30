from django.forms import fields
from django.forms import widgets
from django.forms.widgets import TextInput
from django.http import request
from .models import Category, Comment, Post, Tag
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'email', 'author']


class AddTagForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3, error_messages={
                            'required': 'title is required !'})

    def save(self):
        Tag.objects.create(title=self.cleaned_data['title'])


class DeleteTagForm(forms.Form):
    class Meta:
        model = Tag
        fields = []


class EditTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class SearchTitle(forms.Form):
    searched_text = forms.CharField(max_length=50)


class DeletePostForm(forms.Form):
    class Meta:
        model = Post
        fields = []


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['writer']
        fields = ['title' , 'shortDescription' , 'Text' , 'image' , 'category' , 'tag' , 'slug']

    widgets = {
        'title': forms.TextInput(attrs= {'class':'form-control'}),
        'shortDescription': forms.TextInput(attrs= {'class':'form-control'}),
        'Text': forms.TextInput(attrs= {'class':'form-control'}),
        'image': forms.FileInput(attrs= {'style':'display: none;','class':'form-control', 'required': False})
    }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['writer']
        fields = ['title' , 'shortDescription' , 'Text' , 'image' , 'category' , 'tag' , 'slug']

    widgets = {
        'title': forms.TextInput(attrs= {'class':'form-control'}),
        'shortDescription': forms.TextInput(attrs= {'class':'form-control'}),
        'Text': forms.TextInput(attrs= {'class':'form-control'}),
        'image': forms.FileInput(attrs= {'style':'display: none;','class':'form-control', 'required': False})
    }
 # TODO
 # write view of this


class AddCategoryForms(forms.ModelForm):

    category_choice_parent = Category.objects.all()

    title = forms.CharField(max_length=50, min_length=4, required=True)
    parent = forms.MultipleChoiceField(
        widget=forms.CheckboxInput, required=False, choices=category_choice_parent)

    def save(self):
        Category.objects.create(
            title=self.cleaned_data['title'], parent=self.cleaned_data['parent'])


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class DeleteCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
