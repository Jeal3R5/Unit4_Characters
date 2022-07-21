from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Character, Tamagotchi, Photo
# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class CharacterCreate(CreateView):
  model = Character
  fields = [
    'sex', 
    'name',
  ]

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class CharacterUpdate(UpdateView):
  model = Character
  fields = [
    'sex', 
    'name',
  ]

class CharacterDelete(DeleteView):
  model = Character
  success_url = '/characters/'

def characters_index(request):
  characters = Character.objects.filter(user=request.user)
  return render(request, 'characters/index.html', {'characters':characters})

def character_detail(request, character_id):
  character = Character.objects.get(id=character_id)

  feeding_form = FeedingForm()
  return render(request, 'characters/detail.html', {'character':character, 'feeding_form':feeding_form})

