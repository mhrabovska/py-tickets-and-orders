from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession

User = get_user_model()

def create_order(tickets: list[dict], username: str, date=None):
    """Створює замовлення та квитки всередині транзакції."""
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date if date else None)

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

    return order

def get_orders(username=None):
    """Повертає всі замовлення або замовлення конкретного користувача."""
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
