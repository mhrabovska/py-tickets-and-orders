from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions"
    )

    def __str__(self):
        return self.username


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Автоматично фіксуємо дату створення
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Зв'язок із користувачем

    class Meta:
        ordering = ['-created_at']  # Сортування від найновіших до найстаріших

    def __str__(self):
        return f"<Order: {self.created_at}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey('MovieSession', on_delete=models.CASCADE)  # Зв'язок із сеансом
    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Зв'язок із замовленням
    row = models.IntegerField()  # Номер ряду
    seat = models.IntegerField()  # Номер місця

    class Meta:
        ordering = ['movie_session__show_time']  # Сортуємо за часом сеансу
        constraints = [
            models.UniqueConstraint(fields=['movie_session', 'row', 'seat'], name='unique_ticket_per_seat')
        ]  # Кожен квиток у певному сеансі має бути унікальним для місця

    def __str__(self):
        return f"<Ticket: {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})>"

    def clean(self):
        """Перевіряємо, чи ряд та місце у допустимих межах"""
        max_rows = self.movie_session.cinema_hall.rows
        max_seats = self.movie_session.cinema_hall.seats_in_row

        if not (1 <= self.row <= max_rows):
            raise ValidationError({'row': [f'row number must be in available range: (1, rows): (1, {max_rows})']})

        if not (1 <= self.seat <= max_seats):
            raise ValidationError({'seat': [f'seat number must be in available range: (1, seats_in_row): (1, {max_seats})']})

    def save(self, *args, **kwargs):
        """Перед збереженням викликаємо clean(), щоб перевірити дані"""
        self.full_clean()
        super().save(*args, **kwargs)
