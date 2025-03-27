"""
Manager for dependency injection container
"""

from app.core.interfaces.di import IDIContainer
from typing import Dict, Type, TypeVar, Optional, Callable

T = TypeVar('T')


class DIContainerManager(IDIContainer):
    """
    Singleton manager for dependency injection container
    """

    _instance: Optional[IDIContainer] = None

    def __init__(self) -> None:
        if not hasattr(self, '_services'):
            self._services: Dict[Type[T], T] = {}
        if not hasattr(self, '_factories'):
            self._factories: Dict[Type[T], Callable[[], T]] = {}

    def __new__(cls) -> IDIContainer:
        if cls._instance is None:
            cls._instance = super(DIContainerManager, cls).__new__(cls)
        return cls._instance

    def register(self,
                 service_type: Type[T],
                 instance: T) -> None:
        if isinstance(instance, service_type):
            self._services[service_type] = instance
        else:
            raise ValueError(
                f"Instance of {type(service_type)} "
                f"is not of type {service_type}")

    def register_factory(self,
                         service_type: Type[T],
                         factory: Callable[[], T]) -> None:
        self._factories[service_type] = factory

    def get(self,
            service_type: Type[T]) -> Optional[T]:

        if service_type in self._services:
            return self._services[service_type]

        if service_type in self._factories:
            instance = self._factories[service_type]()
            return instance

        return None

    def has(self,
            service_type: Type[T]) -> bool:
        return (service_type in self._services or
                service_type in self._factories)

    def remove(self,
               service_type: Type[T]) -> None:
        if service_type in self._services:
            del self._services[service_type]
        if service_type in self._factories:
            del self._factories[service_type]

    def clear(self) -> None:
        self._services.clear()
        self._factories.clear()
