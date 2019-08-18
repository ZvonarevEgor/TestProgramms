import unittest
import find_max_func


class TestFindMax(unittest.TestCase):

    def test_float_arr(self):
        self.assertEqual(find_max_func.find_max([1.3, 7.2, 444.0, 3.5]), 444.0)

    def test_int_arr(self):
        self.assertEqual(find_max_func.find_max([1, 3, 5, 123, 9]), 123)

    def test_negative_arr(self):
        self.assertEqual(find_max_func.find_max([9, -5, 6, -69, 22]), 22)

    def test_TypeError_exception(self):
        self.assertRaises(TypeError, find_max_func.find_max, [4, 6, 2, "string", "python", "django"])

    def test_ValueError_exception(self):
        self.assertRaises(ValueError, find_max_func.find_max, [])


if __name__ == '__main__':
    unittest.main()
