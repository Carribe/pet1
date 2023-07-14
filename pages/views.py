from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import os
import random

from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *

from pet import settings
from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import PagesSerializer

menu1 = [
    {'title': "0 сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]

def image_files():
    static_path = os.path.join(settings.BASE_DIR, 'pages/static/images')  # Замените на ваш путь к папке "static"
    image_files = os.listdir(static_path)
    return image_files

class IndexView(ListView):
    template_name = "pages/page.html"
    context_object_name = "posts"
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        # Получаем список файлов из папки images
        static_path = os.path.join(settings.BASE_DIR, 'pages/static/images')
        image_files = os.listdir(static_path)

        # Фильтруем файлы, оставляя только те, которые начинаются с 'banner'
        image_files_filtered = [file for file in image_files if file.startswith('banner')]

        # Получаем список всех опубликованных постов
        posts = Page.objects.filter(is_published=True).select_related('belong_to').prefetch_related('belong_to')

        # Для каждого поста выбираем случайное изображение из списка
        for post in posts:
            random_image = random.choice(image_files_filtered)
            post.random_image = random_image

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем список файлов из папки images
        static_path = os.path.join(settings.BASE_DIR, 'pages/static/images')
        image_files = os.listdir(static_path)

        # Фильтруем файлы, оставляя только те, которые начинаются с 'banner'
        image_files_filtered = [file for file in image_files if file.startswith('banner')]

        # Получаем список опубликованных постов
        posts = self.get_queryset()

        if len(posts) == 0 or len(image_files_filtered) == 0:
            raise Http404()

        # Выбираем случайные изображения для каждого поста
        random_images = random.choices(image_files_filtered, k=min(len(image_files_filtered), len(posts)))
        for i, post in enumerate(posts):
            post.random_image = random_images[i % len(random_images)]

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["random_image"] = random_images[0]
        context["posts"] = page_obj
        context["cats"] = FilmType.objects.all()
        context["cat_selected"] = 0
        context["title"] = "My Pet Page"
        context["menu"] = menu1

        return context


class ShowCategoryView(ListView):
    template_name = "pages/page.html"
    context_object_name = "posts"
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id')
        return Page.objects.filter(is_published=True).select_related('belong_to').prefetch_related('belong_to')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем список файлов из папки images
        static_path = os.path.join(settings.BASE_DIR, 'pages/static/images')
        image_files = os.listdir(static_path)

        # Фильтруем файлы в зависимости от выбранной категории
        cat_id = self.kwargs.get('cat_id')
        if cat_id == 1:
            image_files_filtered = [file for file in image_files if file.startswith('bw')]
        elif cat_id == 2:
            image_files_filtered = [file for file in image_files if file.startswith('banner')]
        else:
            image_files_filtered = []

        # Получаем список опубликованных постов
        posts = self.get_queryset()

        if len(posts) == 0 or len(image_files_filtered) == 0:
            raise Http404()

        # Выбираем случайные изображения для каждого поста
        random_images = random.choices(image_files_filtered, k=min(len(image_files_filtered), len(posts)))
        for i, post in enumerate(posts):
            post.random_image = random_images[i % len(random_images)]

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["random_image"] = random_images[0]
        context["posts"] = page_obj
        context["cats"] = FilmType.objects.all()
        context["cat_selected"] = cat_id
        context["title"] = "Film type"
        context["menu"] = menu1

        return context

class ShowPageView(DetailView):
    model = Page
    template_name = "pages/generic_page.html"
    context_object_name = "page"
    slug_url_kwarg = "page_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prefix = 'bw' if self.object.belong_to_id == 1 else 'banner'
        image_files_filtered = [file for file in image_files() if file.startswith(prefix)]
        random_image = random.choice(image_files_filtered) if image_files_filtered else ''

        context["random_image"] = random_image
        context["cat_selected"] = self.object.belong_to_id
        context["title"] = self.object.title
        context["menu"] = menu1

        return context


class AddPageView(LoginRequiredMixin, CreateView):
    template_name = "pages/add_page.html"
    form_class = AddPostForm
    success_url = reverse_lazy('HomeForRedirect')  # Указываем URL-адрес для перенаправления после успешного создания объекта
    login_url = "/admin/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add some one"
        context["menu"] = menu1
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "pages/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["menu"] = menu1
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("HomeForRedirect")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "pages/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        context["menu"] = menu1
        return context

    def get_success_url(self):
        return reverse_lazy("HomeForRedirect")

def about(request):
    context = {
        "title": "About Pet Project",
        "menu": menu1
    }
    return render(request, "pages/about.html", context=context)



# def contact(request):
#     return HttpResponse("Контакты")

class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pages/footer.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_selected"] = 0
        context["title"] = "My Pet Page"
        context["menu"] = menu1

        return context

        # Эмуляция отправки сообщения в терминал
        print(f'Name: {name}')
        print(f'Email: {email}')
        print(f'Message: {message}')

        return render(request, 'pages/footer.html')


def logout_user(request):
    logout(request)
    return redirect("login")


def page_not_found(request, exception):
    return HttpResponseNotFound("404404404")


# class PagesViewSet(viewsets.ModelViewSet):
#     queryset = Page.objects.all()
#     serializer_class = PagesSerializer
#     lookup_field = 'slug'
#
#     def get_queryset(self):
#         slug = self.kwargs.get("slug")
#
#         if not slug:
#             return Page.objects.all()[:3]
#         return Page.objects.filter(slug=slug)
#
#     @action(methods=['get'], detail=False)
#     def category(self, request, pk=None):
#         cats = FilmType.objects.all()
#
#         return Response ({'cats': [c.name for c in cats]})


class PagesAPIList(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PagesAPIUpdate(generics.UpdateAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PagesAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly,)


class WomenAPIDestroy (generics. RetrieveDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)