import re


class PhoneNumberFormatter:
    def __init__(self):
        self.exp = re.compile(r"\d")

    def pretty_format(self, phone_number):
        phone_number_finds = self.exp.findall(phone_number)
        area_code = "".join(phone_number_finds[-10:-7])
        first_three = "".join(phone_number_finds[-7:-4])
        last_four = "".join(phone_number_finds[-4:])
        return f"({area_code}) {first_three}-{last_four}"


phone_numbers = ["(123) 456-7890", "1234567890", "123.456.7890", "+1 123 456-7890"]

Formatter = PhoneNumberFormatter()
print(list(map(Formatter.pretty_format, phone_numbers)))
