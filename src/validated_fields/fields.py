"""
Дескрипторы для строковых и целочисленных полей.
"""

from .field import Field


class StringField(Field):
    """Дескриптор для строковых полей с проверкой минимальной длины."""

    def __init__(self, min_length:int=0):
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
