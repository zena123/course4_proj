from django.db import models

from django.contrib.auth import get_user_model


class Profile(models.Model):

  user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
  token = models.TextField()

  def __str__(self):
    return f"Profile for {self.user.username}"

