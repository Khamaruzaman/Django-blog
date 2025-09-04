from django.db import transaction

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BlogSearchForm
from .models import Post
from users.tasks import send_notification


# def home(request):
#     context = {
#         "posts": Post.objects.all(),
#         "title": "home",
#     }
#     return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=self.user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.user
        return context


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            f"Your post has been created successfully! ({form.instance.title})",
        )

        transaction.on_commit(lambda: send_notification.delay(self.request.user.id, "Your blog post was successfully created!"))
        
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, f"Your post has been updated! ({form.instance.title})"
        )
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog-home")

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


def about(request):
    return render(request, "blog/about.html", {"title": "about"})


class BlogSearchListView(ListView):
    model = Post
    template_name = "blog/blog_search_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get("query", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BlogSearchForm(self.request.GET or None)
        context["query"] = self.request.GET.get("query", "").strip()

        params = self.request.GET.copy()
        for key in ["page", "csrfmiddlewaretoken"]:
            if key in params:
                params.pop(key)
        context["querystring"] = params.urlencode()

        return context


class BlogAjaxSearchView(View):
    def get(self, request):
        query = request.GET.get("query", "").strip()
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).values("id", "title", "author__username", "date_posted")

        return JsonResponse(list(posts), safe=False)
