"""Unit tests for the Point2D class"""
import unittest
import math
from point import Point2D


class TestPoint2D(unittest.TestCase):
    """Test cases for Point2D class"""
    
    def test_initialization(self):
        """Test that Point2D initializes correctly"""
        point = Point2D(3, 4)
        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)
    
    def test_distance_to_horizontal(self):
        """Test distance calculation for horizontal points"""
        point1 = Point2D(0, 0)
        point2 = Point2D(3, 0)
        distance = point1.distance_to(point2)
        self.assertEqual(distance, 3.0)
    
    def test_distance_to_vertical(self):
        """Test distance calculation for vertical points"""
        point1 = Point2D(0, 0)
        point2 = Point2D(0, 4)
        distance = point1.distance_to(point2)
        self.assertEqual(distance, 4.0)
    
    def test_distance_to_diagonal(self):
        """Test distance calculation for diagonal points (Pythagorean theorem)"""
        point1 = Point2D(0, 0)
        point2 = Point2D(3, 4)
        distance = point1.distance_to(point2)
        self.assertEqual(distance, 5.0)
    
    def test_distance_to_same_point(self):
        """Test distance to same point is zero"""
        point = Point2D(5, 5)
        distance = point.distance_to(point)
        self.assertEqual(distance, 0.0)
    
    def test_distance_to_negative_coordinates(self):
        """Test distance calculation with negative coordinates"""
        point1 = Point2D(-3, -4)
        point2 = Point2D(0, 0)
        distance = point1.distance_to(point2)
        self.assertEqual(distance, 5.0)
    
    def test_distance_symmetry(self):
        """Test that distance is symmetric (d(A,B) == d(B,A))"""
        point1 = Point2D(1, 2)
        point2 = Point2D(4, 6)
        distance1 = point1.distance_to(point2)
        distance2 = point2.distance_to(point1)
        self.assertEqual(distance1, distance2)
    
    def test_str_representation(self):
        """Test string representation of Point2D"""
        point = Point2D(3, 4)
        self.assertEqual(str(point), "Point2D(3, 4)")
    
    def test_distance_with_floats(self):
        """Test distance calculation with float coordinates"""
        point1 = Point2D(1.5, 2.5)
        point2 = Point2D(4.5, 6.5)
        expected_distance = math.sqrt((4.5-1.5)**2 + (6.5-2.5)**2)
        distance = point1.distance_to(point2)
        self.assertAlmostEqual(distance, expected_distance, places=10)


if __name__ == '__main__':
    unittest.main()
