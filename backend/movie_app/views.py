from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from django.http import JsonResponse
import pandas as pd

class FilmesAPIView(APIView):
    def get(self, request):
        nome_filme = request.query_params.get('filme')  # Captura o nome do filme da query string
        return JsonResponse(self.lista_filme(nome_filme), safe=False)
        
    
    def dados_filme(self, nome_filme): #api para coletar informacoes completas de filmes
        response = requests.get(f'http://www.omdbapi.com/?t={nome_filme}&apikey=e982fb10')
        
        if response.status_code == 200:
            return response.json()
        
        return None
    
    def lista_filme(self, nome_filme): #pegando a lista de filmes do csv
        caminho= os.path.join(settings.BASE_DIR, 'static', 'csv', 'filmes.csv')
        df = pd.read_csv(caminho)
        resultados = df[df['title'].notna() & df['title'].str.contains(nome_filme, case=False)]
        
        if not resultados.empty:
            titulos = resultados['title'].tolist() #transformando o df em list

            informacoes_filme = [] #pegando as informacoes completas de cada filme da lista
            for titulo in titulos:
                informacao = self.dados_filme(titulo)
                if informacao:
                    informacoes_filme.append(informacao)
            
            return informacoes_filme
        else:
            return None