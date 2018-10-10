import re

"""
    This program supports two ways of validating ssn; from a txt-file or from direct input in program.

        1) If you wish to validate multiple ssn: Go to main() -> set ssn_txt = True -> set filename
        2) If you wish to validate on specific ssn: Go to main() -> set_txt = False -> specify the ssn you wish to validate
    
    * The ssn's must be of type String
    
    Because of the regex, the ssn can not contain multiple dots or dashes in a row. There are multiple good regex-expressions
    online, but I choose to write my own regex-expression. 
"""

days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

class Parse_string:

    def __init__(self, ssn):
        self.ssn = ssn

    def evaluate(self):
        # | -or
        # + - 1 eller mer
        # () - group. F.eks (com|edu)

        # regex sier: tall 0-9, saa - eller ., osv
        pattern = re.compile(r'([0-9]+)(-|.)([0-9][0-9]+)(-|.)([0-9]+(-|.))')
        matches = pattern.finditer(self.ssn)

        # henter ut gruppe (group) nr 2 og 3 fra re.searchen

        string_array = []
        for match in matches:
            temp = match.group(0)
            for char in temp:
                if char.isdigit():
                    string_array.append(char)
                else:
                    continue
        return string_array


class Evaluator:

    def __init__(self):
        pass

    # ******* method for simplicity ******************
    def get_birthday(self, string_array):
        if len(string_array) > 0:  # for error-detection when using txt-file
            if int(string_array[0]) != 0:
                day = int(string_array[0] + string_array[1])
            else:
                day = int(string_array[1])

            if int(string_array[2]) != 0:
                month = int(string_array[2] + string_array[3])
            else:
                month = int(string_array[3])

            year = int(string_array[4] + string_array[5])
        else:
            day, month, year = 0, 0, 0
        return day, month, year

    def get_intarray(self, string_array):
        int_array = []
        for element in string_array:
            int_array.append(int(element))
        return int_array

    def contains_only_digits(self, string_array):
        for element in string_array:
            if element.isalpha():
                return False
        return True

    def validate_month(self, month):
        if 1 <= month and month <= 12:
            return True
        return False

    def validate_day(self,day, month, year):
        max_days = days_in_month[month]
        if month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):  # check for leapyear
            max_days = 29

        if 1 <= day <= max_days:
            return True
        return False

    def validate_length(self, ssn):
        if len(ssn) == 11:
            return True
        return False

    # validate controll number 1
    def validate_controll_number1(self, ssn):
        k1 = ssn[9]
        check_k1 = 11 - ((3 * ssn[0] + 7*ssn[1] + 6*ssn[2] + 1*ssn[3] + 8*ssn[4] + 9*ssn[5] + 4*ssn[6]
                          + 5*ssn[7] + 2 * ssn[8]) % 11)
        if k1 == check_k1:
            return True
        return False

    # validate controll number 2, which is the last number in the ssn
    def validate_controll_number2(self, ssn):
        k2 = ssn[10]
        k1 = ssn[9]
        check_k1 = 11 - ((5 * ssn[0] + 4 * ssn[1] + 3 * ssn[2] + 2 * ssn[3] + 7 * ssn[4] + 6 * ssn[5] + 5 * ssn[6]
                          + 4 * ssn[7] + 3 * ssn[8] + 2*k1) % 11)
        if k2 == check_k1:
            return True
        return False


# class takes a txt-file as parameter and returns an array containing possible ssn's
def read_file(filename):
    ssn_list = []
    with open(filename, 'r') as f:
        for line in f:
            ssn_list.append(line)  # no need to close file
    ssn_list = map(str.strip, ssn_list)  # removing \n
    return ssn_list

# binding method. Returns whether the ssn is true or not
def bind_all(ssn):
    string_array_ssn = Parse_string(ssn).evaluate()
    ev = Evaluator()
    int_array_ssn = ev.get_intarray(string_array_ssn)
    day, month, year = ev.get_birthday(string_array_ssn)
    return (ev.validate_length(string_array_ssn)
                and ev.contains_only_digits(string_array_ssn)
                and ev.validate_day(day, month, year)
                and ev.validate_month(month)
                and ev.validate_controll_number1(int_array_ssn)
                and ev.validate_controll_number2(int_array_ssn))


def main():
    ssn_txt = False
    filename = "ssns.txt"  # set filename here
    ssn = "1111111111111"  # set ssn-number here

    if ssn_txt:
        ssn_list = read_file(filename)
        for element in ssn_list:
            check = bind_all(element)
            if not check:
                print(str(element) + " is not valid.")

            else:
                print(str(element) + " is VALID!")

    else:
        if bind_all(ssn):
            print(str(ssn) + ": korrekt personnummer!")
            return True
        else:
            print(str(ssn) + ": ikke korrekt personnummer")

main()

