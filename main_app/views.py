from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DeleteView
from .models import Character, Tamagotchi, Photo
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Character, Tamagotchi, Skills, Photo
from .forms import FeedingForm
# Create your views here.

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