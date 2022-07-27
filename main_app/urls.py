from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('characters/', views.characters_index, name='index'),
  path('characters/<int:character_id>/', views.character_detail, name='detail'),
  path('characters/<int:character_id>/level_up/<int:skill_id>/<str:correct>/<str:answer>/', views.verify_answer, name='level_up'),
  path('characters/create/', views.CharacterCreate.as_view(), name='character_create'),
  path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='character_update'),
  path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='character_delete'),
  path('characters/<int:character_id>/assoc_tamagotchi/<int:tamagotchi_id>/', views.assoc_tamagotchi, name='assoc_tamagotchi'),
  path('characters/<int:character_id>/disassoc_tamagotchi/<int:tamagotchi_id>/', views.disassoc_tamagotchi, name='disassoc_tamagotchi'),
  path('tamagotchis/', views.TamagotchiList.as_view(), name='tamagotchi_index'),
  path('tamagotchis/<int:tamagotchi_id>/', views.TamagotchiDetail, name='tamagotchi_detail'),
  path('tamagotchis/create/', views.TamagotchiCreate.as_view(), name='tamagotchi_create'),
  path('tamagotchis/<int:pk>/update/', views.TamagotchiUpdate.as_view(), name='tamagotchi_update'),
  path('tamagotchis/<int:pk>/delete/', views.TamagotchiDelete.as_view(), name='tamagotchi_delete'),
  path('tamagotchis/<int:tamagotchi_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('tamagotchis/<int:tamagotchi_id>/add_photo/', views.add_photo, name='add_photo'), 
  path('accounts/signup/', views.signup, name='signup')
]