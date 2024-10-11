import unittest
from MyServer import inputData


class testing(unittest.TestCase):
    def test(self):
        values = [
            ["Login", "Aids123", "Skyla1234", "Admin"],
            ["Login", "", "", "False"],
        ]
        for i in values:
            with self.subTest(i=i):
                self.assertEqual(inputData(i[:3]), i[3])


unittest.main()
