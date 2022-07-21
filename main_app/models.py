from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


MEAL = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.

class Tamagotchi(models.Model):
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    pet_age = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamagotchi_detail', kwargs={'pk':self.id})


class Character(models.Model):
    sex = models.CharField(max_length=1)
    name = models.CharField(max_length=100)
    tamagotchis = models.ManyToManyField(Tamagotchi)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"character_id": self.id})


class Feeding(models.Model):
    date = models.DateTimeField()
    meals = models.CharField(max_length=1, choices=MEAL, default=MEAL[0][0])
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.date
    
    class Meta:
        ordering = ["date"]
    

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    character = models.ForeignKey( Character, on_delete=CASCADE)

    def __str__(self):
        return self.url
    
