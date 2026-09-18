"""
Базовый класс для моделей с валидируемыми полями.
"""

from .field import Field


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
