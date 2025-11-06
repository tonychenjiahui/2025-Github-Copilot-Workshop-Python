"""Unit tests for the time provider module"""
import unittest
from time_provider import TimeProvider, SystemTimeProvider, MockTimeProvider
import time


class TestSystemTimeProvider(unittest.TestCase):
    """Test cases for SystemTimeProvider"""
    
    def test_get_current_time_returns_float(self):
        """Test that get_current_time returns a float"""
        provider = SystemTimeProvider()
        current_time = provider.get_current_time()
        self.assertIsInstance(current_time, float)
    
    def test_get_current_time_advances(self):
        """Test that time advances between calls"""
        provider = SystemTimeProvider()
        time1 = provider.get_current_time()
        time.sleep(0.01)  # Sleep for 10ms
        time2 = provider.get_current_time()
        self.assertGreater(time2, time1)


class TestMockTimeProvider(unittest.TestCase):
    """Test cases for MockTimeProvider"""
    
    def test_initial_time_default(self):
        """Test that initial time defaults to 0.0"""
        provider = MockTimeProvider()
        self.assertEqual(provider.get_current_time(), 0.0)
    
    def test_initial_time_custom(self):
        """Test that initial time can be set"""
        provider = MockTimeProvider(initial_time=100.0)
        self.assertEqual(provider.get_current_time(), 100.0)
    
    def test_advance_time(self):
        """Test that time can be advanced"""
        provider = MockTimeProvider(initial_time=0.0)
        provider.advance(5.0)
        self.assertEqual(provider.get_current_time(), 5.0)
        provider.advance(3.5)
        self.assertEqual(provider.get_current_time(), 8.5)
    
    def test_set_time(self):
        """Test that time can be set to a specific value"""
        provider = MockTimeProvider(initial_time=0.0)
        provider.set_time(100.0)
        self.assertEqual(provider.get_current_time(), 100.0)
    
    def test_time_does_not_advance_automatically(self):
        """Test that mock time does not advance automatically"""
        provider = MockTimeProvider(initial_time=0.0)
        time1 = provider.get_current_time()
        time.sleep(0.01)  # Sleep for 10ms
        time2 = provider.get_current_time()
        self.assertEqual(time1, time2)


if __name__ == '__main__':
    unittest.main()
