"""
Security tests for delivery_manager.py
"""
import sys
import threading
from delivery_manager import (
    DeliveryManager, KitchenGameManager, RecipeListSO, RecipeSO, 
    KitchenObjectSO, PlateKitchenObject
)


def test_none_input_validation():
    """Test that None inputs are properly rejected"""
    print("Testing None input validation...")
    
    # Create sample data
    tomato = KitchenObjectSO("Tomato", 1)
    sandwich_recipe = RecipeSO("Sandwich", [tomato])
    recipe_list = RecipeListSO([sandwich_recipe])
    
    # Test 1: DeliveryManager with None recipe_list_so
    try:
        delivery_manager = DeliveryManager(None)
        print("❌ FAIL: Should have raised ValueError for None recipe_list_so")
        return False
    except ValueError as e:
        print(f"✓ PASS: Correctly rejected None recipe_list_so: {e}")
    
    # Test 2: DeliveryManager with empty recipe list
    try:
        empty_recipe_list = RecipeListSO([])
        delivery_manager = DeliveryManager(empty_recipe_list)
        print("❌ FAIL: Should have raised ValueError for empty recipe list")
        return False
    except ValueError as e:
        print(f"✓ PASS: Correctly rejected empty recipe list: {e}")
    
    # Test 3: deliver_recipe with None plate
    delivery_manager = DeliveryManager(recipe_list)
    try:
        delivery_manager.deliver_recipe(None)
        print("❌ FAIL: Should have raised ValueError for None plate")
        return False
    except ValueError as e:
        print(f"✓ PASS: Correctly rejected None plate: {e}")
    
    print("✓ All None input validation tests passed!\n")
    return True


def test_thread_safety():
    """Test thread-safe singleton implementation"""
    print("Testing thread-safe singleton...")
    
    instances = []
    
    def create_instance():
        instance = KitchenGameManager.get_instance()
        instances.append(instance)
    
    # Create multiple threads
    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check that all instances are the same
    first_instance = instances[0]
    if all(instance is first_instance for instance in instances):
        print(f"✓ PASS: All {len(instances)} instances are identical (thread-safe)")
        print("✓ Thread safety test passed!\n")
        return True
    else:
        print("❌ FAIL: Multiple instances created (not thread-safe)")
        return False


def test_secure_random():
    """Test that secure random is used (indirect test via module import)"""
    print("Testing secure random usage...")
    
    # Check if secrets module is imported in delivery_manager
    import delivery_manager
    if hasattr(delivery_manager, 'secrets'):
        print("✓ PASS: secrets module is imported")
        print("✓ Secure random test passed!\n")
        return True
    else:
        print("❌ FAIL: secrets module not found")
        return False


def test_object_comparison():
    """Test that object comparison uses both id and name"""
    print("Testing object comparison security...")
    
    # Create test objects
    tomato1 = KitchenObjectSO("Tomato", 1)
    tomato2 = KitchenObjectSO("Tomato", 1)  # Same values
    lettuce = KitchenObjectSO("Lettuce", 1)  # Same ID, different name
    
    # Create recipe and delivery manager
    sandwich_recipe = RecipeSO("Sandwich", [tomato1])
    recipe_list = RecipeListSO([sandwich_recipe])
    
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    delivery_manager._waiting_recipe_so_list = [sandwich_recipe]
    
    # Test 1: Correct ingredient should succeed
    plate1 = PlateKitchenObject()
    plate1.add_kitchen_object(tomato2)
    
    success_count = delivery_manager.get_successful_recipes_amount()
    delivery_manager.deliver_recipe(plate1)
    new_count = delivery_manager.get_successful_recipes_amount()
    
    if new_count == success_count + 1:
        print("✓ PASS: Correct ingredient accepted")
    else:
        print("❌ FAIL: Correct ingredient not accepted")
        return False
    
    # Reset for next test
    delivery_manager._waiting_recipe_so_list = [sandwich_recipe]
    
    # Test 2: Same ID but different name should fail
    plate2 = PlateKitchenObject()
    plate2.add_kitchen_object(lettuce)
    
    success_count = delivery_manager.get_successful_recipes_amount()
    delivery_manager.deliver_recipe(plate2)
    new_count = delivery_manager.get_successful_recipes_amount()
    
    if new_count == success_count:
        print("✓ PASS: Wrong ingredient (same ID, different name) correctly rejected")
        print("✓ Object comparison test passed!\n")
        return True
    else:
        print("❌ FAIL: Wrong ingredient was incorrectly accepted")
        return False


def test_empty_plate_handling():
    """Test that empty plates are handled properly"""
    print("Testing empty plate handling...")
    
    # Create recipe and delivery manager
    tomato = KitchenObjectSO("Tomato", 1)
    sandwich_recipe = RecipeSO("Sandwich", [tomato])
    recipe_list = RecipeListSO([sandwich_recipe])
    
    delivery_manager = DeliveryManager(recipe_list)
    delivery_manager._waiting_recipe_so_list = [sandwich_recipe]
    
    # Test with empty plate
    empty_plate = PlateKitchenObject()
    
    success_count = delivery_manager.get_successful_recipes_amount()
    delivery_manager.deliver_recipe(empty_plate)
    new_count = delivery_manager.get_successful_recipes_amount()
    
    if new_count == success_count:
        print("✓ PASS: Empty plate correctly rejected")
        print("✓ Empty plate test passed!\n")
        return True
    else:
        print("❌ FAIL: Empty plate was incorrectly accepted")
        return False


def main():
    """Run all security tests"""
    print("=" * 60)
    print("Running Security Tests for delivery_manager.py")
    print("=" * 60 + "\n")
    
    tests = [
        test_none_input_validation,
        test_thread_safety,
        test_secure_random,
        test_object_comparison,
        test_empty_plate_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}\n")
            results.append(False)
    
    print("=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("✓ All security tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
