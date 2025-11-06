"""Unit tests for the random provider module"""
import unittest
from random_provider import RandomProvider, SystemRandomProvider, MockRandomProvider


class TestSystemRandomProvider(unittest.TestCase):
    """Test cases for SystemRandomProvider"""
    
    def test_choice_returns_element_from_list(self):
        """Test that choice returns an element from the list"""
        provider = SystemRandomProvider()
        elements = [1, 2, 3, 4, 5]
        choice = provider.choice(elements)
        self.assertIn(choice, elements)
    
    def test_choice_with_single_element(self):
        """Test that choice works with a single element list"""
        provider = SystemRandomProvider()
        elements = [42]
        choice = provider.choice(elements)
        self.assertEqual(choice, 42)


class TestMockRandomProvider(unittest.TestCase):
    """Test cases for MockRandomProvider"""
    
    def test_choice_returns_first_element_by_default(self):
        """Test that choice returns first element when no predetermined choices"""
        provider = MockRandomProvider()
        elements = [1, 2, 3, 4, 5]
        choice = provider.choice(elements)
        self.assertEqual(choice, 1)
    
    def test_choice_with_predetermined_choices(self):
        """Test that choice returns predetermined choices"""
        provider = MockRandomProvider(predetermined_choices=[3, 1, 4])
        elements = [1, 2, 3, 4, 5]
        
        self.assertEqual(provider.choice(elements), 3)
        self.assertEqual(provider.choice(elements), 1)
        self.assertEqual(provider.choice(elements), 4)
    
    def test_choice_cycles_predetermined_choices(self):
        """Test that choice cycles through predetermined choices"""
        provider = MockRandomProvider(predetermined_choices=[1, 2])
        elements = [1, 2, 3, 4, 5]
        
        self.assertEqual(provider.choice(elements), 1)
        self.assertEqual(provider.choice(elements), 2)
        # Should cycle back to the first choice
        self.assertEqual(provider.choice(elements), 1)
        self.assertEqual(provider.choice(elements), 2)
    
    def test_set_choices(self):
        """Test that choices can be set after initialization"""
        provider = MockRandomProvider()
        elements = [1, 2, 3, 4, 5]
        
        # Initially returns first element
        self.assertEqual(provider.choice(elements), 1)
        
        # Set predetermined choices
        provider.set_choices([5, 4, 3])
        self.assertEqual(provider.choice(elements), 5)
        self.assertEqual(provider.choice(elements), 4)
        self.assertEqual(provider.choice(elements), 3)
    
    def test_empty_predetermined_choices(self):
        """Test behavior with empty predetermined choices list"""
        provider = MockRandomProvider(predetermined_choices=[])
        elements = [1, 2, 3, 4, 5]
        choice = provider.choice(elements)
        self.assertEqual(choice, 1)


if __name__ == '__main__':
    unittest.main()
