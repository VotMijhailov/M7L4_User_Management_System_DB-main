import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""

# Тест добавления пользователя с существующим логином.
def test_add_users(setup_database, connection):
    add_user("testuser2", "testuser@example.ry", 'password123')
    result = add_user("testuser2", "testuser@example.ry", 'pass123')
    assert result == False

# Тест успешной аутентификации пользователя.
def test_authenticate_user(setup_database, connection):
    add_user("testuser2", "testuser@example.ry", 'password123')
    result1 = authenticate_user("testuser2", 'pass123')
    assert result1 == False

# Тест аутентификации несуществующего пользователя.
def test_NOT_authenticated_user(setup_database, connection):
    result2 = authenticate_user("testuser2", 'pass123')
    assert result2 == False

# Тест аутентификации пользователя с неправильным паролем.
def test_authenticated_user_with_NOT_incorrect_password(setup_database, connection):
    add_user("testuser2", "testuser@example.ry", 'password123')
    result3 = authenticate_user("testuser2", 'pass123')
    assert result3 == False
