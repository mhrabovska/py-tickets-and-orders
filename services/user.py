from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username, password, email=None, first_name=None, last_name=None):
    """Створення нового користувача з зашифрованим паролем."""
    user = User.objects.create_user(username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user

def get_user(user_id):
    """Отримання користувача за його ID."""
    return User.objects.get(id=user_id)

def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    """Оновлення даних користувача."""
    user = User.objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)  # Шифрування нового пароля
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username, password, email=None, first_name=None, last_name=None):
    """Створення нового користувача з зашифрованим паролем."""
    user = User.objects.create_user(username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user

def get_user(user_id):
    """Отримання користувача за його ID."""
    return User.objects.get(id=user_id)

def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    """Оновлення даних користувача."""
    user = User.objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)  # Шифрування нового пароля
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user
