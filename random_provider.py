"""Random provider abstraction for testability"""
import random
from abc import ABC, abstractmethod
from typing import TypeVar, List

T = TypeVar('T')


class RandomProvider(ABC):
    """Abstract base class for random providers"""
    
    @abstractmethod
    def choice(self, sequence: List[T]) -> T:
        """Choose a random element from a non-empty sequence"""
        pass


class SystemRandomProvider(RandomProvider):
    """Real system random provider"""
    
    def choice(self, sequence: List[T]) -> T:
        """Choose a random element using system random"""
        return random.choice(sequence)


class MockRandomProvider(RandomProvider):
    """Mock random provider for testing"""
    
    def __init__(self, predetermined_choices: List[T] = None):
        self._predetermined_choices = predetermined_choices or []
        self._choice_index = 0
    
    def choice(self, sequence: List[T]) -> T:
        """Return predetermined choices or the first element"""
        if self._predetermined_choices:
            result = self._predetermined_choices[self._choice_index]
            self._choice_index = (self._choice_index + 1) % len(self._predetermined_choices)
            return result
        # Default: return first element
        return sequence[0] if sequence else None
    
    def set_choices(self, choices: List[T]):
        """Set predetermined choices for testing"""
        self._predetermined_choices = choices
        self._choice_index = 0
