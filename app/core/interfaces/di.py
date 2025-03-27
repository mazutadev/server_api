"""
Interface for dependency injection
"""

from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional, Callable

T = TypeVar('T')


class IDIContainer(ABC):
    """
    Interface for dependency injection container
    """

    @abstractmethod
    def register(self,
                 service_type: Type[T],
                 instance: T) -> None:
        """
        Register a service in the container

        Args:
            service_type: Type of the service to register
            instance: Instance of the service to register
        """
        pass

    @abstractmethod
    def register_factory(self,
                         service_type: Type[T],
                         factory: Callable[[], T]) -> None:
        """
        Register a factory for a service in the container

        Args:
            service_type: Type of the service to register
            factory: Factory function to create the service
        """
        pass

    @abstractmethod
    def get(self,
            service_type: Type[T]) -> Optional[T]:
        """
        Get a service from the container by type

        Args:
            service_type: Type of the service to get
        """
        pass

    @abstractmethod
    def has(self,
            service_type: Type[T]) -> bool:
        """
        Check if a service is registered in the container by type

        Args:
            service_type: Type of the service to check
        """
        pass

    @abstractmethod
    def remove(self,
               service_type: Type[T]) -> None:
        """
        Remove a service from the container by type

        Args:
            service_type: Type of the service to remove
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all services from the container
        """
        pass
