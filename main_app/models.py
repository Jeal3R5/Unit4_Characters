from unicodedata import category
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
import requests


MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

TAMAGOTCHIS_TYPE = (
    ('A', 'Kuchipatchi'), 
    ('B', 'Memetchi'), 
    ('C', 'Momotchi'), 
    ('D', 'Mametchi')
)

SEX = (
    ('M', 'Male'),
    ('F', 'Female')
)

categories = ['science', 'music', 'sport_and_leisure', 'arts_and_literature']

# Create your models here.

class Tamagotchi(models.Model):
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100, choices=TAMAGOTCHIS_TYPE, default=TAMAGOTCHIS_TYPE[0])
    pet_age = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamagotchi_detail', kwargs={'tamagotchi_id':self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Character(models.Model):
    sex = models.CharField(max_length=1, choices=SEX, default=SEX[0][0])
    name = models.CharField(max_length=100)
    tamagotchis = models.ManyToManyField(Tamagotchi)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            for category in categories:
                Skill.objects.create(name=category, level=0,character=self)
            
    def get_absolute_url(self):
        return reverse("detail", kwargs={"character_id": self.id})

class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    tamagotchi = models.ForeignKey(Tamagotchi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}."
    
    class Meta:
        ordering = ["-date"]
    

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, level):
        skill = cls(name=name, level=level)
        return skill

    @property
    def level_up(self):
        self.level += 1

    @property
    def get_quiz(self):
        quiz = {}
        endpoint = 'https://the-trivia-api.com/api/questions?categories={category}&limit=1&difficulty=easy'
        url = endpoint.format(category=self.name)
        response = requests.get(url)
        quiz = response.json()
        return quiz

class Photo(models.Model):
    url = models.CharField(max_length=200)
    tamagotchi = models.ForeignKey( Tamagotchi, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
    
