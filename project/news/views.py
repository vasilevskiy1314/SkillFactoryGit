from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 3  # поставим постраничный вывод в один элемент
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()
        return super().get(request, *args, **kwargs)


class PostSearch(ListView):
    model = Post
    template_name = 'news_app/post_search.html'
    context_object_name = 'posts'
    ordering = ['dateCreation']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    template_name = 'news_app/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_time_creation'] = self.object.dateCreation.strftime("%d-%B-%Y %H:%M")
        return context


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news_app/post_update.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'news_app/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('news.delete_post')
