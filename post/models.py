from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from autoslug import AutoSlugField
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Category(HitCountMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home", args=[str(self.name)])


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(HitCountMixin, models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(max_length=200, unique=True, populate_from='title')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='post_pics', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} | {self.author}"

    def get_absolute_url(self):
        return reverse("home")

    def save(self, *args, **kwargs):
        # Set the default category if it's not already set
        if not self.category:
            default_category = Category.objects.get_or_create(name="Uncategorized")[0]
            self.category = default_category
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


