"""Unit tests for the DeliveryManager class"""
import unittest
from deliverManager import (
    DeliveryManager, KitchenGameManager, PlateKitchenObject,
    KitchenObjectSO, RecipeSO, RecipeListSO, Event, EventArgs
)
from time_provider import MockTimeProvider
from random_provider import MockRandomProvider


class TestEvent(unittest.TestCase):
    """Test cases for Event class"""
    
    def test_add_handler(self):
        """Test adding an event handler"""
        event = Event()
        handler_called = []
        
        def handler(sender, args):
            handler_called.append(True)
        
        event.add_handler(handler)
        event.invoke(None)
        self.assertTrue(handler_called)
    
    def test_remove_handler(self):
        """Test removing an event handler"""
        event = Event()
        handler_called = []
        
        def handler(sender, args):
            handler_called.append(True)
        
        event.add_handler(handler)
        event.remove_handler(handler)
        event.invoke(None)
        self.assertEqual(len(handler_called), 0)
    
    def test_multiple_handlers(self):
        """Test multiple event handlers"""
        event = Event()
        call_count = []
        
        def handler1(sender, args):
            call_count.append(1)
        
        def handler2(sender, args):
            call_count.append(2)
        
        event.add_handler(handler1)
        event.add_handler(handler2)
        event.invoke(None)
        self.assertEqual(len(call_count), 2)
        self.assertIn(1, call_count)
        self.assertIn(2, call_count)


class TestKitchenGameManager(unittest.TestCase):
    """Test cases for KitchenGameManager class"""
    
    def setUp(self):
        """Reset singleton before each test"""
        KitchenGameManager._instance = None
    
    def test_singleton_pattern(self):
        """Test that KitchenGameManager follows singleton pattern"""
        manager1 = KitchenGameManager.get_instance()
        manager2 = KitchenGameManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_initial_state_not_playing(self):
        """Test that game is not playing initially"""
        manager = KitchenGameManager.get_instance()
        self.assertFalse(manager.is_game_playing())
    
    def test_start_game(self):
        """Test starting the game"""
        manager = KitchenGameManager.get_instance()
        manager.start_game()
        self.assertTrue(manager.is_game_playing())
    
    def test_stop_game(self):
        """Test stopping the game"""
        manager = KitchenGameManager.get_instance()
        manager.start_game()
        manager.stop_game()
        self.assertFalse(manager.is_game_playing())


class TestPlateKitchenObject(unittest.TestCase):
    """Test cases for PlateKitchenObject class"""
    
    def test_initialization(self):
        """Test that PlateKitchenObject initializes with empty list"""
        plate = PlateKitchenObject()
        self.assertEqual(len(plate.get_kitchen_object_so_list()), 0)
    
    def test_add_kitchen_object(self):
        """Test adding kitchen objects to plate"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        objects = plate.get_kitchen_object_so_list()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0], tomato)
    
    def test_get_kitchen_object_list_returns_copy(self):
        """Test that get_kitchen_object_so_list returns a copy"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        
        objects1 = plate.get_kitchen_object_so_list()
        objects2 = plate.get_kitchen_object_so_list()
        
        # Should be equal but not the same object
        self.assertEqual(objects1, objects2)
        self.assertIsNot(objects1, objects2)


