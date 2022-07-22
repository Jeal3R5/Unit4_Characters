from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('characters/', views.characters_index, name='index'),
  path('characters/<int:character_id>/', views.character_detail, name='detail'),
  path('characters/create/', views.CharacterCreate.as_view(), name='character_create'),
  path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='character_update'),
  path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='character_delete'),
  path('characters/<int:character_id>/assoc_tamagotchi/<int:tamagotchi_id>/', views.assoc_tamagotchi, name='assoc_tamagotchi'),
  path('tamagotchis/', views.TamagotchiList.as_view(), name='tamagotchi_index'),
  path('tamagotchis/<int:pk>/', views.TamagotchiDetail.as_view(), name='tamagotchi_detail'),
  path('tamagotchis/create/', views.TamagotchiCreate.as_view(), name='tamagotchi_create'),
  path('tamagotchis/<int:pk>/update/', views.TamagotchiUpdate.as_view(), name='tamagotchi_update'),
  path('tamagotchis/<int:pk>/delete/', views.TamagotchiDelete.as_view(), name='tamagotchi_delete'),
  path('tamagotchis/<int:tamagotchi_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('tamagotchis/<int:tamagotchi_id>/add_photo/', views.add_photo, name='add_photo'), 
  # path('skills/', views.skills_index, name='skill_index'),
  # path('skills/<int:skill_id>/', views.skills_detail, name='skill_detail'),
  path('/quiz', views.get_quiz, name='quiz'),
  path('accounts/signup/', views.signup, name='signup')
]