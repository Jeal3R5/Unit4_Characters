from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Character, Tamagotchi, Skills, Photo
from .forms import FeedingForm
# Create your views here.

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'characters-cj-2022'

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

  feeding_form = FeedingForm()
  return render(request, 'characters/detail.html', {'character':character, 'feeding_form':feeding_form})

class TamagotchiList(LoginRequiredMixin, ListView):
  model = Tamagotchi

class TamagotchiDetail(LoginRequiredMixin, DetailView):
  model = Tamagotchi

class TamagotchiCreate(LoginRequiredMixin, CreateView):
  model = Tamagotchi
  fields = '__all__'

class TamagotchiUpdate(LoginRequiredMixin, UpdateView):
  model = Tamagotchi
  fiels = ['name', 'pet_type', 'pet_age']

class TamagotchiDelete(DeleteView):
  model = Tamagotchi
  success_url: '/tamagotchis/'
  
@login_required
def add_photo(request, kdrama_id):
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
            photo = Photo(url=url, kdrama_id=kdrama_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', kdrama_id=kdrama_id)

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

