from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username} profili"

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(force_insert=force_insert, force_update=force_update, *args, **kwargs)

        img = Image.open(self.image.path) # Open image

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path)