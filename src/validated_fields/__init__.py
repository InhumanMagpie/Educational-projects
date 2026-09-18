"""
Система валидации полей на основе дескрипторов.

Объединяет:
- Атрибуты класса и экземпляра
- Дескрипторы (__set_name__, __get__, __set__)
- __slots__ (опционально)
- Наследование и MRO
"""

from .field import Field
from .fields import StringField, IntegerField
from .model import ValidatedModel

__all__ = ["Field", "StringField", "IntegerField", "ValidatedModel"]
