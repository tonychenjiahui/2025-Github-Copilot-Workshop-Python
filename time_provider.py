"""Time provider abstraction for testability"""
import time
from abc import ABC, abstractmethod


class TimeProvider(ABC):
    """Abstract base class for time providers"""
    
    @abstractmethod
    def get_current_time(self) -> float:
        """Get the current time in seconds"""
        pass


class SystemTimeProvider(TimeProvider):
    """Real system time provider"""
    
    def get_current_time(self) -> float:
        """Get the current system time in seconds"""
        return time.time()


class MockTimeProvider(TimeProvider):
    """Mock time provider for testing"""
    
    def __init__(self, initial_time: float = 0.0):
        self._current_time = initial_time
    
    def get_current_time(self) -> float:
        """Get the mocked current time"""
        return self._current_time
    
    def advance(self, seconds: float):
        """Advance the mock time by the specified seconds"""
        self._current_time += seconds
    
    def set_time(self, time: float):
        """Set the mock time to a specific value"""
        self._current_time = time