class TestDeliveryManager(unittest.TestCase):
    """Test cases for DeliveryManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        # Reset singletons
        DeliveryManager.reset_instance()
        KitchenGameManager._instance = None
        
        # Create test data
        self.tomato = KitchenObjectSO("Tomato", 1)
        self.lettuce = KitchenObjectSO("Lettuce", 2)
        self.bread = KitchenObjectSO("Bread", 3)
        
        self.sandwich_recipe = RecipeSO("Sandwich", [self.bread, self.lettuce, self.tomato])
        self.salad_recipe = RecipeSO("Salad", [self.lettuce, self.tomato])
        
        self.recipe_list = RecipeListSO([self.sandwich_recipe, self.salad_recipe])
        
        # Create mock providers
        self.mock_time = MockTimeProvider(initial_time=0.0)
        self.mock_random = MockRandomProvider()
    
    def test_initialization(self):
        """Test DeliveryManager initialization"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
    
    def test_singleton_pattern(self):
        """Test that DeliveryManager follows singleton pattern"""
        manager1 = DeliveryManager.get_instance(self.recipe_list, self.mock_time, self.mock_random)
        manager2 = DeliveryManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_singleton_requires_recipe_list_on_first_call(self):
        """Test that first call to get_instance requires recipe_list"""
        with self.assertRaises(ValueError):
            DeliveryManager.get_instance()
    
    def test_update_spawns_recipe_after_timer_expires(self):
        """Test that update spawns a recipe after timer expires"""
        # Start the game
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        # Set up mock random to return sandwich recipe
        self.mock_random.set_choices([self.sandwich_recipe])
        
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Advance time past spawn timer
        self.mock_time.advance(5.0)
        manager.update()
        
        # Should have spawned a recipe
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 1)
    
    def test_update_does_not_spawn_when_game_not_playing(self):
        """Test that update does not spawn recipes when game is not playing"""
        game_manager = KitchenGameManager.get_instance()
        # Don't start the game
        
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Advance time past spawn timer
        self.mock_time.advance(5.0)
        manager.update()
        
        # Should not have spawned a recipe
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
    
    def test_update_respects_max_waiting_recipes(self):
        """Test that update respects maximum waiting recipes limit"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        self.mock_random.set_choices([self.sandwich_recipe])
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Spawn recipes until we hit the max
        for i in range(5):
            self.mock_time.advance(5.0)
            manager.update()
        
        # Should not exceed max of 4
        self.assertLessEqual(len(manager.get_waiting_recipe_so_list()), 4)
    
    def test_deliver_recipe_success(self):
        """Test successful recipe delivery"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Manually add a recipe to waiting list
        manager._waiting_recipe_so_list.append(self.sandwich_recipe)
        
        # Create a matching plate
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.bread)
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        
        # Track event
        success_called = []
        manager.on_recipe_success.add_handler(lambda s, a: success_called.append(True))
        
        # Deliver the recipe
        manager.deliver_recipe(plate)
        
        # Should have succeeded
        self.assertEqual(manager.get_successful_recipes_amount(), 1)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
        self.assertTrue(success_called)
    
    def test_deliver_recipe_failure_wrong_ingredients(self):
        """Test failed recipe delivery with wrong ingredients"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Manually add a recipe to waiting list
        manager._waiting_recipe_so_list.append(self.sandwich_recipe)
        
        # Create a non-matching plate
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        
        # Track event
        failed_called = []
        manager.on_recipe_failed.add_handler(lambda s, a: failed_called.append(True))
        
        # Deliver the recipe
        manager.deliver_recipe(plate)
        
        # Should have failed
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 1)
        self.assertTrue(failed_called)
    
    def test_deliver_recipe_failure_wrong_count(self):
        """Test failed recipe delivery with wrong ingredient count"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Manually add a recipe to waiting list
        manager._waiting_recipe_so_list.append(self.salad_recipe)
        
        # Create a plate with too many ingredients
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        plate.add_kitchen_object(self.bread)
        
        # Deliver the recipe
        manager.deliver_recipe(plate)
        
        # Should have failed
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 1)
    
    def test_get_recipe_by_name_found(self):
        """Test get_recipe_by_name when recipe exists"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        recipe = manager.get_recipe_by_name("Sandwich")
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, "Sandwich")
    
    def test_get_recipe_by_name_not_found(self):
        """Test get_recipe_by_name when recipe does not exist"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        recipe = manager.get_recipe_by_name("NonExistentRecipe")
        self.assertIsNone(recipe)
    
    def test_get_recipe_by_name_no_sql_injection(self):
        """Test that get_recipe_by_name is safe from SQL injection"""
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        # Try SQL injection attack
        recipe = manager.get_recipe_by_name("'; DROP TABLE recipes; --")
        # Should safely return None without executing malicious code
        self.assertIsNone(recipe)
    
    def test_reset_for_testing(self):
        """Test reset_for_testing method"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Add some data
        manager._waiting_recipe_so_list.append(self.sandwich_recipe)
        manager._successful_recipes_amount = 5
        
        # Reset
        manager.reset_for_testing()
        
        # Should be reset
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
    
    def test_events_are_fired(self):
        """Test that all events are fired correctly"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        self.mock_random.set_choices([self.sandwich_recipe])
        manager = DeliveryManager(self.recipe_list, self.mock_time, self.mock_random)
        
        # Track events
        spawned_called = []
        completed_called = []
        success_called = []
        failed_called = []
        
        manager.on_recipe_spawned.add_handler(lambda s, a: spawned_called.append(True))
        manager.on_recipe_completed.add_handler(lambda s, a: completed_called.append(True))
        manager.on_recipe_success.add_handler(lambda s, a: success_called.append(True))
        manager.on_recipe_failed.add_handler(lambda s, a: failed_called.append(True))
        
        # Spawn a recipe
        self.mock_time.advance(5.0)
        manager.update()
        self.assertTrue(spawned_called)
        
        # Successful delivery
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.bread)
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        manager.deliver_recipe(plate)
        
        self.assertTrue(completed_called)
        self.assertTrue(success_called)
        
        # Failed delivery
        plate2 = PlateKitchenObject()
        plate2.add_kitchen_object(self.lettuce)
        manager.deliver_recipe(plate2)
        
        self.assertTrue(failed_called)


if __name__ == '__main__':
    unittest.main()
