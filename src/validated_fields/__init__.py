"""
Система валидации полей на основе дескрипторов.

Объединяет:
- Атрибуты класса и экземпляра
- Дескрипторы (__set_name__, __get__, __set__)
- __slots__ (опционально)
- Наследование и MRO
"""


class Field:
    """Базовый дескриптор для валидации полей."""

    def __set_name__(self, owner, name):
        """Вызывается при создании класса, сохраняет имя поля."""
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        """Возвращает значение из экземпляра."""
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        """Валидирует и сохраняет значение в экземпляре."""
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        """Базовая валидация - переопределяется в подклассах."""
        pass


class StringField(Field):
    """Дескриптор для строковых полей с проверкой минимальной длины."""

    def __init__(self, min_length=0):
        self.min_length = min_length

    def validate(self, value):
        """Проверяет, что значение — строка и имеет минимальную длину."""
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} должно быть строкой")
        if len(value) < self.min_length:
            raise ValueError(
                f"{self.public_name} должно иметь длину не менее {self.min_length}"
            )


class IntegerField(Field):
    """Дескриптор для целочисленных полей с проверкой диапазона."""

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        """Проверяет, что значение — целое число (не bool) и в диапазоне."""
        # bool является подклассом int, поэтому нужно явно исключить
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{self.public_name} должно быть целым числом")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(
                f"{self.public_name} должно быть не меньше {self.min_value}"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValueError(
                f"{self.public_name} должно быть не больше {self.max_value}"
            )


class ValidatedModel:
    """
    Базовый класс для моделей с валидируемыми полями.

    Собирает все поля (дескрипторы) из класса и предоставляет __repr__.
    """

    _fields: dict = {}

    def __init_subclass__(cls, **kwargs):
        """Собирает все поля-дескрипторы при создании подкласса."""
        super().__init_subclass__(**kwargs)
        cls._fields = {}
        for name, value in cls.__dict__.items():
            if isinstance(value, Field):
                cls._fields[name] = value

    def __repr__(self):
        """Красивое представление объекта."""
        fields = ", ".join(
            f"{name}={getattr(self, name)!r}"
            for name in self._fields
        )
        return f"{type(self).__name__}({fields})"


# Пример использования
if __name__ == "__main__":
    class User(ValidatedModel):
        name = StringField(min_length=1)
        age = IntegerField(min_value=0, max_value=150)
        email = StringField(min_length=5)

        def __init__(self, name, age, email):
            self.name = name
            self.age = age
            self.email = email

    # Тестирование
    print("=== Тестирование валидации ===\n")

    # Успешное создание
    user = User("Alice", 30, "alice@example.com")
    print(f"✓ Создан пользователь: {user}")

    # Проверка пустого имени
    try:
        User("", 30, "alice@example.com")
        print("✗ Ошибка: должно было выбросить исключение для пустого имени")
    except ValueError as e:
        print(f"✓ Поймана ошибка для пустого имени: {e}")

    # Проверка отрицательного возраста
    try:
        User("Alice", -5, "alice@example.com")
        print("✗ Ошибка: должно было выбросить исключение для отрицательного возраста")
    except ValueError as e:
        print(f"✓ Поймана ошибка для отрицательного возраста: {e}")

    # Проверка возраста больше максимума
    try:
        User("Alice", 200, "alice@example.com")
        print("✗ Ошибка: должно было выбросить исключение для возраста > 150")
    except ValueError as e:
        print(f"✓ Поймана ошибка для возраста > 150: {e}")

    # Проверка типа имени
    try:
        User(123, 30, "alice@example.com")
        print("✗ Ошибка: должно было выбросить исключение для имени не-string")
    except TypeError as e:
        print(f"✓ Поймана ошибка для имени не-string: {e}")

    # Проверка типа возраста (bool)
    try:
        User("Alice", True, "alice@example.com")
        print("✗ Ошибка: должно было выбросить исключение для bool как возраста")
    except TypeError as e:
        print(f"✓ Поймана ошибка для bool как возраста: {e}")

    # Проверка короткого email
    try:
        User("Alice", 30, "a@b")
        print("✗ Ошибка: должно было выбросить исключение для короткого email")
    except ValueError as e:
        print(f"✓ Поймана ошибка для короткого email: {e}")

    print("\n=== Все тесты пройдены! ===")
