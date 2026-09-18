"""
Базовый дескриптор для валидации полей.
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
