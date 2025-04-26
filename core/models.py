from django.db import models
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class MealHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100)
    total_cost = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.meal_name} - {self.total_cost}₺"