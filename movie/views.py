from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io 
import urllib, base64

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)  
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
    
def statistics_view(request):  
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()

    #Gráfico 1: Películas por año
    movie_counts_by_year = {}

    for movie in all_movies:
        year = movie.year if movie.year else 'None'
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_years = base64.b64encode(image_png).decode('utf-8')

    # Gráfico 2: Películas por género (solo primer género)
    movie_counts_by_genre = {}

    for movie in all_movies:
        genre = movie.genre.split(',')[0].strip() if movie.genre else 'Unknown'
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center', color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png_genre = buffer.getvalue()
    buffer.close()
    graphic_genres = base64.b64encode(image_png_genre).decode('utf-8')

    return render(request, 'statistics.html', {
        'graphic': graphic_years,  
        'graphic_genres': graphic_genres  
    })