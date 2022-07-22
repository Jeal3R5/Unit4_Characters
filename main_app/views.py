from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Character, Tamagotchi, Skill, Photo
from .forms import FeedingForm
# Create your views here.

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'characters-cj-2022'

# For API Consumption
categories = ['science', 'music', 'sport_and_leisure', 'arts_and_literature']

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class CharacterCreate(LoginRequiredMixin, CreateView):
  model = Character
  fields = [
    'sex', 
    'name',
  ]

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class CharacterUpdate(LoginRequiredMixin, UpdateView):
  model = Character
  fields = [
    'sex', 
    'name',
  ]

class CharacterDelete(LoginRequiredMixin, DeleteView):
  model = Character
  success_url = '/characters/'

@login_required
def characters_index(request):
  characters = Character.objects.filter(user=request.user)
  return render(request, 'characters/index.html', {'characters':characters})

@login_required
def character_detail(request, character_id):
  character = Character.objects.get(id=character_id)
  all_skills = []

  for cat in categories:
    all_skills.append([Skill.create(cat,0), Skill.get_quiz(cat)])

  return render(request, 'characters/detail.html', {'character':character, 'all_skills':all_skills})

class TamagotchiList(LoginRequiredMixin, ListView):
  model = Tamagotchi

class TamagotchiDetail(LoginRequiredMixin, DetailView):
  model = Tamagotchi

class TamagotchiCreate(LoginRequiredMixin, CreateView):
  model = Tamagotchi
  fields = '__all__'

class TamagotchiUpdate(LoginRequiredMixin, UpdateView):
  model = Tamagotchi
  fields = ['name', 'pet_type', 'pet_age']

class TamagotchiDelete(DeleteView):
  model = Tamagotchi
  success_url: '/tamagotchis/'
  
@login_required
def add_photo(request, tamagotchi_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, tamagotchi_id=tamagotchi_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', tamagotchi_id=tamagotchi_id)


@login_required
def assoc_tamagotchi(request, character_id, tamagotchi_id):
  Character.objects.get(id=character_id).tamagotchis.add(tamagotchi_id)
  return redirect('detail', character_id=character_id)

@login_required
def add_feeding(request, tamagotchi_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.tamagotchi_id = tamagotchi_id
    new_feeding.save()
  return redirect('tamagotchi_detail', tamagotchi_id=tamagotchi_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = "Invalid sign up - please try again"
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

