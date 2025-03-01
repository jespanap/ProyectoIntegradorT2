from django.core.management.base import BaseCommand
from movie.models import Movie
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Ruta del archivo JSON
        json_file_path = 'movie/management/commands/movies.json'
        
        # Cargar datos del archivo JSON
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        count = 0  # Contador de películas agregadas
        
        for i in range(min(100, len(movies))):
            movie = movies[i]
            
            # Verificar si la película ya existe
            exist = Movie.objects.filter(title=movie.get('title', '')).first()
            if not exist:
                description = movie.get('plot', 'No description available.')
                
                # Si `plot` existe pero es None, asignamos un string vacío
                if description is None:
                    description = 'No description available.'

                # Crear la película
                Movie.objects.create(
                    title=movie.get('title', 'Unknown Title'),
                    image='movie/images/default.jpg',
                    genre=movie.get('genre', 'Unknown Genre'),
                    year=movie.get('year', None),
                    description=description  # Aseguramos que nunca sea None
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} movies to the database'))
