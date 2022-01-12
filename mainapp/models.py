from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     name = models.CharField(max_length=32, unique=True)
#     phone = models.CharField(max_length=32)
#     email = models.EmailField(unique=True)
# 
#     def __str__(self):
#         return self.name


class Article(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField()
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=32, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ToDo(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


    # def __str__(self):
    #     return self.title
