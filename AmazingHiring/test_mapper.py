import unittest
import mapper_func


class TestMapperFunc(unittest.TestCase):

    def test_1(self):
        self.assertEqual(mapper_func.mapper(['no'], False), None)

    def test_2(self):
        self.assertEqual(mapper_func.mapper(None, True), None)

    def test_3(self):
        self.assertEqual(mapper_func.mapper(['no'], True), ['no'])

    def test_4(self):
        self.assertEqual(mapper_func.mapper(None, False), ['any'])

    def test_5(self):
        self.assertEqual(mapper_func.mapper(['no', 'phone'], True), ['no', 'phone'])

    def test_6(self):
        self.assertEqual(mapper_func.mapper(['no', 'phone'], False), ['no', 'phone'])

    def test_7(self):
        self.assertEqual(mapper_func.mapper(['phone'], True), ['phone'])

    def test_8(self):
        self.assertEqual(mapper_func.mapper(['phone'], False), ['phone'])

    def test_9(self):
        self.assertEqual(mapper_func.mapper(['phone', 'email'], True), ['phone', 'email'])

    def test_10(self):
        self.assertEqual(mapper_func.mapper(['phone', 'email', 'skype'], False), ['phone', 'email', 'skype'])


if __name__ == '__main__':
    unittest.main()
