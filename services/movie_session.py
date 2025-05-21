from django.db.models import QuerySet
from django.db import transaction

from db.models import Movie, MovieSession, Ticket


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    movie_duration: int,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    if not isinstance(genres_ids, list) or not all(isinstance(g, int) for g in genres_ids):
        raise ValueError("Genres must be a list of integers.")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
        duration=movie_duration,
    )

    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    return movie


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    movie_session = MovieSession.objects.get(id=session_id)
    if show_time:
        movie_session.show_time = show_time
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id
    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id):
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id).values('row', 'seat')
    return list(tickets)
