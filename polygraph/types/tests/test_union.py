from unittest import TestCase, skip

from polygraph.exceptions import PolygraphValueError
from polygraph.types.basic_type import Union
from polygraph.types.scalar import Float, Int, String


# @skip  # FIXME
class UnionTypeTest(TestCase):
    def test_commutativity(self):
        self.assertEqual(Union(String, Int), Union(Int, String))
        self.assertEqual(Union(String, Int, Float), Union(Float, String, Int, String))

    @skip
    def test_associativity(self):
        self.assertEqual(
            Union(Union(String, Int), Float),
            Union(String, Int, Float),
        )

    def test_pipe_operator(self):
        self.assertEqual(
            String | Int,
            Union(String, Int),
        )

    @skip
    def test_pipe_operator_with_more_than_two_types(self):
        self.assertEqual(
            String | Int | Float,
            Union(String, Int, Float),
        )


class UnionValueTest(TestCase):
    def test_valid_type(self):
        union = String | Int
        self.assertEqual(union(Int(32)), Int(32))
        self.assertEqual(union(String("Test")), String("Test"))

    def test_value_must_be_typed(self):
        union = String | Int
        with self.assertRaises(PolygraphValueError):
            union(32)
        with self.assertRaises(PolygraphValueError):
            union("Test")

    def test_value_must_have_right_type(self):
        union = String | Int
        with self.assertRaises(PolygraphValueError):
            union(Float(32))