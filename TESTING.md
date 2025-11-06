# Testing Guide

## Overview

This project now includes comprehensive unit testing infrastructure to ensure code quality and maintainability. The architecture has been refactored to support dependency injection and testability.

## Running Tests

### Run All Tests

```bash
# Using the test runner
python3 run_tests.py

# Using unittest directly
python3 -m unittest discover -v

# Run specific test file
python3 -m unittest test_delivery_manager.py -v
```

### Run with pytest (optional)

First install dependencies:

```bash
pip install -r requirements.txt
```

Then run:

```bash
pytest -v
pytest --cov=. --cov-report=html  # With coverage report
```

## Architecture Improvements for Testability

### 1. Dependency Injection

The refactored code now uses dependency injection for external dependencies:

- **TimeProvider**: Abstracts system time to allow mocking in tests
- **RandomProvider**: Abstracts random number generation for deterministic testing

Example:
```python
from time_provider import MockTimeProvider
from random_provider import MockRandomProvider

# Create testable instances
mock_time = MockTimeProvider(initial_time=0.0)
mock_random = MockRandomProvider(predetermined_choices=[recipe1, recipe2])

manager = DeliveryManager(recipe_list, mock_time, mock_random)
```

### 2. Separation of Concerns

The code has been restructured to separate:
- **Business Logic**: Core game logic in DeliveryManager
- **External Dependencies**: Time and random providers
- **Data Models**: Clear data classes (RecipeSO, KitchenObjectSO, etc.)

### 3. Testability Features

#### Reset Methods
```python
# Reset singleton instance for clean test state
DeliveryManager.reset_instance()
manager.reset_for_testing()
```

#### Event Testing
All events can be tested by adding handlers:
```python
success_called = []
manager.on_recipe_success.add_handler(lambda s, a: success_called.append(True))
# ... trigger event
assert success_called
```

### 4. Security Improvements

#### SQL Injection Prevention
The original `get_recipe_by_name` method had a SQL injection vulnerability:

**Before (VULNERABLE):**
```python
def get_recipe_by_name(self, user_input):
    query = f"SELECT * FROM recipes WHERE name = '{user_input}'"
    return query
```

**After (SECURE):**
```python
def get_recipe_by_name(self, recipe_name: str) -> Optional[RecipeSO]:
    """レシピ名でレシピを安全に取得（SQL injection対策済み）"""
    for recipe in self._recipe_list_so.recipe_so_list:
        if recipe.name == recipe_name:
            return recipe
    return None
```

For database implementations, use parameterized queries:
```python
cursor.execute("SELECT * FROM recipes WHERE name = ?", (recipe_name,))
```

## Test Structure

### Test Files

- `test_time_provider.py` - Tests for time abstraction (7 tests)
- `test_random_provider.py` - Tests for random abstraction (7 tests)
- `test_point.py` - Tests for Point2D class (9 tests)
- `test_delivery_manager.py` - Comprehensive delivery manager tests (24 tests)

### Test Coverage

The test suite covers:
- ✅ Singleton pattern implementation
- ✅ Dependency injection
- ✅ Time-based logic (recipe spawning)
- ✅ Random selection (deterministic testing)
- ✅ Recipe delivery success/failure scenarios
- ✅ Event firing and handling
- ✅ Edge cases (empty lists, wrong counts, etc.)
- ✅ Security (SQL injection prevention)

## Writing New Tests

### Example Test Structure

```python
import unittest
from deliverManager import DeliveryManager
from time_provider import MockTimeProvider
from random_provider import MockRandomProvider

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test"""
        DeliveryManager.reset_instance()
        self.mock_time = MockTimeProvider(initial_time=0.0)
        self.mock_random = MockRandomProvider()
        # ... create test data
    
    def test_something(self):
        """Test description"""
        # Arrange
        manager = DeliveryManager(recipe_list, self.mock_time, self.mock_random)
        
        # Act
        result = manager.some_method()
        
        # Assert
        self.assertEqual(result, expected_value)
```

### Best Practices

1. **Use Mock Providers**: Always inject mock time and random providers for deterministic tests
2. **Reset State**: Reset singletons in `setUp()` to ensure test isolation
3. **Test Events**: Verify that events fire correctly using handler callbacks
4. **Test Edge Cases**: Include tests for boundary conditions and error cases
5. **Descriptive Names**: Use clear test method names that describe what is being tested

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python3 -m unittest discover -v
```

## Test Metrics

Current test suite:
- **Total Tests**: 47
- **Test Files**: 4
- **Code Coverage**: High coverage of core business logic
- **Execution Time**: < 0.1 seconds

## Future Improvements

Potential areas for additional testing:
1. Integration tests for end-to-end scenarios
2. Performance tests for update loop
3. Stress tests for maximum recipe limits
4. Property-based testing for edge cases
5. Mock database implementation for recipe storage tests
