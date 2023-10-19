from django.views import View
from django.shortcuts import render
from .models import Post


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.filter(is_active=True)
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])
            return render(
                request, "posts/home.html", {"posts": posts, "form": self.form_class}
            )
