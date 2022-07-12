from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Post, Photo
from .forms import PostForm, EditForm
from django.urls import reverse_lazy
import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'ublog-11'

class HomeView(ListView):
  model = Post
  template_name = 'home.html'
  ordering = ['-post_date']

  def get_context_data(self, *args, **kwargs):
    cat_menu = Category.objects.all()
    context = super(HomeView, self).get_context_data(*args, **kwargs)
    context['cat_menu'] = cat_menu
    return context

class ArticleDetailView(DetailView):
  model = Post
  template_name = 'article_details.html'
  def get_context_data(self, *args, **kwargs):
    cat_menu = Category.objects.all()
    context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
    context['cat_menu'] = cat_menu
    return context

class AddPostView(CreateView):
  model = Post
  form_class = PostForm
  template_name = 'add_post.html'

class AddCategoryView(CreateView):
  model = Category
  template_name = 'add_category.html'
  fields = '__all__'

class UpdatePostView(UpdateView):
  model = Post
  form_class = EditForm
  template_name = 'update_post.html'

class DeletePostView(DeleteView):
  model = Post
  template_name = 'delete_post.html'
  success_url = reverse_lazy('home')

def CategoryView(request, categories):
  category_posts = Post.objects.filter(category=categories.replace('-', ' '))
  return render(request, 'categories.html', {'categories':categories.title().replace('-', ' '), 'category_posts':category_posts})

def CategoryListView(request):
  cat_menu_list = Category.objects.all()
  return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})


def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)