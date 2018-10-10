import unittest
import ValidateSSN

class TestValidateSSN(unittest.TestCase):

    def setUp(self):
        pass  # do this later...

    def test_month(self):
        ev = ValidateSSN.Evaluator()
        month_f1 = 130
        month_f2 = 0
        month_f3 = -3
        month_t1 = 1
        month_t2 = 12
        self.assertFalse(ev.validate_month(month_f1))
        self.assertFalse(ev.validate_month(month_f2))
        self.assertFalse(ev.validate_month(month_f3))
        self.assertTrue(ev.validate_month(month_t1))
        self.assertTrue(ev.validate_month(month_t2))

    def test_day(self):
        ev = ValidateSSN.Evaluator()
        day1 = 0
        self.assertFalse(ev.validate_day(day1,1, 2001 ))
        day2 = 33
        self.assertFalse(ev.validate_day(day2, 1, 2001))
        day3 = -1
        self.assertFalse(ev.validate_day(day3, 1, 2001))

    def test_leapyear(self):
        ev = ValidateSSN.Evaluator()
        self.assertTrue(ev.validate_day(29,2,2000))
        self.assertFalse(ev.validate_day(29, 2, 2001))

    def test_length(self):
        ev = ValidateSSN.Evaluator()
        self.assertFalse(ev.validate_length([1,2,3]))
        self.assertTrue(ev.validate_length([1, 2, 3,4,5,6,7,8,9,10,11]))


if __name__ == "__main__":
    unittest.main()
