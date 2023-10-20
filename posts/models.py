from django.db import models
from core.models import BaseModel, SoftDeleteModel, TimeStampMixin
from django.utils.translation import gettext_lazy as _
from Blaze.settings import AUTH_USER_MODEL
from django.urls import reverse
from django.db.models import Manager


class Tag(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

    def tag_post_count(self):
        return self.posts.count()


class Post(TimeStampMixin, SoftDeleteModel):
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(
        verbose_name=_("Title"), max_length=100, help_text=_("Title of post")
    )
    body = models.TextField(
        verbose_name=_("body"), max_length=700, help_text=_("Body of post")
    )
    slug = models.SlugField()
    tags = models.ManyToManyField("Tag", related_name="tags", blank=True, null=True)

    def __str__(self):
        return f"{self.author} wrote about {self.title}"

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=(self.id, self.slug))

    def likes_count(self):
        return self.plikes.count()

    def user_can_like(self, user):
        user_like = user.ulikes.filter(post=self)
        if user_like.exists():
            return True
        return False

    class Meta:
        ordering = ("-created_at",)


class PostRecycle(Post):
    objects = Manager()

    class Meta:
        proxy = True


class Like(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ulikes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="plikes")

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"


class Comment(TimeStampMixin, BaseModel):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ucomments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomments")
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="rcomments",
        blank=True,
        null=True,
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"


