# movie_app/urls.py

from django.urls import path
from .views import FilmesAPIView  # Importe a view que você criou

urlpatterns = [
    path('filmes/', FilmesAPIView.as_view(), name='filmes-api'),  # Rota para a sua API
]
