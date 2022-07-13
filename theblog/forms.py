from django import forms
from .models import Post, Category


# selection_list = []
# selections = Category.objects.all().values_list('name','name')
# for item in selections:
#   selection_list.append(item)

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'title_tag', 'author', 'category', 'body')

    widgets = {
      'title':forms.TextInput(attrs={'class':'form-control'}),
      'title_tag':forms.TextInput(attrs={'class':'form-control'}),
      'author':forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'user', 'type':'hidden'}),
      # 'category':forms.Select(choices=selection_list, attrs={'class':'form-control'}),
      'body':forms.Textarea(attrs={'class':'form-control'}),
    }

class EditForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'title_tag', 'body')

    widgets = {
      'title':forms.TextInput(attrs={'class':'form-control'}),
      'title_tag':forms.TextInput(attrs={'class':'form-control'}),
      'body':forms.Textarea(attrs={'class':'form-control'}),
    }