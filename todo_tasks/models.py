from django.db import models

# Create your models here.
class userModel(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username


class ToDoModel(models.Model):
    User = models.ForeignKey(userModel, on_delete=models.CASCADE, blank=True, null=True)
    task = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.task