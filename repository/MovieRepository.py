from model.Movie import Movie
from repository.exceptions import MovieNotFoundException, MovieTitleExistsException


class MovieRepository():
    _movie_id_counter: int = 0
     _movies = {}
    _movies_by_title = {}

    @classmethod
    def create_movie(cls, title: str, year:int, genre: str, view_count: int | None = None) -> Movie:
        if title.lower() in cls._movies_by_title:
            raise MovieTitleExistsException(f"Movie {title} already exists")

        cls._movie_id_counter += 1

        movie = Movie(id=cls._movie_id_counter, title=title, year=year, genre=genre)
        if (view_count is not None):
            movie.view_count = view_count

        cls._movies[movie.id] = movie
        cls._movies_by_title[movie.title.lower()] = movie

        return movie

    @classmethod
    def delete_movie(cls, id: int):
        movie_to_delete = cls._movies.get(id)

        if not movie_to_delete:
            raise MovieNotFoundException(f"Фільм з ID {id} не знайдено.")

        del cls._movies[id]
        del cls._movies_by_title[movie_to_delete.title.lower()]

    @classmethod
    def delete_all_movies(cls):
        cls._movies.clear()

    @classmethod
    def get_movie(cls, id: int) -> Movie:
        movie = cls._movies.get(id)
        if not movie:
            raise MovieNotFoundException(f"Фільм з ID {id} не знайдено.")
        return movie

    @classmethod
    def get_all_movies(cls) -> list[Movie]:
        return list(cls._movies.values())

    @classmethod
    def update_movie(cls, id: int, title: str, year: int, genre: str, view_count: int | None = None) -> Movie:
        movie_to_update = cls._movies.get(id)

        if not movie_to_update:
            raise MovieNotFoundException()

        new_title_lower = title.lower()
        old_title_lower = movie_to_update.title.lower()

        if new_title_lower != old_title_lower and new_title_lower in cls._movies_by_title:
            raise MovieTitleExistsException(f"Movie {title} already exists")

        del cls._movies_by_title[old_title_lower]

        movie_to_update.title = title
        movie_to_update.year = year
        movie_to_update.genre = genre
        if view_count is not None:
            movie_to_update.view_count = view_count

        cls._movies_by_title[new_title_lower] = movie_to_update

        return movie_to_update
    @classmethod
    def increment_view_count(cls, id: int) -> None:
        movie_to_update = cls._movies.get(id)
        movie_to_update.view_count += 1